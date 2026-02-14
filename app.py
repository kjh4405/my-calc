import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 종합 수익 분석 (순수익 로직 수정)")

# 1. 데이터 정의 (핵심 로직 보존)
pkgs = {
    "Basic": {"price": 150, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 450, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1050, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2250, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 6}
}

# --- 사이드바 설정 ---
st.sidebar.header("📌 설정")
my_p = st.sidebar.selectbox("내 패키지 등급", list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input("나의 월 게임수 (120단위)", value=120, min_value=120, step=120)
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("1대 직접소개 인원", value=2, min_value=1)
dup = st.sidebar.radio("하위 복제 인원 (2~4대)", [2, 3], index=0)

# --- 계산 로직 (수식 보존) ---

# A. 지출 (초기비용 + 월지출)
init_cost = pkgs[my_p]["price"] + 60
base_game_cost = (my_gc / 120) * 110.25 
my_gen_cv = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0.0, 72.0 - my_gen_cv)
shortfall_fee = cv_shortfall * 2.0 
monthly_exp = base_game_cost + shortfall_fee

total_expense = init_cost + monthly_exp # 지출 합계

# B. 수익 (등록 + 연금)
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
    stats.append({"단계": f"{i}대", "인원": curr, "u_reg": u_reg, "u_mon": u_mon, "is_qual": is_qual})

# 바이너리/오빗
w_reg_cv, w_mon_cv = t_reg_cv / 2, t_game_cv / 2
bin_reg = w_reg_cv * pkgs[my_p]["bin"]
bin_mon = w_mon_cv * pkgs[my_p]["bin"]
orb_reg = int(w_reg_cv // 5460) * 450
orb_mon = int(w_mon_cv // 5460) * 450

total_reg_bonus = sum(s['u_reg'] for s in stats) + bin_reg + orb_reg
total_mon_bonus = sum(s['u_mon'] for s in stats) + bin_mon + orb_mon

total_revenue = total_reg_bonus + total_mon_bonus # 수익 합계

# --- C. 순수익 (요청하신 공식 반영) ---
# (등록보너스 + 월보너스) - (초기비용 + 월지출)
net_profit = total_revenue - total_expense

# --- 화면 출력 ---
st.divider()
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("총 산하 인원", f"{total_people:,}명")
m2.metric("초기 비용", f"${init_cost:,}")
m3.metric("나의 월 지출", f"${monthly_exp:,.2f}")
m4.metric("총 등록 보너스", f"${total_reg_bonus:,.0f}")
m5.metric("월 연금 수익", f"${total_mon_bonus:,.1f}")
# 수정한 순수익 지표
m6.metric("종합 순수익", f"${net_profit:,.1f}", delta="첫 달 누적 기준")

# 상세 탭 (기존 내용 그대로 유지)
tabs = st.tabs(["💎 유니레벨 보너스", "⚖️ 바이너리 & 오빗", "🎯 ADIL & 자격 요건", "💳 지출 상세"])

with tabs[3]:
    st.subheader("💳 종합 지출 분석")
    st.write(f"- 초기 진입 비용: ${init_cost:,}")
    st.write(f"- 월간 실질 게임비: ${base_game_cost:,.2f}")
    if shortfall_fee > 0:
        st.write(f"- 자가 CV 부족분 구독료: ${shortfall_fee:,.1f}")
    st.divider()
    st.markdown(f"### **총 지출 합계: ${total_expense:,.2f}**")
