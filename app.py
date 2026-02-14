import streamlit as st

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 종합 수익 분석 (수정본)")

# 1. 데이터 정의
pkgs = {
    "Basic": {"price": 150, "cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 450, "cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1050, "cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2250, "cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 5}
}

# --- 사이드바 설정 ---
st.sidebar.header("📌 나의 설정")
my_p = st.sidebar.selectbox("내 패키지 등급", list(pkgs.keys()), index=2)
# 최소 120게임 단위로 선택 가능
my_gc = st.sidebar.number_input("나의 월 게임수 (120단위 추천)", value=120, min_value=120, step=120)

st.sidebar.header("👥 조직 복제")
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("1대 직접소개 인원", value=2)
dup = st.sidebar.radio("하위 복제 인원 (2~4대)", [2, 3])

# --- 계산 로직 ---

# A. 나의 월 지출 (120판 기준 실질 지출 $110.25 고정)
base_game_cost = (my_gc / 120) * 110.25 

# 자가 CV 충족 여부 계산 (72 CV 기준)
# Basic/Standard는 게임비($20)의 1.5% = 0.3 CV/판
# Premium/Ultimate는 게임비($20)의 3% = 0.6 CV/판
my_gen_cv = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0.0, 72.0 - my_gen_cv)
shortfall_fee = cv_shortfall * 2.0 # 부족한 1 CV당 2달러 과금

total_monthly_exp = base_game_cost + shortfall_fee
init_cost = pkgs[my_p]["price"] + 60

# B. 조직 수익 (연금형)
reg_cv_p = pkgs[pa_p]["cv"]
game_cv_p = 120 * (0.6) # 산하 1인당 월간 고정 72 CV 발생 가정

rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}
lim = pkgs[my_p]["lim"]
stats = {}
t_reg_cv = t_game_cv = t_uni_reg = t_uni_mon = 0
curr = l1

for i in range(1, 5):
    if i > 1: curr *= dup
    r_cv = curr * reg_cv_p
    g_cv = curr * game_cv_p
    t_reg_cv += r_cv
    t_game_cv += g_cv
    
    r_r = (r_cv * rates[i]) if i <= lim else 0
    m_r = (g_cv * rates[i]) if i <= lim else 0
    stats[i] = {"cnt": curr, "rcv": r_cv, "gcv": g_cv, "r_r": r_r, "m_r": m_r}
    t_uni_reg += r_r
    t_uni_mon += m_r

# 바이너리/오빗
w_rcv, w_gcv = t_reg_cv / 2, t_game_cv / 2
i_bin_m = w_gcv * pkgs[my_p]["bin"]
i_orb_m = int(w_gcv // 5460) * 450
total_mon_bonus = t_uni_mon + i_bin_m + i_orb_m

# ADIL (120판당 562.5개)
total_adil = (my_gc / 120) * 562.5
adil_val = total_adil * 0.4

# --- 화면 출력 ---
st.divider()
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("초기 비용", f"${init_cost:,}")
c2.metric("나의 월 지출", f"${total_monthly_exp:,.2f}")
c3.metric("등록 보너스", f"${(t_uni_reg + (w_rcv * pkgs[my_p]['bin']) + int(w_rcv//5460)*450):,.1f}")
c4.metric("월 연금 수익", f"${total_mon_bonus:,.1f}")

# 월 순수익 (ADIL 불포함)
net_cash = total_mon_bonus - total_monthly_exp
c5.metric("월 순수익(현금)", f"${net_cash:,.1f}")

tabs = st.tabs(["📊 수익/지출 요약", "🎯 ADIL 및 자가 CV", "⚖️ 바이너리/오빗 근거"])

with tabs[0]:
    st.subheader("💳 지출 대비 현금 흐름 분석")
    col_x, col_y = st.columns(2)
    with col_x:
        st.write("**[월간 고정 지출 내역]**")
        st.write(f"- 실질 게임비 (이자 차감): ${base_game_cost:,.2f}")
        st.write(f"- 자가 CV 부족분 구독료: ${shortfall_fee:,.1f}")
        st.markdown(f"**총 지출 합계: ${total_monthly_exp:,.2f}**")
    with col_y:
        st.write("**[월간 예상 현금 수익]**")
        st.write(f"- 유니레벨: ${t_uni_mon:,.1f}")
        st.write(f"- 바이너리: ${i_bin_m:,.1f}")
        st.write(f"- 오빗: ${i_orb_m:,.0f}")
        st.markdown(f"**총 수익 합계: ${total_mon_bonus:,.1f}**")

with tabs[1]:
    st.subheader("🎯 ADIL 코인 및 자가 CV 분석")
    st.info(f"**ADIL 획득:** {my_gc}회 게임 시 통계적으로 **{total_adil:,.1f}개**를 얻으며, 가치는 **${adil_val:,.1f}** 입니다.")
    
    st.divider()
    st.write(f"현재 패키지 요율: **{pkgs[my_p]['self_rate']*100:.1f}%**")
    st.write(f"현재 게임수로 발생한 CV: **{my_gen_cv:.1f} CV** / 필수 기준: **72.0 CV**")
    if cv_shortfall > 0:
        st.error(f"⚠️ {cv_shortfall:.1f} CV가 부족하여 **${shortfall_fee}**의 추가 구독료가 포함되었습니다.")
        st.caption("팁: 게임 수를 늘리면 추가 구독료를 줄일 수 있습니다.")
    else:
        st.success("✅ 필수 CV를 모두 충족하여 추가 구독료가 발생하지 않습니다.")

with tabs[2]:
    st.subheader("⚖️ 연금형 바이너리/오빗 산출 근거")
    st.write(f"- 산하 전체 게임 CV: {t_game_cv:,.1f} CV")
    st.write(f"- 소실적(50%) 기준: {w_gcv:,.1f} CV")
    st.write(f"- 바이너리({int(pkgs[my_p]['bin']*100)}%): ${i_bin_m:,.1f}")
    st.write(f"- 오빗({int(w_gcv//5460)}회전): ${i_orb_m:,.0f}")
