import streamlit as st

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 종합 수익 및 경제성 분석")

# 1. 데이터 정의
pkgs = {
    "Basic": {"price": 150, "cv": 72, "bin": 0.05, "sub": 30, "lim": 2},
    "Standard": {"price": 450, "cv": 216, "bin": 0.06, "sub": 30, "lim": 3},
    "Premium": {"price": 1050, "cv": 504, "bin": 0.07, "sub": 0, "lim": 4},
    "Ultimate": {"price": 2250, "cv": 1080, "bin": 0.08, "sub": 0, "lim": 5}
}

# --- 사이드바 설정 ---
st.sidebar.header("📌 설정")
my_p = st.sidebar.selectbox("내 패키지 등급", list(pkgs.keys()), index=2)
game_t = st.sidebar.selectbox("게임 상품", ["$20", "$40"], index=0)
my_gc = st.sidebar.number_input("나의 월 게임수", value=120)

st.sidebar.header("👥 조직 복제")
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("1대 직접소개 인원", value=2)
dup = st.sidebar.radio("하위 복제 인원 (2~4대)", [2, 3])

# --- 계산 로직 ---
# A. 지출 계산
init_cost = pkgs[my_p]["price"] + 60 # 패키지 + 알파스테이지
monthly_game_price = 20 if game_t == "$20" else 40
monthly_cost = (my_gc * monthly_game_price) + pkgs[my_p]["sub"]

# B. CV 상세 정의
reg_cv_per_person = pkgs[pa_p]["cv"]
# 산하 1명이 1게임 할 때 올라오는 CV (월 120판 기준 0.6cv 또는 1.2cv를 120으로 나눔)
cv_per_single_game = (0.6 if game_t == "$20" else 1.2) / 120
game_cv_per_person_month = 120 * cv_per_single_game

# C. 조직 수익 계산
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

# 바이너리 & 오빗
w_rcv, w_gcv = t_reg_cv / 2, t_game_cv / 2
i_bin_reg = w_rcv * pkgs[my_p]["bin"]
i_orbit_reg = int(w_rcv // 5460) * 450
i_bin_mon = w_gcv * pkgs[my_p]["bin"]
i_orbit_mon = int(w_gcv // 5460) * 450

total_reg_bonus = i_bin_reg + i_orbit_reg + t_uni_reg
total_mon_bonus = i_bin_mon + i_orbit_mon + t_uni_mon

# ADIL 계산
win_rate = 0.0625
exp_wins = my_gc * win_rate
total_adil = exp_wins * 75
adil_val = total_adil * 0.4

# --- 화면 출력 (메인 메뉴) ---
st.divider()
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("초기 비용", f"${init_cost:,}")
c2.metric("나의 월 지출", f"${monthly_cost:,.0f}")
c3.metric("등록 보너스", f"${total_reg_bonus:,.1f}")
c4.metric("월 연금 수익", f"${total_mon_bonus:,.1f}")
# 최종 결과값 (월 지출 대비 보너스 + 코인가치 합산 결과)
net_monthly = total_mon_bonus + adil_val - monthly_cost
c5.metric("월 순수익(ADIL포함)", f"${net_monthly:,.1f}", delta=f"{((total_mon_bonus+adil_val)/monthly_cost*100):,.1f}% ROI")

tabs = st.tabs(["💰 1회성 등록 상세", "📅 매달 연금 상세", "🎯 ADIL 경제성", "💳 최종 지출/수익 결과"])

with tabs[0]:
    st.subheader("📁 전체 등록 CV 상세 내역")
    st.info(f"**총 등록 CV: {t_reg_cv:,.0f} CV** (산하 인원 {sum([d['cnt'] for d in stats.values()]):,}명 × 인당 {reg_cv_per_person} CV)")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**[레벨별 CV 구성]**")
        for i, d in stats.items():
            st.write(f"- {i}대 ({d['cnt']}명): {d['rcv']:,.0f} CV")
    with col_b:
        st.write("**[수익 배분]**")
        st.write(f"- 유니레벨 합계: ${t_uni_reg:,.1f}")
        st.write(f"- 바이너리(소실적 {w_rcv:,.0f}CV): ${i_bin_reg:,.1f}")
        st.write(f"- 오빗({int(w_rcv//5460)}회전): ${i_orbit_reg:,.0f}")

with tabs[1]:
    st.subheader("📅 월간 게임 CV 및 연금 상세")
    st.success(f"💡 **비전 포인트:** 산하 조직원 1명이 1게임을 할 때 나에게 **{cv_per_single_game:.4f} CV**가 실시간 적립됩니다.")
    st.write(f"(1명이 월 120판 플레이 시 나에게 총 **{game_cv_per_person_month:.1f} CV** 누적)")
    
    col_c, col_d = st.columns(2)
    with col_c:
        st.write("**[월간 발생 CV]**")
        for i, d in stats.items():
            st.write(f"- {i}대 ({d['cnt']}명): {d['gcv']:,.1f} CV")
    with col_d:
        st.write("**[수익 배분]**")
        st.write(f"- 유니레벨 합계: ${t_uni_mon:,.1f}")
        st.write(f"- 바이너리(소실적 {w_gcv:,.0f}CV): ${i_bin_mon:,.1f}")
        st.write(f"- 오빗({int(w_gcv//5460)}회전): ${i_orbit_mon:,.0f}")

with tabs[2]:
    st.subheader("🎯 ADIL 코인 획득 분석")
    st.write(f"나의 월 게임 {my_gc}회 중 통계적 승리 횟수: **{exp_wins:.1f}회**")
    st.write(f"획득 ADIL: {exp_wins:.1f}회 × 75개 = **{total_adil:,.1f} ADIL**")
    st.write(f"시세 $0.4 적용 시 가치: **${adil_val:.1f}**")
    st.info(f"👉 게임비 ${my_gc*monthly_game_price} 중 약 {adil_val/ (my_gc*monthly_game_price)*100:.1f}%를 코인으로 환급받는 효과")

with tabs[3]:
    st.subheader("📊 지출 대비 보너스 최종 결과 (ROI)")
    col_f, col_g = st.columns(2)
    with col_f:
        st.write("**[총 지출 내역]**")
        st.write(f"- 초기 비용: ${init_cost:,.0f}")
        st.write(f"- 월 유지비: ${monthly_cost:,.0f}")
    with col_g:
        st.write("**[월 예상 총 수익]**")
        st.write(f"- 현금성 보너스: ${total_mon_bonus:,.1f}")
        st.write(f"- ADIL 코인 가치: ${adil_val:,.1f}")
        st.markdown(f"### **합계: ${(total_mon_bonus + adil_val):,.1f}**")
    
    st.divider()
    final_roi = ((total_mon_bonus + adil_val) / monthly_cost) * 100
    if final_roi >= 100:
        st.balloons()
        st.success(f"✅ **수익 분석 결과:** 월 지출 대비 **{final_roi:.1f}%**의 수익이 발생합니다. (매달 ${net_monthly:,.1f} 순수익)")
    else:
        st.warning(f"⚠️ **수익 분석 결과:** 월 지출 대비 수익률은 {final_roi:.1f}%입니다.")
