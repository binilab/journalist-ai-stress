"""
variable_mapping.py

2023년과 2025년 「언론인 조사」의 주요 분석 변수를
동일 개념 단위로 연결하기 위한 변수 매핑 파일이다.
"""

MAPPING = {
    "press_fair": {2023: "q1_1", 2025: "q1_1"},
    "press_expert": {2023: "q1_2", 2025: "q1_2"},
    "press_accurate": {2023: "q1_3", 2025: "q1_3"},
    "press_trust": {2023: "q1_4", 2025: "q1_4"},
    "press_influence": {2023: "q1_5", 2025: "q1_5"},
    "press_free": {2023: "q1_6", 2025: "q1_6"},

    "digital_response": {2023: "q4", 2025: "q4"},
    "digital_fatigue": {2023: "q6", 2025: "q5"},

    "satis_job": {2023: "q24_1", 2025: "q19_1"},
    "satis_company": {2023: "q24_2", 2025: "q19_2"},
    "satis_task": {2023: "q24_3", 2025: "q19_3"},

    "burnout_exhaust": {2023: "q26_3", 2025: "q21_3"},
    "burnout_cynic": {2023: "q26_4", 2025: "q21_4"},

    "ai_speed": {2023: "q45_1", 2025: "q39_1"},
    "ai_accuracy": {2023: "q45_2", 2025: "q39_2"},
    "ai_efficiency": {2023: "q45_3", 2025: "q39_3"},

    "ai_copyright": {2023: "q45_4", 2025: "q39_4"},
    "ai_jobthreat": {2023: "q45_5", 2025: "q39_6"},
    "ai_misinfo": {2023: None, 2025: "q39_5"},

    "gender": {2023: "DQ1", 2025: "DQ1"},
    "age": {2023: "DQ2", 2025: "DQ2"},
    "media_type": {2023: "SQ1", 2025: "SQ1"},
}

ROLE_IMPORTANCE = [f"q2_{i}" for i in range(1, 8)]
ROLE_PERFORMANCE = [f"q3_{i}" for i in range(1, 8)]

MEDIA_LABELS = {
    1: "신문사",
    2: "방송사",
    3: "인터넷언론사",
    4: "뉴스통신사",
}


def get_var(concept, year):
    """개념명과 연도를 입력하면 해당 연도의 실제 변수명을 반환한다."""
    if concept not in MAPPING:
        raise KeyError(f"{concept}은(는) MAPPING에 정의되어 있지 않습니다.")

    if year not in MAPPING[concept]:
        raise KeyError(f"{year}년 변수 매핑이 정의되어 있지 않습니다.")

    return MAPPING[concept][year]