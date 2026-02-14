import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 종합 수익 분석 (순수익 공식 수정본)")

# 1. 데이터 정의
pkgs = {
    "Basic": {"price": 150, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 450, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1050, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2250, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 6}
}

# --- 사이드바 설정 ---
st.sidebar.header("📌 설정")
my_p = st.sidebar.selectbox("내 패키지 등급", list(pkgs.keys()), index=3)
l1 = st.sidebar.number_input("1대 직접소개 인원", value=2, min_value=1)
dup = st.sidebar.number_input("인당 복제 인원(2대 이후)", value=2, min_value=1)
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=1)
my_gc = st.sidebar.number_input("나의 월 게임수", value=120, min_value=120, step=120)

# --- 계산 로직 ---

# A. 지출 계산 (초기비용 + 월지출)
init_cost = pkgs[my_p]["price"] + 60
monthly_exp = (my_gc / 120) * 110.25  # 120판 기준 실질 지출액
total_expense = init_cost + monthly_exp

# B. 수익 계산 (유니레벨 + 바이너리/오빗)
u_rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05, 5: 0.02, 6: 0.02}
my_lim = pkgs[my_p]["lim"]
p_reg_cv = pkgs[pa_p]["reg_cv"]
p_game_cv = 72.0 if pkgs[pa_p]["self_rate"] == 0.03 else 36.0 # 120판 기준 게임 CV

u_data = []
t_u_reg = 0 # 등록 유니레벨 합계
t_u_mon = 0 # 연금 유니레벨 합계
t_reg_cv = 0
t_game_cv = 0
curr_people = l1

for i in range(1, 7):
    if i > 1: curr_people *= dup
    
    # 해당 대수의 총 CV
    r_cv = curr_people * p_reg_cv
    g_cv = curr_people * (my_gc / 120 * p_game_cv)
    t_reg_cv += r_cv
    t_game_cv += g_cv
    
    # 수령 자격 확인 및 계산
    is_qual = i <= my_lim
    reg_bonus = (r_cv * u_rates[i]) if is_qual else 0
    mon_bonus = (g_cv * u_rates[i]) if is_qual else 0
    
    t_u_reg += reg_bonus
    t_u_mon += mon_bonus
    
    u_data.append({
        "대수": f"{i}대",
        "자격": "✅" if is_qual else "❌",
        "인원수": f"{curr_people:,}명",
        "등록수익": f"${reg_bonus:,.1f}",
        "연금수익": f"${mon_bonus:,.1f}"
    })

# 바이너리 & 오빗 (소실적 50% 기준)
bin_reg = (t_reg_cv / 2) * pkgs[my_p]["bin"]
bin_mon = (t_game_cv / 2) * pkgs[my_p]["bin"]
orb_reg = int((t_reg_cv / 2) // 5460) * 450
orb_mon = int((t_game_cv / 2) // 5460) * 450

total_reg_total = t_u_reg + bin_reg + orb_reg
total_mon_total = t_u_mon + bin_mon + orb_mon

# C. 순수익 계산 (사용자 요청 공식)
# (총 등록 보너스 + 월 연금 수익) - (초기 비용 + 월 지출)
net_profit = (total_reg_total + total_mon_total) - total_expense

# --- 결과 출력 ---
st.divider()
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("초기 비용", f"${init_cost:,}")
m2.metric("나의 월 지출", f"${monthly_exp:,.2f}")
m3.metric("총 등록 보너스", f"${total_reg_total:,.0f}")
m4.metric("월 연금 수익", f"${total_mon_total:,.1f}")
m5.metric("지출 합계", f"${total_expense:,.2f}")
m6.metric("종합 순수익", f"${net_profit:,.1f}", delta="초기비용 포함")

st.subheader(f"💎 유니레벨 보너스 상세 (내 등급: {my_p})")
st.table(pd.DataFrame(u_data))

st.info(f"""
💡 **계산 근거:**
1. **지출:** 초기비용(${init_cost:,.0f}) + 월지출(${monthly_exp:,.2f}) = **${total_expense:,.2f}**
2. **수익:** 등록보너스(${total_reg_total:,.0f}) + 연금수익(${total_mon_total:,.1f}) = **${total_reg_total + total_mon_total:,.1f}**
3. **순수익:** 수익 합계 - 지출 합계 = **${net_profit:,.1f}**
""")
