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
    # 매달 유니레벨 수익 (동일 방식 적용)
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

# D. ADIL 코인 가치 (오타 수정됨: total_people)
total_adil_monthly = total_people * 120 * 10 
asset_value = total_adil_monthly * future_price

# --- 화면 출력 ---

st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("4레벨 총 인원", f"{total_people:,} 명")
c2.metric("나의 월 지출", f"${total_my_cost:,}")
c3.metric("1회성 수익 합계", f"${(income_orbit_reg + income_binary_reg + total_unilevel_reg):,.1f}")
c4.metric("월 연금 수익 합계", f"${(income_orbit_monthly + income_binary_monthly + total_unilevel_monthly):,.1f}")

st.subheader("📝 보너스 상세 내역")
tab1, tab2, tab3, tab4, tab5 = st.tabs(["유니레벨", "바이너리", "오빗", "ADIL 자산", "나의 지출"])

with tab1:
    st.write("### 💎 유니레벨 보너스 (1회성 & 매달)")
    st.write(f"보너스 수령 가능 레벨: {limit}레벨 까지")
    for i, data in lv_stats.items():
        st.write(f"**{i}레벨 ({int(rates[i]*100)}%)**: {data['count']}명")
        st.write(f"- 1회성: ${data['reg_revenue']:,.1f} / 매달: ${data['monthly_revenue']:,.1f}")
    st.divider()
    st.write(f"**유니레벨 총합 - 1회성: ${total_unilevel_reg:,.1f} / 매달: ${total_unilevel_monthly:,.1f}**")

with tab2:
    st.write("### ⚖️ 바이너리 보너스 상세")
    st.write(f"나의 요율: {package_info[my_pkg]['binary']*100:.0f}%")
    st.write("**[1회성]**")
    st.write(f"- 소실적: {total_reg_cv_half:,.0f} CV -> 수익: ${income_binary_reg:,.1f}")
    st.write("**[매달 연금]**")
    st.write(f"- 소실적: {total_game_cv_half:,.0f} CV -> 수익: ${income_binary_monthly:,.1f}")

with tab3:
    st.write("### 🔄 오빗(Orbit) 보너스 상세")
    st.write("기준: 소실적 5,460 CV당 $450")
    st.write("**[1회성]**")
    st.write(f"- {int(orbit_count_reg)}회전 -> 수익: ${income_orbit_reg:,.0f}")
    st.write("**[매달 연금]**")
    st.write(f"- {int(orbit_count_monthly)}회전 -> 수익: ${income_orbit_monthly:,.0f}")

with tab4:
    st.write("### 🪙 ADIL 코인 자산 가치")
    st.metric("월간 총 획득 코인", f"{total_adil_monthly:,.0f} ADIL")
    st.info(f"가격이 ${future_price}일 때 가치: **${asset_value:,.0f}**")
    st.write(f"*(한화 약 {asset_value*1350/100000000:.1f} 억원 / 환율 1,350원 기준)*")

with tab5:
    st.write("### 💳 나의 월간 유지비용")
    st.write(f"- 게임 단가: {my_game_type} / 게임 수: {my_game_count}판")
    st.write(f"- 게임 비용: ${my_monthly_game_cost:,.0f}")
    st.write(f"- 월 구독료: ${my_subscription:,.0f}")
    st.error(f"**나의 총 월 지출: ${total_my_cost:,.0f}**")
