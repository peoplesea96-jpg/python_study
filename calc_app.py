import streamlit as st

# -----------------------------
# 1) 계산 함수(로직)
# -----------------------------
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return None
    return a / b

# 연산 매핑(설계 포인트: if-elif 줄이기)
OPS = {
    "+": ("더하기", add),
    "-": ("빼기", subtract),
    "*": ("곱하기", multiply),
    "/": ("나누기", divide),
}

# -----------------------------
# 2) Streamlit UI
# -----------------------------
st.set_page_config(page_title="계산기 앱", page_icon="🧮", layout="centered")

st.title("🧮 Streamlit 계산기")
st.caption("두 숫자와 연산을 선택하면 결과가 계산됩니다.")

# 입력 영역
col1, col2 = st.columns(2)
with col1:
    num1 = st.number_input("숫자 1", value=0.0, step=1.0, format="%.6f")
with col2:
    num2 = st.number_input("숫자 2", value=0.0, step=1.0, format="%.6f")

# 연산 선택
op = st.radio(
    "연산 선택",
    options=list(OPS.keys()),
    format_func=lambda x: f"{x}  ({OPS[x][0]})",
    horizontal=True
)

# 실행 버튼
run = st.button("계산하기", type="primary")

# 결과 영역
if run:
    op_name, op_func = OPS[op]
    result = op_func(num1, num2)

    if result is None:
        st.error("0으로 나눌 수 없습니다. (분모가 0입니다)")
    else:
        st.success(f"결과: {result}")
        st.write(f"연산: **{op_name}**")
        st.write(f"식: `{num1} {op} {num2} = {result}`")

st.divider()

# -----------------------------
# 3) (옵션) 기록 기능 - 세션 상태
# -----------------------------
st.subheader("🧾 계산 기록")

if "history" not in st.session_state:
    st.session_state.history = []

if run:
    if result is None:
        st.session_state.history.append(f"{num1} {op} {num2} = Error(0으로 나눔)")
    else:
        st.session_state.history.append(f"{num1} {op} {num2} = {result}")

if st.session_state.history:
    for i, item in enumerate(reversed(st.session_state.history), start=1):
        st.write(f"{i}. {item}")
else:
    st.info("아직 계산 기록이 없습니다.")

if st.button("기록 지우기"):
    st.session_state.history = []
    st.toast("기록을 삭제했습니다 ✅")
