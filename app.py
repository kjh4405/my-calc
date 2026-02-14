import streamlit as st

# 1. 앱 기본 설정
st.set_page_config(page_title="DHP 비지니스 수익계산기", layout="wide")

st.title("🚀 DHP비지니스 종합 수익 시뮬레이터")
st.write("초기 투자비부터 월 연금 수익, ADIL 코인 자산까지 정밀 분석")

# 2. 데이터 정의
package_info = {
    "Basic": {"price": 150, "cv": 72, "binary": 0.05, "sub": 30, "limit": 2},
    "Standard": {"price": 450, "cv": 216, "binary": 0.06, "sub": 30, "limit": 3},
    "Premium": {"price": 1050, "cv": 504, "binary": 0.07, "sub": 0, "limit": 4},
    "Ultimate": {"price": 2250, "cv": 1080, "binary": 0.08, "sub": 0, "limit": 5}
}

# 3. 사이드바 입력창
st.sidebar.header("📌 설정값 입력")

st.sidebar.subheader("1. 나의 설정")
my_pkg = st.sidebar.selectbox("나의 패키지 등급", list(package_info.keys()), index=2)
my_game_type = st.sidebar.selectbox("나의 게임 선택", ["$20 게임", "$40 게임"], index=0)
my_game_count = st.sidebar.number_input("나의 한 달 게임 횟수", value=120)

st.sidebar.subheader("2. 조직 복제 설정")
partner_pkg = st.sidebar.selectbox("파트너 패키지 등급", list(package_info.keys()), index=2)
lv1_people = st.sidebar.number_input("나의 직접 소개 (1레벨)", value=2, min_value=1)
duplication = st.sidebar.radio("하위 복제 인원 (2~4레벨)", [2, 3], index=0)

st.sidebar.subheader("3. 코인 설정")
future_price = st.sidebar.slider("장래 예상 가격 ($)", 0.1, 10.0, 1.0, step=0.1)

# 4. 계산 로직
my_pkg_price = package_info[my_pkg]["price"]
alpha_stage_cost = 60
game_unit_price = 20 if my_game_type == "$20 게임" else 40
my_monthly_game_cost = my_game_count * game_unit_price
my_subscription = package_info[my_pkg]["sub"]

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
    
    reg_rev = (level_reg_cv * rates[i]) if i <= limit else 0
    mon_rev = (level_game_cv * rates[i]) if i <= limit else 0
    
    lv_stats[i] = {"count": current_count, "reg_cv": level_reg_cv, "game_cv": level_game_cv, "reg_rev": reg_rev, "mon_rev": mon_rev}
    total_unilevel_reg += reg_rev
    total_unilevel_monthly += mon_rev

total_people = sum([d["count"] for d in lv_stats.values()])

weak_reg_cv = total_reg_cv_combined / 2
orbit_reg = int(weak_reg_cv // 5460)
income_orbit_reg = orbit_reg * 450
income_binary_reg = weak_reg_cv * package_info[my_pkg]["binary"]

weak_game_cv = total_game_cv_combined / 2
orbit_mon = int(weak_game_cv // 5460)
income_orbit_mon = orbit_mon * 450
income_binary_mon = weak_game_cv * package_info[my_pkg]["binary"]

total_adil_monthly = total_people * 120 * 10 
asset_value = total_adil_monthly * future_price

# 5. 화면 출력
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("총 인원 (4단계)", f"{total_people:,}명")
c2.metric("나의 총 지출", f"${(my_pkg_price + alpha_stage_cost + my_monthly_game_cost + my_subscription):,.0f}")
c3.metric("1회성 보너스", f"${(income_orbit_reg + income_binary_reg + total_unilevel_reg):,.1f}")
c4.metric("월 연금 수익", f"${(income_orbit_mon + income_binary_mon + total_unilevel_monthly):,.1f}")

st.subheader("🔍 상세 분석 데이터")
t1, t2, t3, t4, t5 = st.tabs(["보너스 CV 내역", "유니레벨 상세", "바이너리/오빗", "ADIL 자산", "지출 상세 내역"])

with t1:
    st.info("### 📊 보너스 산출 레벨별 CV")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**[1회성] 패키지 등록 CV**")
        for i, d in lv_stats.items():
            st.write(f"- {i}레벨: {d['reg_cv']:,.0f} CV")
        st.markdown(f"**총 합계: {total_reg_cv_combined:,.0f} CV**")
    with col_b:
        st.write("**[매달] 게임 활동 CV**")
        for i, d in lv_stats.items():
            st.write(f"- {i}레벨: {d['game_cv']:,.0f} CV")
        st.markdown(f"**총 합계: {total_game_cv_combined:,.0f} CV**")

with t2:
    st.write("### 💎 유니레벨 보너스 (3, 5, 8, 5%)")
    for i, d
