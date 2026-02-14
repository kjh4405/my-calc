import streamlit as st

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 종합 수익 분석 (최종 로직)")

# 1. 데이터 정의 (패키지별 등록 CV 및 요율)
pkgs = {
    "Basic": {"price": 150, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 450, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1050, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2250, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 5}
}

# --- 사이드바 설정 ---
st.sidebar.header("📌 나의 설정")
my_p = st.sidebar.selectbox("내 패키지 등급", list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input("나의 월 게임수 (120단위)", value=120, min_value=120, step=120)

st.sidebar.header("👥 조직 복제 설정")
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("1대 직접소개 인원", value=2, min_value=1)
dup = st.sidebar.radio("하위 복제 인원 (2~4대)", [2, 3], index=0)

# --- 계산 로직 ---

# A. 나의 월 지출 ($110.25 고정 로직)
base_game_cost = (my_gc / 120) * 110.25 
# 나의 자가 CV 충족 여부 (Premium 이상 120판 시 72 CV / 이하는 36 CV)
my_gen_cv = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0.0, 72.0 - my_gen_cv)
shortfall_fee = cv_shortfall * 2.0 
total_monthly_exp = base_game_cost + shortfall_fee
init_cost = pkgs[my_p]["price"] + 60

# B. 수익 계산
# 파트너 등급에 따른 등록 CV 및 게임 CV 결정
p_reg_cv_value = pkgs[pa_p]["reg_cv"] # 등록 보너스용 (패키지 CV)
p_game_cv_value = 72.0 if pkgs[pa_p]["self_rate"] == 0.03 else 36.0 # 연금 보너스용 (120판 기준)

rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}
lim = pkgs[my_p]["lim"]

stats = {}
t_reg_cv = t_game_cv = t_uni_reg = t_uni_mon = total_people = 0
curr = l1

for i in range(1, 5):
    if i > 1: curr *= dup
    total_people += curr
    
    # 1. 등록 보너스 (인당 패키지 CV 적용)
    r_cv = curr * p_reg_cv_value
    # 2. 연금 보너스 (인당 게임 발생 CV 적용)
    g_cv = curr * (my_gc / 120 * p_game_cv_value)
    
    t_reg_cv += r_cv
    t_game_cv += g_cv
    
    r_rev = (r_cv * rates[i]) if i <= lim else 0
    m_rev = (g_cv * rates[i]) if i <= lim else 0
    
    stats[i] = {"cnt": curr, "rcv": r_cv, "gcv": g_cv, "r_r": r_rev, "m_r": m_rev, "rate": rates[i]}
    t_uni_reg += r_rev
    t_uni_mon += m_rev

# 바이너리/오빗 (연금형)
w_gcv = t_game_cv / 2
i_bin_m = w_gcv * pkgs[my_p]["bin"]
i_orb_m = int(w_gcv // 5460) * 450
total_mon_bonus = t_uni_mon + i_bin_m + i_orb_m

# ADIL 가치
total_adil = (my_gc / 120) * 562.5
adil_val = total_adil * 0.4

# --- 화면 출력 ---
st.divider()
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("총 산하 인원", f"{total_people:,}명")
m2.metric("초기 비용", f"${init_cost:,}")
m3.metric("나의 월 지출", f"${total_monthly_exp:,.2f}")
# 등록 보너스 총합 (유니레벨 + 바이너리 + 오빗)
t_reg_total = t_uni_reg + (t_reg_cv/2 * pkgs[my_p]['bin']) + int(t_reg_cv/2//5460)*450
m4.metric("총 등록 보너스", f"${t_reg_total:,.0f}")
m5.metric("월 연금 수익", f"${total_mon_bonus:,.1f}")
m6.metric("월 순수익(현금)", f"${total_mon_bonus - total_monthly_exp:,.1f}")

tabs = st.tabs(["💰 등록 보너스 상세", "📅 연금 보너스 상세", "🎯 ADIL 및 자가 CV", "⚖️ 바이너리/오빗 근거"])

with tabs[0]:
    st.subheader("💰 1회성 등록 보너스 산출 근거")
    st.write(f"파트너 {pa_p} 등급 기준: 인당 **{p_reg_cv_value} CV** 적용")
    header = st.columns([1, 1, 2, 2])
    header[0].write("**단계**")
    header[1].write("**인원**")
    header[2].write("**합계 등록 CV**")
    header[3].write("**수령 보너스 (유니)**")
    for i, d in stats.items():
        cols = st.columns([1, 1, 2, 2])
        cols[0].write(f"{i}대 " + ("✅" if i <= lim else "❌"))
        cols[1].write(f"{d['cnt']:,}명")
        cols[2].write(f"{d['rcv']:,.0f} CV")
        cols[3].write(f"${d['r_r']:,.1f}")

with tabs[1]:
    st.subheader("📅 월간 연금 보너스 산출 근거")
    st.write(f"파트너 {pa_p} 등급의 월 120판 발생 CV: **{p_game_cv_value} CV** 적용")
    header2 = st.columns([1, 1, 2, 2])
    header2[0].write("**단계**")
    header2[1].write("**인원**")
    header2[2].write("**합계 게임 CV**")
    header2[3].write("**수령 보너스 (유니)**")
    for i, d in stats.items():
        cols = st.columns([1, 1, 2, 2])
        cols[0].write(f"{i}대 " + ("✅" if i <= lim else "❌"))
        cols[1].write(f"{d['cnt']:,}명")
        cols[2].write(f"{d['gcv']:,.1f} CV")
        cols[3].write(f"${d['m_r']:,.1f}")

with tabs[2]:
    st.subheader("🎯 ADIL 및 자격 충족(72 CV)")
    st.write(f"- 월 {my_gc}회 게임 시 예상 ADIL: **{total_adil:,.1f}개** (가치 ${adil_val:,.1f})")
    st.divider()
    st.write(f"**자가 CV 현황:** 발생 {my_gen_cv:.1f} CV / 기준 72.0 CV")
    if cv_shortfall > 0:
        st.warning(f"⚠️ 부족분 {cv_shortfall:.1f} CV에 대해 ${shortfall_fee} 추가 구독료 발생")
    else:
        st.success("✅ 자가 CV 충족 완료")

with tabs[3]:
    st.subheader("⚖️ 바이너리 & 오빗 상세 내역")
    c_a, c_b = st.columns(2)
    with c_a:
        st.write("**[1회성 등록 기준]**")
        st.write(f"- 전체 등록 CV: {t_reg_cv:,.0f}")
        st.write(f"- 소실적 바이너리: ${t_reg_cv/2 * pkgs[my_p]['bin']:,.1f}")
    with c_b:
        st.write("**[매달 연금 기준]**")
        st.write(f"- 전체 게임 CV: {t_game_cv:,.1f}")
        st.write(f"- 소실적 바이너리: ${i_bin_m:,.1f}")
        st.write(f"- 오빗({int(w_gcv//5460)}회전): ${i_orb_m:,.0f}")
