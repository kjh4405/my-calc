import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 종합 수익 분석 (최신 가격 반영)")

# 1. 데이터 정의 (보내주신 이미지 가격으로 수정)
# 가격에 회비 60달러는 포함되지 않은 순수 팩 가격입니다.
pkgs = {
    "Basic": {"price": 120, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 480, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1200, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2640, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 6}
}

# --- 사이드바 설정 ---
st.sidebar.header("📌 설정")
my_p = st.sidebar.selectbox("내 패키지 등급", list(pkgs.keys()), index=2) # Premium
my_gc = st.sidebar.number_input("나의 월 게임수", value=120, step=120)
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("1대 직접소개 인원", value=2)
dup = st.sidebar.radio("하위 복제 인원 (2~6대)", [2, 3], index=0)

# --- 계산 로직 ---

# A. 지출 (보내주신 가격 + 회비 60)
init_cost = pkgs[my_p]["price"] + 60
monthly_exp = (my_gc / 120) * 110.25 
total_expense_sum = init_cost + monthly_exp

# B. 수익 및 인원 (등급별 수령 한도 적용)
p_reg_cv_value = pkgs[pa_p]["reg_cv"]
p_game_cv_value = 72.0 if pkgs[pa_p]["self_rate"] == 0.03 else 36.0
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05, 5: 0.02, 6: 0.02}
my_lim = pkgs[my_p]["lim"]

stats = []
t_reg_cv = t_game_cv = total_people = 0
curr = l1

for i in range(1, 7):
    if i > 1: curr *= dup
    if i <= my_lim:
        total_people += curr
        r_cv = curr * p_reg_cv_value
        g_cv = curr * (my_gc / 120 * p_game_cv_value)
        t_reg_cv += r_cv
        t_game_cv += g_cv
        u_reg = r_cv * rates[i]
        u_mon = g_cv * rates[i]
        stats.append({"단계": f"{i}대", "인원": f"{curr:,}명", "등록유니": u_reg, "연금유니": u_mon, "요율": f"{int(rates[i]*100)}%"})

# 바이너리 & 오빗
w_reg_cv, w_mon_cv = t_reg_cv / 2, t_game_cv / 2
bin_reg = w_reg_cv * pkgs[my_p]["bin"]
bin_mon = w_mon_cv * pkgs[my_p]["bin"]
orb_reg = int(w_reg_cv // 5460) * 450
orb_mon = int(w_mon_cv // 5460) * 450

total_reg_bonus = sum(s['등록유니'] for s in stats) + bin_reg + orb_reg
total_mon_bonus = sum(s['연금유니'] for s in stats) + bin_mon + orb_mon

# C. 순수익 공식: (수익 합계) - (초기비용 + 월지출)
total_revenue_sum = total_reg_bonus + total_mon_bonus
net_profit = total_revenue_sum - total_expense_sum

# --- 화면 출력 ---
st.divider()
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("총 산하 인원", f"{total_people:,}명")
m2.metric("초기 비용", f"${init_cost:,}") # 이제 Premium 선택 시 1,260달러 표시
m3.metric("나의 월 지출", f"${monthly_exp:,.2f}")
m4.metric("총 등록 보너스", f"${total_reg_bonus:,.0f}")
m5.metric("월 연금 수익", f"${total_mon_bonus:,.1f}")
m6.metric("종합 순수익", f"${net_profit:,.1f}")

st.info(f"💡 **업데이트 내역:** {my_p} 팩 가격 ${pkgs[my_p]['price']} + 회비 $60 = 초기 비용 ${init_cost}")
