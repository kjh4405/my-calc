import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP 정밀 수익 분석기", layout="wide")
st.title("🚀 DHP 보너스 시뮬레이션")

# [데이터 보존] 기존 가격 및 로직 절대 유지
pkgs = {
    "Basic": {"price": 120, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 480, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1200, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2640, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 6}
}

# --- 사이드바 설정 ---
st.sidebar.header("📌 설정")
my_p = st.sidebar.selectbox("내 패키지 등급", list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input("나의 월 게임수 (120단위)", value=120, min_value=120, step=120)
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("1대 직접소개 인원", value=2, min_value=1)
dup = st.sidebar.radio("하위 복제 인원 (2~6대)", [2, 3], index=0)

# --- [수정 금지] 기존 계산 로직 구간 ---
init_cost = pkgs[my_p]["price"] + 60
base_game_cost = (my_gc / 120) * 110.25 
my_gen_cv = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0.0, 72.0 - my_gen_cv)
shortfall_fee = cv_shortfall * 2.0 
monthly_exp = base_game_cost + shortfall_fee
total_expense_sum = init_cost + monthly_exp

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
        stats.append({"단계": f"{i}대", "인원": curr, "r_u": u_reg, "m_u": u_mon, "rate": f"{int(rates[i]*100)}%"})

w_reg_cv, w_mon_cv = t_reg_cv / 2, t_game_cv / 2
bin_reg = w_reg_cv * pkgs[my_p]["bin"]
bin_mon = w_mon_cv * pkgs[my_p]["bin"]
orb_reg = int(w_reg_cv // 5460) * 450
orb_mon = int(w_mon_cv // 5460) * 450

total_reg_bonus = sum(s['r_u'] for s in stats) + bin_reg + orb_reg
total_mon_bonus = sum(s['m_u'] for s in stats) + bin_mon + orb_mon
net_profit = (total_reg_bonus + total_mon_bonus) - total_expense_sum

# --- [신규 추가] ADIL 확률 및 보너스 상세 ---

# 1. ADIL 수익 분석 (120판 기준 562.5개 획득)
adil_count = (my_gc / 120) * 562.5
adil_prices = [0.1, 0.5, 1.0, 2.0] # 예상 상장가
win_rates = [1/16, 2/16, 4/16] # 1위 확률 (기본 6.25%, 숙련 12.5%, 전략 25%)

# 2. 보너스 상세 내역 테이블용 데이터
detail_data = [
    {"항목": "유니레벨 보너스", "1회성 등록 수익": f"${sum(s['r_u'] for s in stats):,.1f}", "매달 연금 수익": f"${sum(s['m_u'] for s in stats):,.1f}"},
    {"항목": "바이너리 보너스", "1회성 등록 수익": f"${bin_reg:,.1f}", "매달 연금 수익": f"${bin_mon:,.1f}"},
    {"항목": "오빗 보너스", "1회성 등록 수익": f"${orb_reg:,.0f}", "매달 연금 수익": f"${orb_mon:,.0f}"},
]

# --- 화면 출력 ---
st.divider()
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("총 산하 인원", f"{total_people:,}명")
m2.metric("초기 비용", f"${init_cost:,}")
m3.metric("나의 월 지출", f"${monthly_exp:,.2f}")
m4.metric("총 등록 보너스", f"${total_reg_bonus:,.0f}")
m5.metric("월 연금 수익", f"${total_mon_bonus:,.1f}")
m6.metric("종합 순수익", f"${net_profit:,.1f}")

# 탭 메뉴 구성
tabs = st.tabs(["📊 보너스 상세내역", "💰 ADIL 기대수익", "💳 지출/구조 상세"])

with tabs[0]:
    st.subheader("🧾 보너스 유형별 상세 리포트")
    st.table(pd.DataFrame(detail_data))
    st.info(f"💡 유니레벨은 현재 {my_lim}대까지 합산된 결과입니다.")

with tabs[1]:
    st.subheader(f"🪙 ADIL 코인 가치 분석 (월 {adil_count:,.0f}개 획득 시)")
    adil_results = []
    for p in adil_prices:
        row = {"상장가 ($)": f"${p}"}
        for r in win_rates:
            prob_label = f"확률 {r*100:.1f}%"
            # 1위 확률에 따른 기대 가치 (단순 보유 가치 + 확률적 가산)
            row[prob_label] = f"${(adil_count * p * (1 + r)):,.1f}"
        adil_results.append(row)
    st.table(pd.DataFrame(adil_results))
    st.caption("※ 확률 수익은 1위 당첨 시 추가 보상 가중치를 반영한 기대값입니다.")

with tabs[2]:
    col1, col2 = st.columns(2)
    with col1:
        st.write("**[조직도 시뮬레이션]**")
        st.write(pd.DataFrame(stats)[["단계", "인원", "rate"]].rename(columns={"rate": "요율"}))
    with col2:
        st.write("**[지출 상세]**")
        st.write(f"- 패키지(${pkgs[my_p]['price']}) + 회비($60) = ${init_cost}")
        st.write(f"- 월간 실질 지출: ${monthly_exp:,.2f}")
