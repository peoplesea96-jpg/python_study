import streamlit as st
import pandas as pd
from datetime import datetime

# -----------------------------
# 1) 권장 칼로리 계산(TDEE)
# -----------------------------
def bmr_mifflin(sex: str, age: int, height_cm: float, weight_kg: float) -> float:
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age
    return base + 5 if sex == "남성" else base - 161

ACTIVITY_FACTORS = {
    "거의 운동 안 함(좌식)": 1.2,
    "가벼운 활동(주 1~3회)": 1.375,
    "보통 활동(주 3~5회)": 1.55,
    "활발(주 6~7회)": 1.725,
    "매우 활발(강훈련/육체노동)": 1.9,
}
GOAL_FACTORS = {
    "유지": 1.0,
    "감량(-15%)": 0.85,
    "증량(+10%)": 1.10,
}

# -----------------------------
# 2) 음식 DB(예시)
# -----------------------------
FOODS = {
    "밥(흰쌀밥)": {"unit": "공기", "kcal_per_unit": 300},
    "김치": {"unit": "g", "kcal_per_unit": 0.25},        # 100g=25kcal
    "닭가슴살": {"unit": "g", "kcal_per_unit": 1.65},     # 100g=165kcal
    "계란": {"unit": "개", "kcal_per_unit": 70},
    "바나나": {"unit": "개", "kcal_per_unit": 105},
    "사과": {"unit": "개", "kcal_per_unit": 95},
    "우유": {"unit": "ml", "kcal_per_unit": 0.64},        # 100ml=64kcal
    "라면": {"unit": "봉지", "kcal_per_unit": 500},
    "빵(식빵)": {"unit": "장", "kcal_per_unit": 80},
    "아메리카노": {"unit": "잔", "kcal_per_unit": 10},
    "콜라": {"unit": "ml", "kcal_per_unit": 0.42},        # 100ml=42kcal
}

def food_kcal(food_name: str, amount: float) -> float:
    info = FOODS[food_name]
    return amount * info["kcal_per_unit"]

# -----------------------------
# 3) 세션 상태 초기화
# -----------------------------
MEALS = ["아침", "점심", "저녁"]  # 원하면 "간식" 추가 가능

if "meal_logs" not in st.session_state:
    st.session_state.meal_logs = {m: [] for m in MEALS}  # {아침:[...], 점심:[...], ...}

# -----------------------------
# 4) UI
# -----------------------------
st.set_page_config(page_title="식단/칼로리 트래커", page_icon="🍱", layout="centered")
st.title("🍱 식단/칼로리 트래커")
st.caption("아침/점심/저녁별로 음식을 여러 개 추가하고, 하루 기준 칼로리 초과 여부를 확인합니다.")

st.subheader("1) 사용자 정보 입력(기준 칼로리 계산)")

with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        sex = st.selectbox("성별", ["남성", "여성"])
    with c2:
        age = st.number_input("나이", min_value=5, max_value=120, value=30, step=1)
    with c3:
        height = st.number_input("키(cm)", min_value=80.0, max_value=250.0, value=170.0, step=0.5)

    c4, c5 = st.columns(2)
    with c4:
        weight = st.number_input("체중(kg)", min_value=10.0, max_value=300.0, value=65.0, step=0.5)
    with c5:
        activity = st.selectbox("활동 수준", list(ACTIVITY_FACTORS.keys()), index=0)

    goal = st.selectbox("목표", list(GOAL_FACTORS.keys()), index=0)

bmr = bmr_mifflin(sex, int(age), float(height), float(weight))
tdee = bmr * ACTIVITY_FACTORS[activity]
target_kcal = tdee * GOAL_FACTORS[goal]

with st.container(border=True):
    st.metric("오늘 기준 칼로리(kcal)", f"{target_kcal:.0f}")
    st.caption(f"BMR≈{bmr:.0f}, 활동계수={ACTIVITY_FACTORS[activity]}, 목표계수={GOAL_FACTORS[goal]}")

st.subheader("2) 식사 카테고리별 음식 입력")

# 입력 방식: DB/직접입력
mode = st.radio("입력 방식", ["음식 DB에서 선택", "직접 입력(사용자 정의 음식)"], horizontal=True)

