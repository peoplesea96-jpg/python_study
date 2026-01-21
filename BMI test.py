import streamlit as st

# -----------------------------
# 1) BMI 로직
# -----------------------------
def calc_bmi(height_cm: float, weight_kg: float) -> float:
    """키(cm), 몸무게(kg)로 BMI 계산"""
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def bmi_category_kr(bmi: float) -> str:
    """
    (교육용) 한국에서 흔히 쓰는 BMI 분류 기준(아시아-태평양/국내에서 자주 사용)
    - 저체중: < 18.5
    - 정상: 18.5 ~ 22.9
    - 과체중: 23.0 ~ 24.9
    - 비만(1단계): 25.0 ~ 29.9
    - 고도비만(2단계 이상): >= 30.0
    """
    if bmi < 18.5:
        return "저체중"
    elif bmi < 23.0:
        return "정상"
    elif bmi < 25.0:
        return "과체중"
    elif bmi < 30.0:
        return "비만"
    else:
        return "고도비만"

def bmi_tip(category: str) -> str:
    tips = {
        "저체중": "균형 잡힌 식사 + 근력운동으로 건강한 체중 증가를 목표로 해보세요.",
        "정상": "현재 상태를 유지하며 규칙적인 운동과 식습관을 지속해보세요.",
        "과체중": "가벼운 유산소(걷기)와 식단 조절로 체중 관리를 시작해보세요.",
        "비만": "식단(당/지방) 조절 + 주 3~5회 운동을 권장해요. 필요하면 전문가 상담도 좋아요.",
        "고도비만": "건강 위험이 커질 수 있어요. 의료진/전문가와 상담하여 계획적으로 관리해보세요.",
    }
    return tips.get(category, "")

# -----------------------------
# 2) Streamlit UI
# -----------------------------
st.set_page_config(page_title="BMI 비만 검사기", page_icon="🧍", layout="centered")

st.title("🧍 BMI 체질량 비만 검사기")
st.caption("키와 몸무게를 입력하면 BMI와 비만도를 계산합니다.")

with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        height = st.number_input("키 (cm)", min_value=50.0, max_value=250.0, value=170.0, step=0.5)
    with col2:
        weight = st.number_input("몸무게 (kg)", min_value=10.0, max_value=300.0, value=65.0, step=0.5)

    run = st.button("BMI 계산하기", type="primary")

if run:
    bmi = calc_bmi(height, weight)
    category = bmi_category_kr(bmi)

    st.subheader("📌 결과")
    st.metric("BMI", value=f"{bmi:.1f}")
    st.write(f"판정: **{category}**")
    st.info(bmi_tip(category))

    # -----------------------------
    # 3) 기록(옵션)
    # -----------------------------
    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append({
        "키(cm)": height,
        "몸무게(kg)": weight,
        "BMI": round(bmi, 1),
        "판정": category
    })

st.divider()
st.subheader("🧾 계산 기록")

if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.info("아직 기록이 없습니다. 위에서 BMI를 계산해보세요.")
else:
    st.dataframe(st.session_state.history, use_container_width=True)

    colA, colB = st.columns(2)
    with colA:
        if st.button("기록 지우기"):
            st.session_state.history = []
            st.toast("기록을 삭제했습니다 ✅")
    with colB:
        st.caption("※ 기록은 브라우저 세션 동안만 유지됩니다.")
