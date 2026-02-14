import streamlit as st

st.set_page_config(page_title="DHP 수익계산기", layout="wide")
st.title("🚀 DHP비지니스 종합 수익 시뮬레이터")

# 데이터 정의
pkgs = {
    "Basic": {"price": 150, "cv": 72, "bin": 0.05, "sub": 30, "lim": 2},
    "Standard": {"price": 450, "cv": 216, "bin": 0.06, "sub": 30, "lim": 3},
    "Premium": {"price": 1050, "cv": 504, "bin": 0.07, "sub": 0, "lim": 4},
    "Ultimate": {"price": 2250, "cv": 1080, "bin": 0.08, "sub": 0, "lim": 5}
}

# 입력창
st.sidebar.header("📌 설정")
my_p = st.sidebar.selectbox("내 패키지", list(pkgs.keys()), index=2)
game_t = st.sidebar.selectbox("게임 선택", ["$20", "$40"])
my_gc = st.sidebar.number_input("내 게임수", value=120)
pa_p = st.sidebar.selectbox("파트너 패키지", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("1대 인원", value=2)
dup = st.sidebar.radio("복제 인원", [2, 3])
f_pr = st.sidebar.slider("예상 코인가격($)", 0.1, 10.0, 1.0)

# 계산
g_up = 20 if game_t == "$20" else 40
g_cv = 0.6 if game_t == "$20" else 1.2
m_g_cv = 120 * g_cv
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}
lim = pkgs[my_p]["lim"]

stats = {}
t_reg_cv = t_game_cv = t_uni_reg = t_uni_mon = 0
curr = l1

for i in range(1, 5):
    if i > 1: curr *= dup
    r_cv, g_cv_l = curr * pkgs[pa_p]["cv"], curr * m_g_cv
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
t_adil = total_p * 120 * 10

# 출력
st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("총 인원", f"{total_p:,}명")
c2.metric("나의 총 지출", f"${(pkgs[my_p]['price']+60+my_gc*g_up+pkgs[my_p]['sub']):,.0f}")
c3.metric("1회성 수익", f"${(i_b_r+i_o_r+t_uni_reg):,.1f}")
c4.metric("월 연금 수익", f"${(i_b_m+i_o_m+t_uni_mon):,.1f}")

tabs = st.tabs(["CV 내역", "유니레벨", "바이너리/오빗", "ADIL 코인", "지출상세"])
with tabs[0]:
    st.write("**등록 CV 합계:**", f"{t_reg_cv:,.0f}", "/ **게임 CV 합계:**", f"{t_game_cv:,.0f}")
    for i, d in stats.items(): st.write(f"{i}대({d['cnt']}명): 등록{d['rcv']:,.0f} / 게임{d['gcv']:,.0f} CV")
with tabs[1]:
    for i, d in stats.items(): st.write(f"**{i}대**({'✅' if i<=lim else '❌'}): 등록 ${d['r_r']:,.1f} / 게임 ${d['m_r']:,.1f}")
with tabs[2]:
    st.write(f"**1회성:** 바이너리 ${i_b_r:,.1f}, 오빗 ${i_o_r:,.0f} (소실적 {w_rcv:,.0f}CV)")
    st.write(f"**매달:** 바이너리 ${i_b_m:,.1f}, 오빗 ${i_o_m:,.0f} (소실적 {w_gcv:,.0f}CV)")
with tabs[3]:
    st.metric("월 획득 코인", f"{t_adil:,.0f} ADIL")
    st.info(f"가격 ${f_pr}일 때 가치: ${t_adil*f_pr:,.0f}")
with tabs[4]:
    st.write(f"**초기:** 패키지 ${pkgs[my_p]['price']} + 알파 $60 = **${pkgs[my_p]['price']+60}**")
    st.write(f"**월간:** 게임 ${my_gc*g_up} + 구독 ${pkgs[my_p]['sub']} = **${my_gc*g_up+pkgs[my_p]['sub']}**")
