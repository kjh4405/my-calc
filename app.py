import streamlit as st

# 앱 화면 설정
st.set_page_config(page_title="DHP 비지니스 수익계산기", layout="wide")

# 제목 변경
st.title("🚀 DHP비지니스 수익계산기")
st.write("나의 패키지와 팀 복제 전략에 따른 종합 수익 시뮬레이션")

# --- 설정값 입력란 (사이드바) ---
st.sidebar.header("📌 설정값 입력")

# 1. 패키지 정보 설정
package_info = {
    "Basic": {"cv": 72, "binary": 0.05, "unilevel": 5},
    "Standard": {"cv": 216, "binary": 0.06, "unilevel": 10},
    "Premium": {"cv": 504, "binary": 0.07, "unilevel": 15},
    "Ultimate": {"cv": 1080, "binary": 0.08, "unilevel": 20}
}

# 나의 패키지 선택 -> 요율 자동 표시
my_pkg = st.sidebar.selectbox("나의 패키지 등급 선택", list(package_info.keys()), index=3)
my_binary_rate = package_info[my_pkg]["binary"]
my_unilevel_val = package_info[my_pkg]["unilevel"]

st.sidebar.info(f"선택됨: 바이너리 {my_binary_rate*100:.0f}% / 유니레벨 ${my_unilevel_val}")

# 2. 인원 복제 설정
st.sidebar.subheader("👥 인원 복제 전략")
lv1_people = st.sidebar.number_input("나의 직접 소개 (1레벨)", value=2, min_value=1)
duplication = st.sidebar.radio("파트너 복제 명수 (2~5레벨)", [2, 3], index=0)

# 3. 게임 상품 설정 ($20 vs $40)
game_type = st.sidebar.selectbox("게임 상품 선택", ["$20 게임", "$40 게임"], index=0)
game_cv = 0.6 if game_type == "$20 게임" else 1.2

# 4. ADIL 코인 설정
st.sidebar.subheader("🪙 ADIL 코인 가치")
adil_per_game = 10 # 한 판당 10개 획득 가정
future_price = st.sidebar.slider("장래 예상 가격 ($)", 0.1, 10.0, 1.0, step=0.1)

# --- 계산 로직 ---
# 단계별 인원 계산
lv2 = lv1_people * duplication
lv3 = lv2 * duplication
lv4 = lv3 * duplication
lv5 = lv4 * duplication
total_people = lv1_people + lv2 + lv3 + lv4 + lv5

# 1회성 수익 (등록 시)
reg_cv = package_info[my_pkg]["cv"]
total_reg_cv_half = (total_people * reg_cv) / 2
orbit_count = total_reg_cv_half // 5460
income_orbit = orbit_count * 450
income_binary = total_reg_cv_half * my_binary_rate
income_unilevel = total_people * my_unilevel_val

# 매달 연금 수익 (게임 시)
monthly_games = 120
total_game_cv_half = (total_people * monthly_games * game_cv) / 2
m_orbit_count = total_game_cv_half // 5460
m_income_orbit = m_orbit_count * 450
m_income_binary = total_game_cv_half * my_binary_rate
m_income_unilevel = total_people * (my_unilevel_val / 10) # 게임 유니레벨은 1/10 가정

# 자산 가치 (ADIL 코인)
total_adil = total_people * monthly_games * adil_per_game
asset_total = total_adil * future_price

# --- 결과 출력 ---
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("총 인원 (5단계)", f"{total_people:,} 명")
c2.metric("1회성 합계", f"${(income_orbit + income_binary + income_unilevel):,.0f}")
c3.metric("월 연금 합계", f"${(m_income_orbit + m_income_binary + m_income_unilevel):,.0f}")

st.subheader("📝 상세 분석")
tab1, tab2, tab3 = st.tabs(["1회성 수익", "매달 연금", "ADIL 자산가치"])

with tab1:
    st.write(f"**패키지 등록 보너스** (소실적 CV: {total_reg_cv_half:,.0f})")
    st.write(f"- 오빗 ({int(orbit_count)}회전): ${income_orbit:,.0f}")
    st.write(f"- 바이너리: ${income_binary:,.0f}")
    st.write(f"- 유니레벨: ${income_unilevel:,.0f}")

with tab2:
    st.write(f"**월간 게임 보너스** (기준: {game_type})")
    st.write(f"- 매달 오빗: ${m_income_orbit:,.0f}")
    st.write(f"- 매달 바이너리: ${m_income_binary:,.0f}")
    st.write(f"- 매달 유니레벨: ${m_income_unilevel:,.0f}")

with tab3:
    st.write(f"**🪙 ADIL 코인 미래 자산**")
    st.write(f"- 월간 총 획득량: {total_adil:,.0f} ADIL")
    st.info(f"가격이 ${future_price}일 때 가치: **${asset_total:,.0f}** (한화 약 {asset_total*1350/100000000:.1f} 억원)")
