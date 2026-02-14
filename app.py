import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 종합 수익 분석 (통합 테이블 버전)")

# 1. 데이터 정의 (기존 로직 유지)
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

# --- 계산 로직 (모든 수식 보존) ---

# A. 나의 월 지출 ($110.25 고정 로직)
base_game_cost = (my_gc / 120) * 110.25 
my_gen_cv = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0.0, 72.0 - my_gen_cv)
shortfall_fee = cv_shortfall * 2.0 
total_monthly_exp = base_game_cost + shortfall_fee
init_cost = pkgs[my_p]["price"] + 60

# B. 수익 계산
p_reg_cv_value = pkgs[pa_p]["reg_cv"]
p_game_cv_value = 72.0 if pkgs[pa_p]["self_rate"] == 0.03 else 36.0

rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}
lim = pkgs[my_p]["lim"]
bin_rate = pkgs[my_p]["bin"]

stats = []
t_reg_cv = t_game_cv = total_people = 0
curr = l1

for i in range(1, 5):
    if i > 1: curr *= dup
    total_people += curr
    
    r_cv = curr * p_reg_cv_value
    g_cv = curr * (my_gc / 120 * p_game_cv_value)
    
    t_reg_cv += r_cv
    t_game_cv += g_cv
    
    # 수익 계산 (내 등급 제한 반영)
    is_qual = i <= lim
    u_reg = r_cv * rates[i] if is_qual else 0
    u_mon = g_cv * rates[i] if is_qual else 0
    
    # 바이너리/오빗은 합산 실적 기준이지만 가독성을 위해 단계별 기여도로 표시
    # (바이너리는 소실적 50% 가정이므로 전체 CV의 절반에 내 요율을 곱함)
    b_reg = (r_cv / 2) * bin_rate
    b_mon = (g_cv / 2) * bin_rate
    
    stats.append({
        "단계": f"{i}대" + ("(✅)" if is_qual else "(❌)"),
        "인원": f"{curr:,}명",
        "등록CV": r_cv,
        "등록유니": u_reg,
        "등록바이너리": b_reg,
        "게임CV": g_cv,
        "연금유니": u_mon,
        "연금바이너리": b_mon
    })

# 오빗 보너스 총합 계산
reg_orbit = int((t_reg_cv / 2) // 5460) * 450
mon_orbit = int((t_game_cv / 2) // 5460) * 450

total_reg_bonus = sum(s['등록유니'] + s['등록바이너리'] for s in stats) + reg_orbit
total_mon_bonus = sum(s['연금유니'] + s['연금바이너리'] for s in stats) + mon_orbit

# ADIL 가치
total_adil = (my_gc / 120) * 562.5
adil_val = total_adil * 0.4

# --- 화면 출력 (상단 메트릭) ---
st.divider()
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("총 산하 인원", f"{total_people:,}명")
m2.metric("초기 비용", f"${init_cost:,}")
m3.metric("나의 월 지출", f"${total_monthly_exp:,.2f}")
m4.metric("총 등록 보너스", f"${total_reg_total := total_reg_bonus:,.0f}")
m5.metric("월 연금 수익", f"${total_mon_bonus:,.1f}")
m6.metric("월 순수익(현금)", f"${total_mon_bonus - total_monthly_exp:,.1f}")

tabs = st.tabs(["💰 1회성 등록 보너스 통합", "📅 월간 연금 보너스 통합", "🎯 ADIL 및 자격 조건", "💳 지출 상세 근거"])

with tabs[0]:
    st.subheader("💰 등록 보너스 상세 테이블 (유니레벨 + 바이너리)")
    st.write(f"파트너 {pa_p} 등급 진입 기준 (인당 {p_reg_cv_value} CV)")
    
    df_reg = pd.DataFrame(stats)[["단계", "인원", "등록CV", "등록유니", "등록바이너리"]]
    df_reg.columns = ["단계", "인원수", "발생 CV", "유니레벨($)", "바이너리($)"]
    st.table(df_reg.style.format({"발생 CV": "{:,.0f}", "유니레벨($)": "{:,.1f}", "바이너리($)": "{:,.1f}"}))
    
    c1, c2 = st.columns(2)
    c1.info(f"**오빗 보너스(등록):** {int((t_reg_cv/2)//5460)}회전 발생 → **${reg_orbit:,.0f}**")
    c2.success(f"**등록 보너스 합계:** **${total_reg_bonus:,.1f}**")

with tabs[1]:
    st.subheader("📅 월간 연금 보너스 상세 테이블 (유니레벨 + 바이너리)")
    st.write(f"파트너 {pa_p} 등급 월 120판 기준 (인당 {p_game_cv_value} CV 발생)")
    
    df_mon = pd.DataFrame(stats)[["단계", "인원", "게임CV", "연금유니", "연금바이너리"]]
    df_mon.columns = ["단계", "인원수", "발생 CV", "유니레벨($)", "바이너리($)"]
    st.table(df_mon.style.format({"발생 CV": "{:,.1f}", "유니레벨($)": "{:,.1f}", "바이너리($)": "{:,.1f}"}))
    
    c3, c4 = st.columns(2)
    c3.info(f"**오빗 보너스(연금):** {int((t_game_cv/2)//5460)}회전 발생 → **${mon_orbit:,.0f}**")
    c4.success(f"**월 연금 수익 합계:** **${total_mon_bonus:,.1f}**")

with tabs[2]:
    st.subheader("🎯 ADIL 및 자격 충족(72 CV)")
    st.write(f"- 월 {my_gc}회 게임 시 예상 ADIL: **{total_adil:,.1f}개** (가치 ${adil_val:,.1f})")
    st.divider()
    st.write(f"**자가 CV 현황:** 발생 {my_gen_cv:.1f} CV / 기준 72.0 CV")
    if cv_shortfall > 0:
        st.warning(f"⚠️ 부족분 {cv_shortfall:.1f} CV에 대해 ${shortfall_fee} 추가 구독료 발생 (Basic/Standard 등급)")
    else:
        st.success("✅ 자가 CV 충족 완료 (Premium/Ultimate 또는 게임 수 충분)")

with tabs[3]:
    st.subheader("💳 지출 및 이자수익 상세 ($110.25 근거)")
    st.write("나의 120판 게임 시 발생하는 실질 비용 계산:")
    st.write("- 1위(7.5회) 비용: $150.00")
    st.write("- 2위(7.5회) 이자수익(4%): -$6.00")
    st.write("- 3~16위(105회) 이자수익(1.5%): -$33.75")
    st.markdown(f"### **실질 게임 지출액: ${base_game_cost:,.2f}**")
    st.caption("※ 이 지출액에 CV 부족분 과금이 합산되어 '나의 월 지출'이 결정됩니다.")
