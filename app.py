import streamlit as st

st.set_page_config(page_title="DHP 수익 시뮬레이터", layout="wide")
st.title("🚀 DHP 비지니스 수익 정밀 분석기")

# 1. 데이터 정의
pkgs = {
    "Basic": {"price": 150, "cv": 72, "bin": 0.05, "sub": 30, "lim": 2},
    "Standard": {"price": 450, "cv": 216, "bin": 0.06, "sub": 30, "lim": 3},
    "Premium": {"price": 1050, "cv": 504, "bin": 0.07, "sub": 0, "lim": 4},
    "Ultimate": {"price": 2250, "cv": 1080, "bin": 0.08, "sub": 0, "lim": 5}
}

# --- 사이드바 설정 ---
st.sidebar.header("📌 설정")
my_p = st.sidebar.selectbox("내 패키지", list(pkgs.keys()), index=2)
game_t = st.sidebar.selectbox("게임 상품", ["$20", "$40"], index=0)
my_gc = st.sidebar.number_input("나의 월 게임수", value=120)

st.sidebar.header("👥 조직 복제")
pa_p = st.sidebar.selectbox("파트너 패키지", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("1대 직접소개", value=2)
dup = st.sidebar.radio("하위 복제 인원", [2, 3])

# --- 계산 로직 ---
# 1인당 발생하는 CV (등록 시 vs 게임 시)
reg_cv_per_person = pkgs[pa_p]["cv"]
game_cv_per_play = 0.005 if game_t == "$20" else 0.01 # 1게임당 발생하는 CV (예시값)
game_cv_per_person_month = 120 * (0.6 if game_t == "$20" else 1.2) # 1인당 월간(120판) 누적 CV

rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}
lim = pkgs[my_p]["lim"]

stats = {}
t_reg_cv = t_game_cv = t_uni_reg = t_uni_mon = 0
curr = l1

for i in range(1, 5):
    if i > 1: curr *= dup
    r_cv_l = curr * reg_cv_per_person
    g_cv_l = curr * game_cv_per_person_month
    t_reg_cv += r_cv_l
    t_game_cv += g_cv_l
    
    r_rev = (r_cv_l * rates[i]) if i <= lim else 0
    m_rev = (g_cv_l * rates[i]) if i <= lim else 0
    stats[i] = {"cnt": curr, "rcv": r_cv_l, "gcv": g_cv_l, "r_r": r_rev, "m_r": m_rev}
    t_uni_reg += r_rev
    t_uni_mon += m_rev

