"""
stats_helpers.py

집단 비교와 통계검정 결과 해석에 필요한 보조 함수를 모아둔 파일이다.
p-value와 함께 효과크기를 계산해 통계적 유의성과 실질적 차이를 함께 확인한다.
"""

import numpy as np
from scipy.stats import chi2_contingency, f_oneway, ttest_ind


def _drop_nan(values):
    """배열에서 결측치를 제거한 numpy array를 반환한다."""
    arr = np.asarray(values, dtype=float)
    return arr[~np.isnan(arr)]


def cohens_d(a, b):
    """두 집단 평균 차이에 대한 Cohen's d를 계산한다."""
    a = _drop_nan(a)
    b = _drop_nan(b)

    n_a = len(a)
    n_b = len(b)

    if n_a < 2 or n_b < 2:
        return np.nan

    pooled_sd = np.sqrt(
        ((n_a - 1) * a.std(ddof=1) ** 2 + (n_b - 1) * b.std(ddof=1) ** 2)
        / (n_a + n_b - 2)
    )

    if pooled_sd == 0:
        return 0.0

    return (a.mean() - b.mean()) / pooled_sd


def welch_ttest(a, b):
    """Welch 독립표본 t-test와 Cohen's d를 함께 계산한다."""
    a = _drop_nan(a)
    b = _drop_nan(b)

    t_stat, p_value = ttest_ind(a, b, equal_var=False)
    effect_size = cohens_d(a, b)

    return t_stat, p_value, effect_size


def eta_squared(groups):
    """일원분산분석의 eta squared 효과크기를 계산한다."""
    clean_groups = [_drop_nan(group) for group in groups]
    clean_groups = [group for group in clean_groups if len(group) > 0]

    f_stat, p_value = f_oneway(*clean_groups)

    grand = np.concatenate(clean_groups)
    grand_mean = grand.mean()

    ss_between = sum(
        len(group) * (group.mean() - grand_mean) ** 2
        for group in clean_groups
    )
    ss_total = ((grand - grand_mean) ** 2).sum()

    effect_size = ss_between / ss_total if ss_total != 0 else 0.0

    return f_stat, p_value, effect_size


def cramers_v(contingency):
    """카이제곱 검정의 Cramér's V 효과크기를 계산한다."""
    table = np.asarray(contingency, dtype=float)

    chi2, p_value, dof, expected = chi2_contingency(table)

    n = table.sum()
    rows, cols = table.shape

    denominator = n * (min(rows, cols) - 1)
    effect_size = np.sqrt(chi2 / denominator) if denominator != 0 else 0.0

    return chi2, p_value, effect_size


def interpret_d(d):
    """Cohen's d 값을 해석하기 쉬운 문자열로 변환한다."""
    abs_d = abs(d)

    if abs_d >= 0.8:
        return "큼"
    if abs_d >= 0.5:
        return "중간"
    if abs_d >= 0.2:
        return "작음"
    return "매우 작음"


def star(p_value):
    """p-value를 유의성 표기 문자열로 변환한다."""
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return "n.s."


def fmt_p(p_value):
    """보고서 표기에 적합한 p-value 문자열을 반환한다."""
    if p_value < 0.001:
        return "p<.001"

    return f"p={p_value:.3f}".replace("0.", ".")