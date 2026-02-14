import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 종합 수익 분석")

# 1. 데이터 정의
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

# A. 나의 월 지출 ($110.25 고정 및 자가 CV 부족분)
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
    
    is_qual = i <= lim
    u_reg = r_cv * rates[i] if is_qual else 0
    u_mon = g_cv * rates[i] if is_qual else 0
    
    stats.append({
        "단계": f"{i}대" + (" (✅)" if is_qual else " (❌)"),
        "인원": f"{curr:,}명",
        "등록CV": r_cv,
        "등록유니": u_reg,
        "게임CV": g_cv,
        "연금유니": u_mon,
        "요율": f"{int(rates[i]*100)}%"
    })

# 바이너리 & 오빗 계산 (소실적 CV 근거)
w_reg_cv = t_reg_cv / 2
w_mon_cv = t_game_cv / 2

bin_reg = w_reg_cv * pkgs[my_p]["bin"]
bin_mon = w_mon_cv * pkgs[my_p]["bin"]

orb_reg = int(w_reg_cv // 5460) * 450
orb_mon = int(w_mon_cv // 5460) * 450

total_reg_bonus = sum(s['등록유니'] for s in stats) + bin_reg + orb_reg
total_mon_bonus = sum(s['연금유니'] for s in stats) + bin_mon + orb_mon

# ADIL 가치
total_adil = (my_gc / 120) * 562.5
adil_val = total_adil * 0.4

# --- 화면 출력 (상단 메트릭) ---
st.divider()
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("총 산하 인원", f"{total_people:,}명")
m2.metric("초기 비용", f"${init_cost:,}")
m3.metric("나의 월 지출", f"${total_monthly_exp:,.2f}")
m4.metric("총 등록 보너스", f"${total_reg_bonus:,.0f}")
m5.metric("월 연금 수익", f"${total_mon_bonus:,.1f}")
m6.metric("월 순수익(현금)", f"${total_mon_bonus - total_monthly_exp:,.1f}")

tabs = st.tabs(["💎 유니레벨 보너스", "⚖️ 바이너리 & 오빗 (소실적 기준)", "🎯 ADIL & 자격 요건", "💳 지출 산출 근거"])

with tabs[0]:
    st.subheader("💎 단계별 유니레벨 보너스")
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("**[1회성 등록 유니레벨]**")
        df_reg = pd.DataFrame(stats)[["단계", "인원", "등록CV", "요율", "등록유니"]]
        df_reg.columns = ["단계", "인원수", "발생 CV", "요율", "수익($)"]
        st.table(df_reg.style.format({"발생 CV": "{:,.0f}", "수익($)": "{:,.1f}"}))
        st.write(f"**등록 유니레벨 소계: ${sum(s['등록유니'] for s in stats):,.1f}**")

    with c2:
        st.write("**[월간 연금 유니레벨]**")
        df_mon = pd.DataFrame(stats)[["단계", "인원", "게임CV", "요율", "연금유니"]]
        df_mon.columns = ["단계", "인원수", "발생 CV", "요율", "수익($)"]
        st.table(df_mon.style.format({"발생 CV": "{:,.1f}", "수익($)": "{:,.1f}"}))
        st.write(f"**연금 유니레벨 소계: ${sum(s['연금유니'] for s in stats):,.1f}**")

with tabs[1]:
    st.subheader("⚖️ 소실적 CV 기반 보너스 (바이너리 & 오빗)")
    st.write("바이너리와 오빗은 동일한 **소실적 CV**를 근거로 계산됩니다.")
    
    col_reg, col_mon = st.columns(2)
    
    with col_reg:
        st.info(f"**등록 소실적 CV: {w_reg_cv:,.0f} CV**")
        st.write(f"- 바이너리 ({int(pkgs[my_p]['bin']*100)}%): **${bin_reg:,.1f}**")
        st.write(f"- 오빗 ({int(w_reg_cv//5460)}회전): **${orb_reg:,.0f}**")
        st.markdown(f"**등록 합계: ${bin_reg + orb_reg:,.1f}**")

    with col_mon:
        st.success(f"**연금 소실적 CV: {w_mon_cv:,.1f} CV**")
        st.write(f"- 바이너리 ({int(pkgs[my_p]['bin']*100)}%): **${bin_mon:,.1f}**")
        st.write(f"- 오빗 ({int(w_mon_cv//5460)}회전): **${orb_mon:,.0f}**")
        st.markdown(f"**연금 합계: ${bin_mon + orb_mon:,.1f}**")

with tabs[2]:
    st.subheader("🎯 ADIL 및 자격 충족(72 CV)")
    st.write(f"**[ADIL 획득 예상]**")
    st.write(f"- 월 {my_gc}회 게임 시 예상 ADIL: **{total_adil:,.1f}개** (가치: **${adil_val:,.1f}**)")
    st.divider()
    st.write(f"**[자가 CV 현황]**")
    st.write(f"- 내 게임으로 발생한 CV: **{my_gen_cv:.1f} CV** (기준: 72.0 CV)")
    if cv_shortfall > 0:
        st.warning(f"⚠️ 부족분 {cv_shortfall:.1f} CV에 대해 **${shortfall_fee}** 추가 구독료 합산")
    else:
        st.success("✅ 자가 CV 충족 완료")

with tabs[3]:
    st.subheader("💳 지출 산출 근거 ($110.25)")
    st.write("- 1위(7.5회) 비용: $150.00")
    st.write("- 2위(7.5회) 이자수익(4%): -$6.00")
    st.write("- 3~16위(105회) 이자수익(1.5%): -$33.75")
    st.markdown(f"### **실질 게임 지출액: ${base_game_cost:,.2f}**")