# 바이너리 & 오빗 계산
w_rcv, w_gcv = t_reg_cv / 2, t_game_cv / 2
# 1회성(등록)
i_bin_reg = w_rcv * pkgs[my_p]["bin"]
i_orbit_reg = int(w_rcv // 5460) * 450
# 매달(연금)
i_bin_mon = w_gcv * pkgs[my_p]["bin"]
i_orbit_mon = int(w_gcv // 5460) * 450

# --- 화면 출력 ---
st.divider()
total_people = sum([d["cnt"] for d in stats.values()])
c1, c2, c3, c4 = st.columns(4)
c1.metric("총 인원", f"{total_people:,}명")
c2.metric("나의 월 지출", f"${(my_gc*(20 if game_t=='$20' else 40) + pkgs[my_p]['sub']):,.0f}")
c3.metric("총 등록 보너스", f"${(i_bin_reg + i_orbit_reg + t_uni_reg):,.1f}")
c4.metric("총 월간 보너스", f"${(i_bin_mon + i_orbit_mon + t_uni_mon):,.1f}")

tabs = st.tabs(["💰 1회성 등록 보너스", "📅 매달 연금 보너스", "🎯 ADIL 효율 분석", "💳 지출 상세"])

with tabs[0]:
    st.subheader("초기 패키지 등록 보너스 상세")
    st.write(f"**산출 기준:** 파트너 1인당 등록 CV = **{reg_cv_per_person} CV**")
    col1, col2, col3 = st.columns(3)
    col1.metric("유니레벨", f"${t_uni_reg:,.1f}")
    col2.metric("바이너리", f"${i_bin_reg:,.1f}")
    col3.metric("오빗", f"${i_orbit_reg:,.0f}")
    
    with st.expander("바이너리/오빗 상세 계산 근거"):
        st.write(f"- 전체 등록 CV: {t_reg_cv:,.0f} CV")
        st.write(f"- 소실적(50%) 기준: {w_rcv:,.0f} CV")
        st.write(f"- 바이너리: {w_rcv:,.0f} CV × {int(pkgs[my_p]['bin']*100)}% = ${i_bin_reg:,.1f}")
        st.write(f"- 오빗: {w_rcv:,.0f} CV ÷ 5,460 = {int(w_rcv // 5460)}회전 (${i_orbit_reg:,.0f})")

with tabs[1]:
    st.subheader("월간 게임 활동 보너스 상세")
    cv_per_play = (0.6 if game_t == "$20" else 1.2) / 120
    st.write(f"**산출 기준:** 산하 1명이 1게임당 나에게 주는 CV = **{cv_per_play:.4f} CV**")
    st.write(f"(1인당 월 120판 시 누적 **{0.6 if game_t == '$20' else 1.2} CV** 발생)")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("유니레벨", f"${t_uni_mon:,.1f}")
    col2.metric("바이너리", f"${i_bin_mon:,.1f}")
    col3.metric("오빗", f"${i_orbit_mon:,.0f}")

    with st.expander("바이너리/오빗 상세 계산 근거"):
        st.write(f"- 월간 전체 게임 CV: {t_game_cv:,.2f} CV")
        st.write(f"- 소실적(50%) 기준: {w_gcv:,.2f} CV")
        st.write(f"- 바이너리: {w_gcv:,.2f} CV × {int(pkgs[my_p]['bin']*100)}% = ${i_bin_mon:,.1f}")
        st.write(f"- 오빗: {w_gcv:,.2f} CV ÷ 5,460 = {int(w_gcv // 5460)}회전 (${i_orbit_mon:,.0f})")

with tabs[2]:
    st.subheader("🎯 ADIL 코인 획득 경제성 (사용자 시나리오)")
    win_rate = 0.0625 # 6.25%
    expected_wins = my_gc * win_rate # 120회 시 7.5회
    adil_per_win = 75 # 회당 75개
    total_adil_won = expected_wins * adil_per_win # 7.5 * 75 = 562.5개
    market_val = total_adil_won * 0.4 # 0.4달러 시세 적용
    
    my_cost = my_gc * (20 if game_t == "$20" else 40)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""
        **획득 시뮬레이션**
        - 월 게임수: {my_gc}회
        - 예상 1위 횟수: **{expected_wins:.1f}회** (6.25% 확률)
        - 1회 당첨 시 획득: **75 ADIL**
        - **월간 총 획득: {total_adil_won:.1f} ADIL**
        """)
    with col2:
        st.success(f"""
        **가치 분석 (시세 $0.4 기준)**
        - 획득 코인 가치: **${market_val:.1f}**
        - 게임 비용: ${my_cost:,.0f}
        - **실질 게임 체감비용: ${(my_cost - market_val):,.1f}**
        """)
    st.write(f"결과적으로 코인 가치를 제외하면 게임 한 판을 약 **${(my_cost - market_val)/my_gc:.2f}** 에 즐기는 셈입니다.")

with tabs[3]:
    st.write("### 💳 지출 비용 요약")
    st.write(f"**초기 비용:** 패키지 ${pkgs[my_p]['price']} + 알파 $60 = **${pkgs[my_p]['price']+60}**")
    st.write(f"**월 고정비:** 게임비 ${my_gc*(20 if game_t=='$20' else 40)} + 구독료 ${pkgs[my_p]['sub']} = **${my_gc*(20 if game_t=='$20' else 40)+pkgs[my_p]['sub']}**")
