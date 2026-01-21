import streamlit as st
import pandas as pd
from datetime import datetime
import os

DATA_FILE = "health_history.csv"

# -----------------------------
# 계산 로직
# -----------------------------
def calc_bmi(height_cm: float, weight_kg: float) -> float:
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def bmi_category_kr(bmi: float) -> str:
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

# -----------------------------
# 저장/불러오기
# -----------------------------
COLUMNS = ["날짜", "키(cm)", "체중(kg)", "BMI", "BMI판정", "최고혈압(SBP)", "최저혈압(DBP)"]

def load_data() -> pd.DataFrame:
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        # 컬럼 누락 대비
        for c in COLUMNS:
            if c not in df.columns:
                df[c] = None
        return df[COLUMNS]
    return pd.DataFrame(columns=COLUMNS)

def save_data(df: pd.DataFrame) -> None:
    df.to_csv(DATA_FILE, index=False)

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="건강 기록기 (BMI + 혈압)", page_icon="🩺", layout="centered")
st.title("🩺 건강 기록기 (BMI + 혈압)")
st.caption("날짜/키/체중/혈압을 입력하면 BMI 계산과 함께 기록됩니다. (CSV로 저장/불러오기)")

df = load_data()

with st.container(border=True):
    # 날짜는 사용자가 직접 입력할 수 있게 (기록 날짜 소급 가능)
    record_date = st.date_input("날짜", value=datetime.now().date())

    c1, c2 = st.columns(2)
    with c1:
        height = st.number_input("키 (cm)", min_value=80.0, max_value=250.0, value=170.0, step=0.5)
    with c2:
        weight = st.number_input("체중 (kg)", min_value=10.0, max_value=300.0, value=65.0, step=0.5)

    c3, c4 = st.columns(2)
    with c3:
        sbp = st.number_input("최고혈압(SBP) (mmHg)", min_value=50, max_value=250, value=120, step=1)
    with c4:
        dbp = st.number_input("최저혈압(DBP) (mmHg)", min_value=30, max_value=200, value=80, step=1)

    add_btn = st.button("기록 추가(저장)", type="primary")

# -----------------------------
# 기록 추가 + 저장
# -----------------------------
if add_btn:
    if height <= 0:
        st.error("키는 0보다 커야 합니다.")
    elif sbp <= dbp:
        st.warning("일반적으로 최고혈압(SBP)이 최저혈압(DBP)보다 큽니다. 입력값을 확인해보세요.")
        # 그래도 저장은 허용(현장 데이터 입력은 다양한 경우가 있어)
        bmi = calc_bmi(height, weight)
        cat = bmi_category_kr(bmi)
        new_row = {
            "날짜": record_date.strftime("%Y-%m-%d"),
            "키(cm)": round(height, 1),
            "체중(kg)": round(weight, 1),
            "BMI": round(bmi, 1),
            "BMI판정": cat,
            "최고혈압(SBP)": int(sbp),
            "최저혈압(DBP)": int(dbp),
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.toast("기록이 저장되었습니다 ✅")
    else:
        bmi = calc_bmi(height, weight)
        cat = bmi_category_kr(bmi)
        new_row = {
            "날짜": record_date.strftime("%Y-%m-%d"),
            "키(cm)": round(height, 1),
            "체중(kg)": round(weight, 1),
            "BMI": round(bmi, 1),
            "BMI판정": cat,
            "최고혈압(SBP)": int(sbp),
            "최저혈압(DBP)": int(dbp),
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.toast("기록이 저장되었습니다 ✅")

# -----------------------------
# 저장된 표 표시
# -----------------------------
st.divider()
st.subheader("📋 기록표")

if df.empty:
    st.info("저장된 기록이 없습니다. 위에서 기록을 추가해보세요.")
else:
    # 날짜 기준 정렬(최근이 위)
    try:
        df_sorted = df.copy()
        df_sorted["날짜"] = pd.to_datetime(df_sorted["날짜"], errors="coerce")
        df_sorted = df_sorted.sort_values(by="날짜", ascending=False)
        df_sorted["날짜"] = df_sorted["날짜"].dt.strftime("%Y-%m-%d")
    except Exception:
        df_sorted = df

    st.dataframe(df_sorted, use_container_width=True)

    colA, colB, colC = st.columns(3)

    with colA:
        if st.button("기록 전체 삭제"):
            df = df.iloc[0:0]
            save_data(df)
            st.warning("모든 기록이 삭제되었습니다.")

    with colB:
        st.download_button(
            label="CSV 다운로드",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="health_history.csv",
            mime="text/csv"
        )

    with colC:
        st.caption("※ 파일 저장 위치: 실행 폴더에 health_history.csv")
