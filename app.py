import streamlit as st

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 종합 수익 분석 (최종 로직 반영)")

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
my_gc = st.sidebar.number_input("나의 월 게임수 (120단위)", value=120, min_value=120, step=120)

st.sidebar.header("👥 조직 복제 설정")
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("1대 직접소개 인원", value=2, min_value=1)
dup = st.sidebar.radio("하위 복제 인원 (2~4대)", [2, 3], index=0)

# --- 계산 로직 ---

# A. 나의 월 지출 (이자 차감 후 $110.25 기준)
base_game_cost = (my_gc / 120) * 110.25 
# 자가 CV 부족분 계산 (72 CV 기준)
my_gen_cv = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0.0, 72.0 - my_gen_cv)
shortfall_fee = cv_shortfall * 2.0 

total_monthly_exp = base_game_cost + shortfall_fee
init_cost = pkgs[my_p]["price"] + 60

# B. 조직 수익 및 인원수 계산
reg_cv_p = pkgs[pa_p]["cv"]
# 산하 인원 1명이 월 120판 플레이 시 발생하는 CV = 72 CV (고정)
game_cv_p = (my_gc / 120) * 72.0 

rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}
lim = pkgs[my_p]["lim"]

stats = {}
t_reg_cv = t_game_cv = t_uni_reg = t_uni_mon = total_people = 0
curr = l1

for i in range(1, 5):
    if i > 1:
        curr *= dup
    
    total_people += curr
    r_cv = curr * reg_cv_p
    g_cv = curr * game_cv_p
    
    t_reg_cv += r_cv
    t_game_cv += g_cv
    
    # 유니레벨 수익 (내 등급 제한 적용)
    r_r = (r_cv * rates[i]) if i <= lim else 0
    m_r = (g_cv * rates[i]) if i <= lim else 0
    
    stats[i] = {"cnt": curr, "rcv": r_cv, "gcv": g_cv, "r_r": r_r, "m_r": m_r, "rate": rates[i]}
    t_uni_reg += r_r
    t_uni_mon += m_r

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
# 메인 지표 6칸으로 확장
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("총 산하 인원", f"{total_people:,}명")
m2.metric("초기 비용", f"${init_cost:,}")
m3.metric("나의 월 지출", f"${total_monthly_exp:,.2f}")
m4.metric("등록 보너스", f"${(t_uni_reg + (t_reg_cv/2 * pkgs[my_p]['bin']) + int(t_reg_cv/2//5460)*450):,.0f}")
m5.metric("월 연금 수익", f"${total_mon_bonus:,.1f}")
# 월 순수익 (ADIL 불포함)
net_cash = total_mon_bonus - total_monthly_exp
m6.metric("월 순수익(현금)", f"${net_cash:,.1f}", delta=f"ROI {int((total_mon_bonus/total_monthly_exp)*100)}%")

tabs = st.tabs(["💎 유니레벨 상세", "⚖️ 바이너리/오빗 근거", "🎯 ADIL 및 자가 CV", "💳 지출/이자 상세"])

with tabs[0]:
    st.subheader("💎 단계별 유니레벨 보너스 산출 근거")
    st.write(f"현재 내 등급({my_p}) 수령 제한: **{lim}대까지**")
    
    # 테이블 형태로 깔끔하게 표시
    header = st.columns([1, 1, 2, 1, 2])
    header[0].write("**단계**")
    header[1].write("**인원수**")
    header[2].write("**합계 CV (인당 72)**")
    header[3].write("**요율**")
    header[4].write("**월 수익(현금)**")
    
    for i, d in stats.items():
        cols = st.columns([1, 1, 2, 1, 2])
        is_limited = i > lim
        cols[0].write(f"{i}대 " + ("❌" if is_limited else "✅"))
        cols[1].write(f"{d['cnt']:,}명")
        cols[2].write(f"{d['gcv']:,.1f} CV")
        cols[3].write(f"{int(d['rate']*100)}%")
        cols[4].write(f"**${d['m_r']:,.1f}**")
    st.divider()
    st.write(f"**유니레벨 연금 합계: ${t_uni_mon:,.1f}**")

with tabs[1]:
    st.subheader("⚖️ 바이너리 및 오빗 보너스 (연금형)")
    st.write("모든 조직원이 월 120판(72 CV 발생)을 한다는 가정하에 산출된 실적입니다.")
    c_a, c_b = st.columns(2)
    with c_a:
        st.info(f"**실적 분석**\n- 전체 게임 CV: {t_game_cv:,.1f}\n- 소실적 CV (50%): {w_gcv:,.1f}")
    with c_b:
        st.success(f"**수익 분석**\n- 바이너리({int(pkgs[my_p]['bin']*100)}%): ${i_bin_m:,.1f}\n- 오빗({int(w_gcv//5460)}회전): ${i_orb_m:,.0f}")

with tabs[2]:
    st.subheader("🎯 ADIL 코인 및 자가 CV 충족 현황")
    st.write(f"- 월 {my_gc}회 게임 시 예상 ADIL: **{total_adil:,.1f}개** (가치 ${adil_val:,.1f})")
    st.divider()
    st.write(f"- 내 게임으로 발생한 CV: **{my_gen_cv:.1f} CV** / 필수 기준: **72.0 CV**")
    if cv_shortfall > 0:
        st.warning(f"⚠️ 부족분 {cv_shortfall:.1f} CV에 대해 **${shortfall_fee}**의 추가 구독료가 지출에 포함되었습니다.")
    else:
        st.success("✅ 필수 CV를 충족하여 추가 구독료가 발생하지 않습니다.")

with tabs[3]:
    st.subheader("💳 지출 및 이자수익 상세 ($110.25 근거)")
    st.write("나의 120판 게임 시 발생하는 실질 비용 계산:")
    st.write("- 1위(7.5회) 비용: $150.00")
    st.write("- 2위(7.5회) 이자수익(4%): -$6.00")
    st.write("- 3~16위(105회) 이자수익(1.5%): -$33.75")
    st.markdown(f"### **실질 게임 지출액: ${base_game_cost:,.2f}**")
    st.caption("※ 240판 플레이 시 위 금액의 2배가 적용됩니다.")
