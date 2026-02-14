import streamlit as st

# 앱 화면 설정
st.set_page_config(page_title="DHP 비지니스 수익계산기", layout="wide")

# 제목
st.title("🚀 DHP비지니스 종합 수익 시뮬레이터")
st.write("유니레벨, 바이너리, 오빗, 그리고 ADIL 코인 자산까지 한눈에 확인하세요.")

# --- 설정값 입력란 (사이드바) ---
st.sidebar.header("📌 설정값 입력")

# 패키지 데이터 정의
package_info = {
    "Basic": {"cv": 72, "binary": 0.05, "sub": 30, "limit": 2},
    "Standard": {"cv": 216, "binary": 0.06, "sub": 30, "limit": 3},
    "Premium": {"cv": 504, "binary": 0.07, "sub": 0, "limit": 4},
    "Ultimate": {"cv": 1080, "binary": 0.08, "sub": 0, "limit": 5}
}

# 1. 나의 설정
st.sidebar.subheader("1. 나의 설정")
my_pkg = st.sidebar.selectbox("나의 패키지 등급", list(package_info.keys()), index=2)
my_game_type = st.sidebar.selectbox("나의 게임 선택", ["$20 게임", "$40 게임"], index=0)
my_game_count = st.sidebar.number_input("나의 한 달 게임 횟수", value=120)

# 2. 조직 설정
st.sidebar.subheader("2. 조직 복제 설정")
partner_pkg = st.sidebar.selectbox("1레벨 파트너들의 패키지", list(package_info.keys()), index=2)
lv1_people = st.sidebar.number_input("나의 직접 소개 (1레벨)", value=2, min_value=1)
duplication = st.sidebar.radio("하위 레벨 복제 인원 (2~4레벨)", [2, 3], index=0)

# 3. 코인 및 가격 설정
st.sidebar.subheader("3. ADIL 코인 설정")
future_price = st.sidebar.slider("장래 예상 가격 ($)", 0.1, 10.0, 1.0, step=0.1)

# --- 계산 로직 시작 ---

# A. 나의 월 지출
game_unit_price = 20 if my_game_type == "$20 게임" else 40
my_monthly_game_cost = my_game_count * game_unit_price
my_subscription = package_info[my_pkg]["sub"]
total_my_cost = my_monthly_game_cost + my_subscription

# B. 조직 인원 및 유니레벨 계산 (4레벨)
p_cv = package_info[partner_pkg]["cv"]
limit = package_info[my_pkg]["limit"]
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}

lv_stats = {}
total_unilevel_reg = 0
total_unilevel_monthly = 0
current_count = lv1_people

# 매달 보너스용 게임 CV (120게임 기준)
game_cv_per_person = 0.6 if my_game_type == "$20 게임" else 1.2
monthly_game_cv_per_person = 120 * game_cv_per_person

for i in range(1, 5):
    if i > 1:
        current_count *= duplication
    
    # 1회성 유니레벨 수익
    reg_revenue = (current_count * p_cv * rates[i]) if i <= limit else 0
    # 매달 유니레벨 수익 (동일 방식 적용: 인원 * 월간게임CV * 요율)
    monthly_revenue = (current_count * monthly_game_cv_per_person * rates[i]) if i <= limit else 0
    
    lv_stats[i] = {
        "count": current_count,
        "reg_revenue": reg_revenue,
        "monthly_revenue": monthly_revenue
    }
    total_unilevel_reg += reg_revenue
    total_unilevel_monthly += monthly_revenue

total_people = sum([d["count"] for d in lv_stats.values()])

# C. 바이너리 & 오빗 계산
# 1회성
total_reg_cv_half = (total_people * p_cv) / 2
orbit_count_reg = total_reg_cv_half // 5460
income_orbit_reg = orbit_count_reg * 450
income_binary_reg = total_reg_cv_half * package_info[my_pkg]["binary"]

# 매달
total_game_cv_half = (total_people * monthly_game_cv_per_person) / 2
orbit_count_monthly = total_game_cv_half // 5460
income_orbit_monthly = orbit_count_monthly * 450
income_binary_monthly = total_game_cv_half * package_info[my_pkg]["binary"]

# D. ADIL 코인 가치
total_adil_monthly = total_
