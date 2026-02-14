import streamlit as st

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 종합 수익 분석 (로직 업데이트)")

# 1. 데이터 정의 (패키지별 자가 CV 요율 추가)
pkgs = {
    "Basic": {"price": 150, "cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 450, "cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1050, "cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2250, "cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 5}
}

# --- 사이드바 설정 ---
st.sidebar.header("📌 나의 설정")
my_p = st.sidebar.selectbox("내 패키지 등급", list(pkgs.keys()), index=2)
# 최소 게임수를 120개로 고정
my_gc = st.sidebar.number_input("나의 월 게임수 (최소 120회 권장)", value=120, min_value=120, step=120)

st.sidebar.header("👥 조직 복제")
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("1대 직접소개 인원", value=2)
dup = st.sidebar.radio("하위 복제 인원 (2~4대)", [2, 3])

# --- 계산 로직 ---

# A. 나의 월 지출 계산 (사용자 정의 로직)
# 120게임 기준 1위(7.5회) 비용 $150 - (2위 이자 $6 + 3~16위 이자 $33.75) = $110.25
base_game_cost = (my_gc / 120) * 110.25 

# 자가 CV 계산 및 부족분(Shortfall) 계산
# Premium/Ultimate는 120판 시 72CV 달성 / Basic/Standard는 36CV 달성
my_generated_cv = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0, 72 - my_generated_cv)
shortfall_fee = cv_shortfall * 2 # 부족한 1CV당 2달러 과금 로직 (36CV 부족 시 72달러)

total_monthly_expenditure = base_game_cost + shortfall_fee

# B. 조직 수익 계산 (기존 동일)
reg_cv_per_person = pkgs[pa_p]["cv"]
cv_per_single_game = (0.6) / 120 # 20달러 게임 기준 산하에서 올라오는 CV
game_cv_per_person_month = 120 * cv_per_single_game

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

w_rcv, w_gcv = t_reg_cv / 2, t_game_cv / 2
i_bin_reg = w_rcv * pkgs[my_p]["bin"]
i_orbit_reg = int(w_rcv // 5460) * 450
i_bin_mon = w_gcv * pkgs[my_p]["bin"]
i_orbit_mon = int(w_gcv // 5460) * 450

total_reg_bonus = i_bin_reg + i_orbit_reg + t_uni_reg
total_mon_bonus = i_bin_mon + i_orbit_mon + t_uni_mon

# ADIL 계산 (120판 기준 7.5회 승리 -> 562.5개)
total_adil = (my_gc / 120) * 562.5
adil_val = total_adil * 0.4

# --- 화면 출력 ---
st.divider()
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("초기 비용", f"${pkgs[my_p]['price'] + 60:,}")
c2.metric("나의 월 지출", f"${total_monthly_expenditure:,.2f}")
c3.metric("등록 보너스", f"${total_reg_bonus:,.1f}")
c4.metric("월 연금 수익", f"${total_mon_bonus:,.1f}")

# 월 순수익 (ADIL 불포함)
net_cash_profit = total_mon_bonus - total_monthly_expenditure
c5.metric("월 순수익(ADIL불포함)", f"${net_cash_profit:,.1f}", delta_color="normal")

tabs = st.tabs(["💰 등록/연금 상세", "🎯 ADIL 및 자가CV 분석", "💳 지출/이자 상세"])

with tabs[0]:
    col_reg, col_mon = st.columns(2)
    with col_reg:
        st.subheader("1회성 등록 보너스")
        st.write(f"- 유니레벨: ${t_uni_reg:,.1f}")
        st.write(f"- 바이너리: ${i_bin_reg:,.1f}")
        st.write(f"- 오빗: ${i_orbit_reg:,.0f}")
    with col_mon:
        st.subheader("매달 연금 보너스")
        st.write(f"- 유니레벨: ${t_uni_mon:,.1f}")
        st.write(f"- 바이너리: ${i_bin_mon:,.1f}")
        st.write(f"- 오빗: ${i_orbit_mon:,.0f}")

with tabs[1]:
    st.subheader("🎯 ADIL 코인 및 자가 CV 분석")
    st.info(f"**ADIL 획득:** {my_gc}회 게임 시 통계적으로 **{total_adil:,.1f}개**의 ADIL을 획득합니다. (시세 $0.4 기준 가치: ${adil_val:,.1f})")
    
    st.write("---")
    st.subheader("💡 자가 발생 CV 및 추가 구독료")
    st.write(f"- 현재 패키지 등급 자가 CV 요율: **{pkgs[my_p]['self_rate']*100:.1;f}%**")
    st.write(f"- {my_gc}회 게임 시 발생 CV: **{my_generated_cv:.1f} CV**")
    if cv_shortfall > 0:
        st.warning(f"⚠️ 필수 72 CV에 대해 **{cv_shortfall:.1f} CV**가 부족하여 **${shortfall_fee}**의 추가 비용이 발생했습니다.")
    else:
        st.success(f"✅ 필수 72 CV를 달성하여 추가 비용이 없습니다.")

with tabs[2]:
    st.subheader("💳 지출 및 이자수익 상세 (120판 기준)")
    st.write(f"1. 1위 당첨(7.5회) 게임비: $150")
    st.write(f"2. 2위(7.5회) 이자 수익(4%): -$6.00")
    st.write(f"3. 3~16위(105회) 이자 수익(1.5%): -$33.75")
    st.markdown(f"### **실질 월 게임 지출: ${base_game_cost:,.2f}**")
    st.write(f"(여기에 자가 CV 부족 시 추가 구독료가 합산됩니다.)")
