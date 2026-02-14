import streamlit as st
import math

st.set_page_config(page_title="DHP 종합 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 종합 수익 및 확률 분석")

# 1. 데이터 정의
pkgs = {
    "Basic": {"price": 150, "cv": 72, "bin": 0.05, "sub": 30, "lim": 2},
    "Standard": {"price": 450, "cv": 216, "bin": 0.06, "sub": 30, "lim": 3},
    "Premium": {"price": 1050, "cv": 504, "bin": 0.07, "sub": 0, "lim": 4},
    "Ultimate": {"price": 2250, "cv": 1080, "bin": 0.08, "sub": 0, "lim": 5}
}

# --- 사이드바 설정 ---
st.sidebar.header("📌 기본 설정")
my_p = st.sidebar.selectbox("내 패키지", list(pkgs.keys()), index=2)
game_t = st.sidebar.selectbox("게임 상품", ["$20", "$40"], index=0)
my_gc = st.sidebar.number_input("나의 한달 게임수", value=120, min_value=1)

st.sidebar.header("👥 조직 복제 설정")
pa_p = st.sidebar.selectbox("파트너 패키지", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("1대 직접소개", value=2, min_value=1)
dup = st.sidebar.radio("하위 복제 인원", [2, 3], index=0)

st.sidebar.header("🪙 코인 시세 설정")
market_price = st.sidebar.number_input("현재 ADIL 시세 ($)", value=0.4)
future_price = st.sidebar.slider("장래 목표 가격 ($)", 0.1, 10.0, 1.0)

# --- 계산 로직 ---

# A. 확률 계산 (1회 승률 6.25%)
win_prob = 0.0625 # 6.25%
expected_wins = my_gc * win_prob # 한달 예상 1위 횟수 (기댓값)
# 한 달 동안 적어도 한 번 이상 1위를 할 확률 (여사건 이용)
at_least_one_win_prob = (1 - (1 - win_prob)**my_gc) * 100 

# B. ADIL 수익 및 효율
adil_per_win = 100 # 1위 시 100개 가정 (수정 가능)
total_my_adil = expected_wins * adil_per_win
g_up = 20 if game_t == "$20" else 40
my_total_game_cost = my_gc * g_up
my_token_price = my_total_game_cost / total_my_adil if total_my_adil > 0 else 0

# C. 조직 보너스 계산 (바이너리, 오빗, 유니레벨)
g_cv_val = 0.6 if game_t == "$20" else 1.2
m_g_cv = 120 * g_cv_val # 조직원당 발생하는 월 게임 CV
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}
lim = pkgs[my_p]["lim"]

stats = {}
t_reg_cv = t_game_cv = t_uni_reg = t_uni_mon = 0
curr = l1

for i in range(1, 5):
    if i > 1: curr *= dup
    r_cv_l = curr * pkgs[pa_p]["cv"]
    g_cv_l = curr * m_g_cv
    t_reg_cv += r_cv_l
    t_game_cv += g_cv_l
    
    r_rev = (r_cv_l * rates[i]) if i <= lim else 0
    m_rev = (g_cv_l * rates[i]) if i <= lim else 0
    
    stats[i] = {"cnt": curr, "rcv": r_cv_l, "gcv": g_cv_l, "r_r": r_rev, "m_r": m_rev}
    t_uni_reg += r_rev
    t_uni_mon += m_rev

# D. 바이너리 및 오빗 최종 산출
total_p = sum([d["cnt"] for d in stats.values()])
w_rcv, w_gcv = t_reg_cv / 2, t_game_cv / 2 # 소실적 5:5 가정

i_bin_reg = w_rcv * pkgs[my_p]["bin"]
i_orbit_reg = int(w_rcv // 5460) * 450

i_bin_mon = w_gcv * pkgs[my_p]["bin"]
i_orbit_mon = int(w_gcv // 5460) * 450

# --- 화면 출력 ---
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("4레벨 총 인원", f"{total_p:,}명")
c2.metric("나의 총 지출(초기+월)", f"${(pkgs[my_p]['price']+60+my_total_game_cost+pkgs[my_p]['sub']):,.0f}")
c3.metric("1회성 총 보너스", f"${(i_bin_reg + i_orbit_reg + t_uni_reg):,.1f}")
c4.metric("월 연금 총 수익", f"${(i_bin_mon + i_orbit_mon + t_uni_mon):,.1f}")

tabs = st.tabs(["🪙 ADIL 확률/효율", "💎 유니레벨", "⚖️ 바이너리/오빗", "📊 CV 및 지출 상세"])

with tabs[0]:
    st.write("### 🎯 ADIL 코인 획득 확률 및 경제성 분석")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""
        **통계적 확률 분석**
        - 1회 레이스 승률: **6.25%**
        - 한 달({my_gc}회) 게임 시 1회 이상 당첨 확률: **{at_least_one_win_prob:.2f}%**
        - 한 달 예상 1위 횟수: **{expected_wins:.2f}회**
        - 예상 획득 코인: **{total_my_adil:,.1f} ADIL**
        """)
    with col2:
        st.success(f"""
        **실질 취득 단가 분석**
        - 게임 투자비: ${my_total_game_cost:,.0f}
        - 나의 코인 평단가: **${my_token_price:.3f}**
        - 현재 시세(${market_price}) 대비 이득: **${(market_price - my_token_price):.3f}/개**
        """)

with tabs[1]:
    st.write("### 💎 유니레벨 상세 (3%, 5%, 8%, 5%)")
    for i, d in stats.items():
        st.write(f"**{i}대**({d['cnt']}명) 수령: {'✅' if i<=lim else '❌'} | 등록 ${d['r_r']:,.1f} / 게임 ${d['m_r']:,.1f}")

with tabs[2]:
    st.write("### ⚖️ 바이너리 & 오빗 (소실적 기준)")
    col_reg, col_mon = st.columns(2)
    with col_reg:
        st.markdown("**[1회성]**")
        st.write(f"- 바이너리: ${i_bin_reg:,.1f}")
        st.write(f"- 오빗 ({int(w_rcv // 5460)}회): ${i_orbit_reg:,.0f}")
    with col_mon:
        st.markdown("**[매달 연금]**")
        st.write(f"- 바이너리: ${i_bin_mon:,.1f}")
        st.write(f"- 오빗 ({int(w_gcv // 5460)}회): ${i_orbit_mon:,.0f}")

with tabs[3]:
    st.write("### 📊 상세 데이터")
    st.write(f"**등록 CV 합계:** {t_reg_cv:,.0f} (소실적: {w_rcv:,.0f})")
    st.write(f"**게임 CV 합계:** {t_game_cv:,.0f} (소실적: {w_gcv:,.0f})")
    st.divider()
    st.write(f"**초기 지출:** 패키지 ${pkgs[my_p]['price']} + 알파 $60 = **${pkgs[my_p]['price']+60}**")
    st.write(f"**월 유지비:** 게임비 ${my_total_game_cost} + 구독료 ${pkgs[my_p]['sub']} = **${my_total_game_cost+pkgs[my_p]['sub']}**")
