import streamlit as st

st.set_page_config(page_title="DHP 수익 시뮬레이터", layout="wide")
st.title("🚀 DHP 비지니스 수익 상세 분석")
st.write("등록 보너스와 매달 연금 보너스를 구분하여 정밀 분석합니다.")

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
g_up = 20 if game_t == "$20" else 40
g_cv_val = 0.6 if game_t == "$20" else 1.2
m_g_cv = 120 * g_cv_val 
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}
lim = pkgs[my_p]["lim"]

stats = {}
t_reg_cv = t_game_cv = t_uni_reg = t_uni_mon = 0
curr = l1

# 4레벨 복제 및 유니레벨 계산
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
c2.metric("나의 월 지출", f"${(my_gc*g_up + pkgs[my_p]['sub']):,.0f}")
c3.metric("총 등록 보너스", f"${(i_bin_reg + i_orbit_reg + t_uni_reg):,.1f}")
c4.metric("총 월간 보너스", f"${(i_bin_mon + i_orbit_mon + t_uni_mon):,.1f}")

# 메인 분석 탭
tabs = st.tabs(["💰 1회성 등록 보너스", "📅 매달 연금 보너스", "🎯 ADIL 효율/확률", "💳 지출 상세"])

with tabs[0]:
    st.subheader("초기 패키지 등록 수익 상세")
    col1, col2, col3 = st.columns(3)
    col1.metric("유니레벨(등록)", f"${t_uni_reg:,.1f}")
    col2.metric("바이너리(등록)", f"${i_bin_reg:,.1f}")
    col3.metric("오빗(등록)", f"${i_orbit_reg:,.0f}")
    
    st.write("---")
    st.write("**레벨별 유니레벨(등록) 내역**")
    for i, d in stats.items():
        st.write(f"- {i}대 ({d['cnt']}명): {d['rcv']:,.0f} CV × {int(rates[i]*100)}% = ${d['r_r']:,.1f}")

with tabs[1]:
    st.subheader("월간 게임 활동 연금 수익 상세")
    col1, col2, col3 = st.columns(3)
    col1.metric("유니레벨(연금)", f"${t_uni_mon:,.1f}")
    col2.metric("바이너리(연금)", f"${i_bin_mon:,.1f}")
    col3.metric("오빗(연금)", f"${i_orbit_mon:,.0f}")
    
    st.write("---")
    st.write("**레벨별 유니레벨(연금) 내역**")
    for i, d in stats.items():
        st.write(f"- {i}대 ({d['cnt']}명): {d['gcv']:,.0f} CV × {int(rates[i]*100)}% = ${d['m_r']:,.1f}")

with tabs[2]:
    win_p = 0.0625
    exp_wins = my_gc * win_p
    at_least_p = (1 - (1 - win_p)**my_gc) * 100
    total_adil = exp_wins * 100
    t_price = (my_gc * g_up) / total_adil if total_adil > 0 else 0
    
    st.write("### 🎯 ADIL 획득 확률 및 경제성")
    st.info(f"한 달({my_gc}판) 게임 시 예상 1위 횟수는 **{exp_wins:.2f}회** 이며, 최소 1번 이상 당첨될 확률은 **{at_least_p:.2f}%** 입니다.")
    st.success(f"나의 코인 평단가: **${t_price:.3f}** (게임비 지출 기준)")

with tabs[3]:
    st.write("### 💳 지출 비용 요약")
    st.write(f"**초기 비용:** 패키지 ${pkgs[my_p]['price']} + 알파 $60 = **${pkgs[my_p]['price']+60}**")
    st.write(f"**월 고정비:** 게임비 ${my_gc*g_up} + 구독료 ${pkgs[my_p]['sub']} = **${my_gc*g_up+pkgs[my_p]['sub']}**")
