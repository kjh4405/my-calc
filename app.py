import streamlit as st

# 앱 화면 설정
st.set_page_config(page_title="DHP 비지니스 수익계산기", layout="wide")

# 제목
st.title("🚀 DHP비지니스 종합 수익 시뮬레이터")
st.write("초기 투자비, 월 지출, 그리고 레벨별 상세 수익 리포트")

# --- 설정값 입력란 (사이드바) ---
st.sidebar.header("📌 설정값 입력")

# 패키지 데이터 정의
package_info = {
    "Basic": {"price": 150, "cv": 72, "binary": 0.05, "sub": 30, "limit": 2},
    "Standard": {"price": 450, "cv": 216, "binary": 0.06, "sub": 30, "limit": 3},
    "Premium": {"price": 1050, "cv": 504, "binary": 0.07, "sub": 0, "limit": 4},
    "Ultimate": {"price": 2250, "cv": 1080, "binary": 0.08, "sub": 0, "limit": 5}
}

# 1. 나의 설정
st.sidebar.subheader("1. 나의 설정")
my_pkg = st.sidebar.selectbox("나의 패키지 등급", list(package_info.keys()), index=2)
my_game_type = st.sidebar.selectbox("나의 게임 선택", ["$20 게임", "$40 게임"], index=0)
my_game_count = st.sidebar.number_input("나의 한 달 게임 횟수", value=120)

# 2. 조직 설정
st.sidebar.subheader("2. 조직 복제 설정")
partner_pkg = st.sidebar.selectbox("파트너 패키지 등급", list(package_info.keys()), index=2)
lv1_people = st.sidebar.number_input("나의 직접 소개 (1레벨)", value=2, min_value=1)
duplication = st.sidebar.radio("하위 복제 인원 (2~4레벨)", [2, 3], index=0)

# 3. 코인 설정
st.sidebar.subheader("3. ADIL 코인 설정")
future_price = st.sidebar.slider("장래 예상 가격 ($)", 0.1, 10.0, 1.0, step=0.1)

# --- 계산 로직 시작 ---

# A. 나의 지출 계산
my_pkg_price = package_info[my_pkg]["price"]
alpha_stage_cost = 60
game_unit_price = 20 if my_game_type == "$20 게임" else 40
my_monthly_game_cost = my_game_count * game_unit_price
my_subscription = package_info[my_pkg]["sub"]

# B. 조직 및 CV 상세 계산 (4레벨)
p_cv = package_info[partner_pkg]["cv"]
limit = package_info[my_pkg]["limit"]
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}

game_cv_per_person = 0.6 if my_game_type == "$20 게임" else 1.2
monthly_game_cv_per_person = 120 * game_cv_per_person

lv_stats = {}
total_unilevel_reg = 0
total_unilevel_monthly = 0
current_count = lv1_people
total_reg_cv_combined = 0
total_game_cv_combined = 0

for i in range(1, 5):
    if i > 1:
        current_count *= duplication
    
    level_reg_cv = current_count * p_cv
    level_game_cv = current_count * monthly_game_cv_per_person
    
    total_reg_cv_combined += level_reg_cv
    total_game_cv_combined += level_game_cv
    
    reg_revenue = (level_reg_cv * rates[i]) if i <= limit else 0
    monthly_revenue = (level_game_cv * rates[i]) if i <= limit else 0
    
    lv_stats[i] = {
        "count": current_count,
        "reg_cv": level_reg_cv,
        "game_cv": level_game_cv,
        "reg_revenue": reg_revenue,
        "monthly_revenue": monthly_revenue
    }
    total_unilevel_reg += reg_revenue
    total_unilevel_monthly += monthly_revenue

total_people = sum([d["count"] for d in lv_stats.values()])

# 바이너리 & 오빗 상세
weak_reg_cv = total_reg_cv_combined / 2
orbit_count_reg = int(weak_reg_cv // 5460)
income_orbit_reg = orbit_count_reg * 450
income_binary_reg = weak_reg_cv * package_info[my_pkg]["binary"]

weak_game_cv = total_game_cv_combined / 2
orbit_count_monthly = int(weak_game_cv // 5460)
income_orbit_monthly = orbit_count_monthly * 450
income_binary_monthly = weak_game_cv * package_info[my_pkg]["binary"]

# ADIL 코인
total_adil_monthly = total_people * 120 * 10 
asset_value = total_adil_monthly * future_price

# --- 화면 출력 ---

st.divider()
dash1, dash2, dash3, dash4 = st.columns(4)
dash1.metric("4레벨 총 인원", f"{total_people:,}명")
dash2.metric("나의 총 지출", f"${(my_pkg_price + alpha_stage_cost + my_monthly_game_cost + my_subscription):,.0f}")
dash3.metric("1회성 보너스", f"${(income_orbit_reg + income_binary_reg + total_unilevel_reg):,.1f}")
dash4.metric("월 연금 수익", f"${(income_orbit_monthly + income_binary_monthly + total_unilevel_monthly):,.1f}")

st.subheader("🔍 상세 분석 데이터")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["보너스 CV 내역", "유
