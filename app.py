import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 종합 수익 분석 (30명 구조 복구)")

# 1. 데이터 정의 (가장 정확했던 원본 데이터)
pkgs = {
    "Basic": {"price": 150, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 450, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1050, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2250, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 6}
}

# --- 사이드바 설정 (사용자 선택에 따라 30명이 나오도록 설정) ---
st.sidebar.header("📌 설정")
my_p = st.sidebar.selectbox("내 패키지 등급", list(pkgs.keys()), index=2) # Premium 기준
my_gc = st.sidebar.number_input("나의 월 게임수 (120단위)", value=120, min_value=120, step=120)
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=2) # 파트너 Premium 기준
l1 = st.sidebar.number_input("1대 직접소개 인원", value=2, min_value=1)
dup = st.sidebar.radio("하위 복제 인원 (2~6대)", [2, 3], index=0) # 2명 선택 시 30명 구조

# --- 계산 로직 (수정 전 가장 정확했던 수식 복구) ---

# A. 지출 계산 (초기비용 + 월지출)
init_cost = pkgs[my_p]["price"] + 60
base_game_cost = (my_gc / 120) * 110.25 
my_gen_cv = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0.0, 72.0 - my_gen_cv)
shortfall_fee = cv_shortfall * 2.0 
monthly_exp = base_game_cost + shortfall_fee

# 종합 지출 (순수익 계산용)
total_expense_sum = init_cost + monthly_exp

# B. 수익 계산 (6대까지의 로직을 유지하되, 2명 복제 시 4대까지 30명이 됨)
p_reg_cv_value = pkgs[pa_p]["reg_cv"]
p_game_cv_value = 72.0 if pkgs[pa_p]["self_rate"] == 0.03 else 36.0
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05, 5: 0.02, 6: 0.02}
lim = pkgs[my_p]["lim"]

stats = []
t_reg_cv = t_game_cv = total_people = 0
curr = l1

for i in range(1, 7):
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

# 바이너리 & 오빗 (가장 정확했던 원본 수식)
w_reg_cv, w_mon_cv = t_reg_cv / 2, t_game_cv / 2
bin_reg = w_reg_cv * pkgs[my_p]["bin"]
bin_mon = w_mon_cv * pkgs[my_p]["bin"]
orb_reg = int(w_reg_cv // 5460) * 450
orb_mon = int(w_mon_cv // 5460) * 450

total_reg_bonus = sum(s['등록유니'] for s in stats) + bin_reg + orb_reg
total_mon_bonus = sum(s['연금유니'] for s in stats) + bin_mon + orb_mon

# C. 순수익 계산 (요청하신 방식: 총수익 - 총지출)
total_revenue_sum = total_reg_bonus + total_mon_bonus
net_profit = total_revenue_sum - total_expense_sum

# --- 화면 출력 (6칸 메트릭 및 인원수 복구) ---
st.divider()
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("총 산하 인원", f"{total_people:,}명") # 설정에 따라 30명 출력
m2.metric("초기 비용", f"${init_cost:,}")
m3.metric("나의 월 지출", f"${monthly_exp:,.2f}")
m4.metric("총 등록 보너스", f"${total_reg_bonus:,.0f}")
m5.metric("월 연금 수익", f"${total_mon_bonus:,.1f}")
m6.metric("종합 순수익", f"${net_profit:,.1f}")

# 통합 탭 구성
tabs = st.tabs(["💎 유니레벨 보너스", "⚖️ 바이너리 & 오빗", "🎯 ADIL & 자격 요건", "💳 지출 상세"])

with tabs[0]:
    st.subheader("💎 단계별 유니레벨 보너스")
    c1, c2 = st.columns(2)
    with c1:
        st.write("**[1회성 등록 유니레벨]**")
        df_reg = pd.DataFrame(stats)[["단계", "인원", "등록CV", "요율", "등록유니"]]
        st.table(df_reg.style.format({"등록CV": "{:,.0f}", "등록유니": "{:,.1f}"}))
    with c2:
        st.write("**[월간 연금 유니레벨]**")
        df_mon = pd.DataFrame(stats)[["단계", "인원", "게임CV", "요율", "연금유니"]]
        st.table(df_mon.style.format({"게임CV": "{:,.1f}", "연금유니": "{:,.1f}"}))

with tabs[1]:
    st.subheader("⚖️ 소실적 CV 기반 보너스 (바이너리 & 오빗)")
    col_reg, col_mon = st.columns(2)
    with col_reg:
        st.info(f"**등록 소실적 CV: {w_reg_cv:,.0f} CV**")
        st.write(f"- 바이너리: ${bin_reg:,.1f}")
        st.write(f"- 오빗: ${orb_reg:,.0f}")
    with col_mon:
        st.success(f"**연금 소실적 CV: {w_mon_cv:,.1f} CV**")
        st.write(f"- 바이너리: ${bin_mon:,.1f}")
        st.write(f"- 오빗: ${orb_mon:,.0f}")

with tabs[2]:
    total_adil = (my_gc / 120) * 562.5
    st.subheader(f"🎯 ADIL 예상 획득: {total_adil:,.1f}개")

with tabs[3]:
    st.subheader("💳 지출 상세 근거")
    st.write(f"- 초기 비용: ${init_cost:,}")
    st.write(f"- 월간 실질 지출: ${monthly_exp:,.2f}")
    st.markdown(f"### **종합 지출액: ${total_expense_sum:,.2f}**")