# 카테고리 탭(아침/점심/저녁)
tabs = st.tabs(MEALS)

for i, meal in enumerate(MEALS):
    with tabs[i]:
        st.write(f"### 🍽️ {meal} 기록 추가")

        if mode == "음식 DB에서 선택":
            food = st.selectbox(f"[{meal}] 음식 선택", list(FOODS.keys()), key=f"{meal}_food")
            unit = FOODS[food]["unit"]
            amount = st.number_input(f"[{meal}] 먹은 양 ({unit})", min_value=0.0, value=1.0, step=0.5, key=f"{meal}_amt")
            add_btn = st.button(f"{meal}에 추가", type="primary", key=f"{meal}_add_db")

            if add_btn:
                kcal = food_kcal(food, amount)
                st.session_state.meal_logs[meal].append({
                    "시간": datetime.now().strftime("%H:%M"),
                    "식사": meal,
                    "음식": food,
                    "양": amount,
                    "단위": unit,
                    "칼로리(kcal)": round(kcal, 1)
                })
                st.toast(f"{meal}에 기록 추가 ✅")

        else:
            custom_food = st.text_input(f"[{meal}] 음식 이름", value="사용자음식", key=f"{meal}_cfood")
            custom_unit = st.text_input(f"[{meal}] 단위(예: g, ml, 개)", value="g", key=f"{meal}_cunit")
            c6, c7 = st.columns(2)
            with c6:
                custom_amount = st.number_input(f"[{meal}] 먹은 양", min_value=0.0, value=100.0, step=10.0, key=f"{meal}_camt")
            with c7:
                custom_kcal_per_unit = st.number_input(f"[{meal}] 1 단위당 칼로리(kcal)", min_value=0.0, value=1.0, step=0.1, key=f"{meal}_ckpu")

            add_custom_btn = st.button(f"{meal}에 추가(직접)", type="primary", key=f"{meal}_add_custom")

            if add_custom_btn:
                kcal = custom_amount * custom_kcal_per_unit
                st.session_state.meal_logs[meal].append({
                    "시간": datetime.now().strftime("%H:%M"),
                    "식사": meal,
                    "음식": custom_food,
                    "양": custom_amount,
                    "단위": custom_unit,
                    "칼로리(kcal)": round(kcal, 1)
                })
                st.toast(f"{meal}에 기록 추가 ✅")

        # 해당 식사 기록 표시 + 합계
        logs = st.session_state.meal_logs[meal]
        if len(logs) == 0:
            st.info(f"{meal} 기록이 없습니다.")
        else:
            df_meal = pd.DataFrame(logs)
            meal_sum = float(df_meal["칼로리(kcal)"].sum())
            st.metric(f"{meal} 합계(kcal)", f"{meal_sum:.0f}")
            st.dataframe(df_meal, use_container_width=True)

            colA, colB = st.columns(2)
            with colA:
                if st.button(f"{meal} 기록 지우기", key=f"{meal}_clear"):
                    st.session_state.meal_logs[meal] = []
                    st.toast(f"{meal} 기록 삭제 ✅")
            with colB:
                st.caption("기록은 앱 실행 동안 유지됩니다(세션).")

st.subheader("3) 하루 총합 & 초과 판별")

# 전체 합치기
all_rows = []
for meal in MEALS:
    all_rows.extend(st.session_state.meal_logs[meal])

if len(all_rows) == 0:
    st.info("아직 입력된 음식이 없습니다.")
else:
    df_all = pd.DataFrame(all_rows)
    total = float(df_all["칼로리(kcal)"].sum())
    remaining = target_kcal - total

    with st.container(border=True):
        st.metric("하루 섭취 총합(kcal)", f"{total:.0f}")
        st.metric("남은 칼로리(kcal)", f"{remaining:.0f}")

        if total > target_kcal:
            st.error(f"기준 칼로리를 **{total - target_kcal:.0f} kcal** 초과했습니다 ❗")
        else:
            st.success(f"기준 칼로리 이내입니다 ✅ (남은 {remaining:.0f} kcal)")

    st.dataframe(df_all, use_container_width=True)

    if st.button("전체 기록 초기화"):
        st.session_state.meal_logs = {m: [] for m in MEALS}
        st.toast("전체 기록을 초기화했습니다 ✅")
