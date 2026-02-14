import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 비지니스 분석 (Ultimate 4대/30명 기준)")

# 1. 데이터 정의 (핵심 로직 보존)
pkgs = {
    "Basic": {"price": 150, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 450, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1050, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2250, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 4} # 4대로 제한 수정
}

# --- 사이드바 설정 ---
st.sidebar.header("📌 설정")
my_p = st.sidebar.selectbox("내 패키지 등급", list(pkgs.keys()), index=3) # 기본값 Ultimate
my_gc = st.sidebar.number_input("나의 월 게임수", value=120, step=120)
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=2) # 파트너 Premium 가정
l1 = st.sidebar.number_input("1대 직접소개 인원", value=2)
dup = st.sidebar.radio("하위 복제 인원", [2, 3], index=0) # 2명 선택 시 총 30명

# --- 계산 로직 ---

# A. 지출 (초기비용 + 월지출)
init_cost = pkgs[my_p]["price"] + 60
monthly_exp = (my_gc / 120) * 110.25 
total_expense = init_cost + monthly_exp

# B. 수익 (4대까지만 반복 계산)
p_reg_cv_value = pkgs[pa_p]["reg_cv"]
p_game_cv_value = 72.0 if pkgs[pa_p]["self_rate"] == 0.03 else 36.0
u_rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05} # 요율 4대까지만 정의

stats = []
t_reg_cv = t_game_cv = total_people = 0
curr = l1

for i in range(1, 5): # 4대까지만 강제 제한
    if i > 1: curr *= dup
    total_people += curr
    
    r_cv = curr * p_reg_cv_value
    g_cv = curr * (my_gc / 120 * p_game_cv_value)
    
    t_reg_cv += r_cv
    t_game_cv += g_cv
    
    u_reg = r_cv * u_rates[i]
    u_mon = g_cv * u_rates[i]
    
    stats.append({
        "단계": f"{i}대",
        "인원": f"{curr:,}명",
        "등록CV": r_cv,
        "등록유니": u_reg,
        "게임CV": g_cv,
        "연금유니": u_mon,
        "요율": f"{int(u_rates[i]*100)}%"
    })

# 바이너리 & 오빗 (소실적 기준)
w_reg_cv, w_mon_cv = t_reg_cv / 2, t_game_cv / 2
bin_reg = w_reg_cv * pkgs[my_p]["bin"]
bin_mon = w_mon_cv * pkgs[my_p]["bin"]
orb_reg = int(w_reg_cv // 5460) * 450
orb_mon = int(w_mon_cv // 5460) * 450

total_reg_bonus = sum(s['등록유니'] for s in stats) + bin_reg + orb_reg
total_mon_bonus = sum(s['연금유니'] for s in stats) + bin_mon + orb_mon

# C. 순수익 (종합 수익 - 종합 지출)
total_revenue = total_reg_bonus + total_mon_bonus
net_profit = total_revenue - total_expense

# --- 화면 출력 ---
st.divider()
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("총 산하 인원", f"{total_people:,}명") # 정확히 30명 출력
m2.metric("초기 비용", f"${init_cost:,}")
m3.metric("나의 월 지출", f"${monthly_exp:,.2f}")
m4.metric("총 등록 보너스", f"${total_reg_bonus:,.0f}")
m5.metric("월 연금 수익", f"${total_mon_bonus:,.1f}")
m6.metric("종합 순수익", f"${net_profit:,.1f}")

tabs = st.tabs(["💎 유니레벨 보너스", "⚖️ 바이너리 & 오빗", "🎯 ADIL & 자격 요건"])

with tabs[0]:
    st.subheader("💎 4대(30명) 제한 유니레벨 보너스")
    c1, c2 = st.columns(2)
    with c1:
        df_reg = pd.DataFrame(stats)[["단계", "인원", "등록CV", "요율", "등록유니"]]
        st.table(df_reg.style.format({"등록CV": "{:,.0f}", "등록유니": "{:,.1f}"}))
    with c2:
        df_mon = pd.DataFrame(stats)[["단계", "인원", "게임CV", "요율", "연금유니"]]
        st.table(df_mon.style.format({"게임CV": "{:,.1f}", "연금유니": "{:,.1f}"}))

with tabs[1]:
    st.subheader("⚖️ 소실적 CV 기반 보너스")
    st.write(f"등록 소실적: {w_reg_cv:,.0f} CV / 연금 소실적: {w_mon_cv:,.1f} CV")
    st.info(f"바이너리({int(pkgs[my_p]['bin']*100)}%) + 오빗 보너스 합산 완료")

with tabs[2]:
    total_adil = (my_gc / 120) * 562.5
    st.write(f"월 예상 ADIL 코인 획득: **{total_adil:,.1f}개**")
