import streamlit as st

st.set_page_config(page_title="DHP 수익계산기", layout="wide")
st.title("🚀 DHP비지니스 종합 수익 및 ADIL 효율 분석")

# 데이터 정의
pkgs = {
    "Basic": {"price": 150, "cv": 72, "bin": 0.05, "sub": 30, "lim": 2},
    "Standard": {"price": 450, "cv": 216, "bin": 0.06, "sub": 30, "limit": 3},
    "Premium": {"price": 1050, "cv": 504, "bin": 0.07, "sub": 0, "lim": 4},
    "Ultimate": {"price": 2250, "cv": 1080, "bin": 0.08, "sub": 0, "lim": 5}
}

# --- 사이드바 설정 ---
st.sidebar.header("📌 기본 설정")
my_p = st.sidebar.selectbox("내 패키지", list(pkgs.keys()), index=2)
game_t = st.sidebar.selectbox("게임 선택", ["$20", "$40"])
my_gc = st.sidebar.number_input("내 한달 게임수", value=120)

st.sidebar.header("🪙 ADIL 획득 설정")
win_rate = st.sidebar.slider("1위 당첨 확률 (%)", 1, 100, 10)
adil_per_win = st.sidebar.number_input("1위 시 획득 코인수", value=100)
market_price = st.sidebar.number_input("현재 코인 시세 ($)", value=0.4)

st.sidebar.header("👥 조직 복제")
pa_p = st.sidebar.selectbox("파트너 패키지", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("1대 인원", value=2)
dup = st.sidebar.radio("복제 인원", [2, 3])
f_pr = st.sidebar.slider("장래 예상 가격 ($)", 0.1, 10.0, 1.0)

# --- 계산 로직 ---
# 1. 게임 및 지출 계산
g_up = 20 if game_t == "$20" else 40
g_cv_val = 0.6 if game_t == "$20" else 1.2
my_total_game_cost = my_gc * g_up # 내가 실제로 게임에 쓴 돈

# 2. ADIL 코인 획득 분석
expected_wins = (my_gc * win_rate) / 100 # 예상 1위 횟수
total_my_adil = expected_wins * adil_per_win # 내가 획득한 총 코인
# 실질 취득 단가 = 내가 쓴 게임비 / 획득 코인수
if total_my_adil > 0:
    my_token_price = my_total_game_cost / total_my_adil
else:
    my_token_price = 0
profit_per_token = market_price - my_token_price

# 3. 조직 수익 계산 (기존 로직)
lim = pkgs[my_p]["lim"]
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}
stats = {}
t_reg_cv = t_game_cv = t_uni_reg = t_uni_mon = 0
curr = l1

for i in range(1, 5):
    if i > 1: curr *= dup
    r_cv, g_cv_l = curr * pkgs[pa_p]["cv"], curr * (120 * g_cv_val)
    t_reg_cv += r_cv
    t_game_cv += g_cv_l
    r_rev = (r_cv * rates[i]) if i <= lim else 0
    m_rev = (g_cv_l * rates[i]) if i <= lim else 0
    stats[i] = {"cnt": curr, "rcv": r_cv, "gcv": g_cv_l, "r_r": r_rev, "m_r": m_rev}
    t_uni_reg += r_rev
    t_uni_mon += m_rev

total_p = sum([d["cnt"] for d in stats.values()])
w_rcv, w_gcv = t_reg_cv/2, t_game_cv/2
i_b_r, i_o_r = w_rcv * pkgs[my_p]["bin"], int(w_rcv//5460)*450
i_b_m, i_o_m = w_gcv * pkgs[my_p]["bin"], int(w_gcv//5460)*450

# --- 화면 출력 ---
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("총 인원", f"{total_p:,}명")
c2.metric("나의 월 게임비", f"${my_total_game_cost:,}")
c3.metric("예상 ADIL 획득", f"{total_my_adil:,.0f} 개")
c4.metric("코인당 취득가", f"${my_token_price:,.2f}")

st.subheader("📝 상세 분석 보고서")
tabs = st.tabs(["ADIL 효율 분석", "수익 요약", "유니레벨 상세", "지출 상세"])

with tabs[0]:
    st.write("### 🪙 ADIL 코인 획득 및 경제성 분석")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**획득 시나리오**\n- 총 게임수: {my_gc}회\n- 예상 1위 횟수 ({win_rate}%): {expected_wins:.1f}회\n- 총 획득 코인: {total_my_adil:,.0f} ADIL")
    with col2:
        st.success(f"**가격 경쟁력**\n- 게임 투자비: ${my_total_game_cost:,.0f}\n- 나의 코인 평단가: **${my_token_price:.3f}**\n- 현재 시세 대비 이득: **${profit_per_token:.3f}/개**")
    
    st.write(f"현재 시세({market_price}$) 기준으로 거래소에서 사는 것보다 **{((market_price-my_token_price)/market_price)*100:.1f}%** 더 저렴하게 확보하고 계십니다.")



with tabs[1]:
    st.write("### 💰 비즈니스 수익 요약")
    st.write(f"- **1회성 보너스 합계:** ${(i_b_r+i_o_r+t_uni_reg):,.1f}")
    st.write(f"- **월 연금 보너스 합계:** ${(i_b_m+i_o_m+t_uni_mon):,.1f}")
    st.write(f"- **장래 코인 자산 가치 (가격 ${f_pr} 가정):** ${(total_my_adil + (total_p * 1200)) * f_pr:,.0f}")

with tabs[2]:
    for i, d in stats.items():
        st.write(f"**{i}대**({d['cnt']}명): 등록 보너스 ${d['r_r']:,.1f} / 매달 연금 ${d['m_r']:,.1f}")

with tabs[3]:
    st.write(f"**초기 투자:** 패키지 ${pkgs[my_p]['price']} + 알파 $60 = **${pkgs[my_p]['price']+60}**")
    st.write(f"**월 고정비:** 게임비 ${my_total_game_cost} + 구독료 ${pkgs[my_p]['sub']} = **${my_total_game_cost+pkgs[my_p]['sub']}**")
