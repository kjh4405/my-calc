import streamlit as st

# 앱 화면 설정
st.set_page_config(page_title="DHP 비지니스 수익계산기", layout="wide")

# 제목
st.title("🚀 DHP비지니스 수익계산기 (Ver 2.0)")
st.write("4레벨 복제 모델 및 개인 유지비용 시뮬레이션")

# --- 설정값 입력란 (사이드바) ---
st.sidebar.header("📌 개인 및 조직 설정")

# 패키지 데이터 정의
package_info = {
    "Basic": {"cv": 72, "binary": 0.05, "unilevel": 5, "subscription": 30},
    "Standard": {"cv": 216, "binary": 0.06, "unilevel": 10, "subscription": 30},
    "Premium": {"cv": 504, "binary": 0.07, "unilevel": 15, "subscription": 0},
    "Ultimate": {"cv": 1080, "binary": 0.08, "unilevel": 20, "subscription": 0}
}

# 1. 나의 설정
st.sidebar.subheader("1. 나의 설정")
my_pkg = st.sidebar.selectbox("나의 패키지 등급", list(package_info.keys()), index=3)
my_game_type = st.sidebar.selectbox("나의 게임 선택", ["$20 게임", "$40 게임"], index=0)
my_game_count = st.sidebar.number_input("나의 한 달 게임 횟수", value=120, min_value=0)

# 2. 조직 설정
st.sidebar.subheader("2. 조직 복제 설정")
partner_pkg = st.sidebar.selectbox("1레벨 파트너들의 패키지 (이하 동일 적용)", list(package_info.keys()), index=3)
lv1_people = st.sidebar.number_input("나의 직접 소개 (1레벨)", value=2, min_value=1)
duplication = st.sidebar.radio("파트너 복제 명수 (2~4레벨)", [2, 3], index=0)

# 3. 코인 및 가격 설정
st.sidebar.subheader("3. 기타 설정")
future_price = st.sidebar.slider("장래 예상 가격 ($)", 0.1, 10.0, 1.0, step=0.1)

# --- 계산 로직 ---

# A. 나의 월간 지출 계산
game_unit_price = 20 if my_game_type == "$20 게임" else 40
my_monthly_game_cost = my_game_count * game_unit_price
my_subscription = package_info[my_pkg]["subscription"]
total_my_cost = my_monthly_game_cost + my_subscription

# B. 조직 인원 계산 (4레벨까지)
lv2 = lv1_people * duplication
lv3 = lv2 * duplication
lv4 = lv3 * duplication
total_people = lv1_people + lv2 + lv3 + lv4

# C. 1회성 수익 (파트너 패키지 기준)
p_cv = package_info[partner_pkg]["cv"]
total_reg_cv_half = (total_people * p_cv) / 2
orbit_count = total_reg_cv_half // 5460
income_orbit = orbit_count * 450
income_binary = total_reg_cv_half * package_info[my_pkg]["binary"]
income_unilevel = total_people * package_info[my_pkg]["unilevel"]

# D. 매달 수익 (72CV 달성을 위한 120게임 기준)
# 하위 인원들도 본인이 선택한 게임 단가를 따른다고 가정 (단가에 따른 CV 변화)
p_game_cv = 0.6 if my_game_type == "$20 게임" else 1.2
total_game_cv_half = (total_people * 120 * p_game_cv) / 2
m_orbit_count = total_game_cv_half // 5460
m_income_orbit = m_orbit_count * 450
m_income_binary = total_game_cv_half * package_info[my_pkg]["binary"]
m_income_unilevel = total_people * (package_info[my_pkg]["unilevel"] / 10)

# E. 코인 가치
total_adil = total_people * 120 * 10
asset_total = total_adil * future_price

# --- 화면 출력 ---

st.divider()

# 상단 요약 대시보드
c1, c2, c3, c4 = st.columns(4)
c1.metric("4레벨 총 인원", f"{total_people:,} 명")
c2.metric("나의 월 지출", f"${total_my_cost:,}")
c3.metric("1회성 수익", f"${(income_orbit + income_binary + income_unilevel):,.0f}")
c4.metric("월 연금 수익", f"${(m_income_orbit + m_income_binary + m_income_unilevel):,.0f}")

st.subheader("📝 상세 분석 보고서")
tab1, tab2, tab3, tab4 = st.tabs(["나의 유지비용", "1회성 수익", "매달 연금", "ADIL 자산가치"])

with tab1:
    st.write(f"### 💳 나의 월간 유지비용")
    st.write(f"- 선택한 게임: {my_game_type} (판당 ${game_unit_price})")
    st.write(f"- 게임 비용: {my_game_count}판 x ${game_unit_price} = **${my_monthly_game_cost:,.0f}**")
    st.write(f"- 월 구독료 ({my_pkg} 등급): **${my_subscription:,.0f}**")
    st.markdown(f"#### **총 월 지출 예상액: ${total_my_cost:,.0f}**")
    if my_subscription > 0:
        st.warning("⚠️ Basic/Standard 등급은 매달 $30의 구독료가 발생합니다.")

with tab2:
    st.write(f"### 💰 패키지 등록 보너스")
    st.write(f"- 파트너 패키지: {partner_pkg} ({p_cv} CV)")
    st.write(f"- 오빗 수익 ({int(orbit_count)}회전): ${income_orbit:,.0f}")
    st.write(f"- 바이너리 수익: ${income_binary:,.0f}")
    st.write(f"- 유니레벨 수익: ${income_unilevel:,.0f}")

with tab3:
    st.write(f"### 📅 매달 게임 연금 수익")
    st.write(f"- 하위 전원 120게임 수행 기준 (72CV 이상 달성)")
    st.write(f"- 매달 오빗: ${m_income_orbit:,.0f}")
    st.write(f"- 매달 바이너리: ${m_income_binary:,.0f}")
    st.write(f"- 매달 유니레벨: ${m_income_unilevel:,.0f}")

with tab4:
    st.write(f"### 🪙 ADIL 코인 자산 가치")
    st.write(f"- 조직 전체 월 획득량: {total_adil:,.0f} ADIL")
    st.info(f"코인 가격 ${future_price} 도달 시 자산 가치: **${asset_total:,.0f}**")
