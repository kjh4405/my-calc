import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP Business Report", layout="wide")

# --- 1. 데이터 정의 (팩 가격 및 수식 보존) ---
pkgs = {
    "Basic": {"price": 120, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 480, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1200, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2640, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 6}
}

# --- 2. 언어 선택 및 사전 ---
lang = st.sidebar.selectbox("🌐 Language", ["Korean", "English", "Japanese", "Chinese", "Thai", "Vietnamese"])

# (해설형 리포트를 위한 텍스트 사전)
t_dict = {
    "Korean": {
        "title": "📊 DHP 비즈니스 수익 해설 리포트 (5대 기준)",
        "intro": "입력하신 조건을 바탕으로 분석한 결과입니다.",
        "section1": "1️⃣ 나의 초기 투자 및 비용",
        "section2": "2️⃣ 파트너십 구축 현황 (5대 고정 합산)",
        "section3": "3️⃣ 수익 분석 및 리쿱(Recoup) 시점",
        "recoup_head": "💰 원금 회수(Recoup) 분석",
        "reg_total": "총 가입 보너스", "mon_total": "매월 연금 보너스",
        "net_profit": "월 순수익 (보너스 - 지출)",
        "recoup_now": "🎉 즉시 회수 완료!",
        "recoup_wait": "👉 예상 원금 회수 시점:",
        "recoup_desc": "💡 리쿱 이후 월 연금 수익은 전액 순수익이 됩니다."
    }
    # ... (타 언어는 내부적으로 매칭되도록 설계)
}
t = t_dict.get(lang, t_dict["Korean"])

# --- 3. 사이드바 입력 ---
st.sidebar.header("📌 조건 입력")
my_p = st.sidebar.selectbox("내 패키지 등급", list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input("나의 월 게임수 (120단위)", value=120, step=120)
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("직접 소개 인원 (1대)", value=2)
dup = st.sidebar.radio("복제 인원 (2~5대)", [2, 3], index=0)

# --- 4. 계산 로직 (5대 고정 확장) ---
init_cost = pkgs[my_p]["price"] + 60
base_game_cost = (my_gc / 120) * 110.25 
my_gen_cv = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0.0, 72.0 - my_gen_cv)
shortfall_fee = cv_shortfall * 2.0 
monthly_exp = base_game_cost + shortfall_fee

p_reg_cv_value = pkgs[pa_p]["reg_cv"]
p_game_cv_value = 72.0 if pkgs[pa_p]["self_rate"] == 0.03 else 36.0

# 5대까지의 요율 적용 (3% -> 5% -> 8% -> 5% -> 2%)
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05, 5: 0.02}

stats = []
t_reg_cv = t_game_cv = total_people = 0
curr = l1

# [핵심 수정] 1대부터 5대까지 반복 계산
for i in range(1, 6):
    if i > 1: curr *= dup
    total_people += curr
    r_cv = curr * p_reg_cv_value
    g_cv = curr * (my_gc / 120 * p_game_cv_value)
    t_reg_cv += r_cv
    t_game_cv += g_cv
    stats.append({
        "Gen": f"{i} Gen", 
        "num": curr, 
        "r_u": r_cv * rates.get(i, 0), 
        "m_u": g_cv * rates.get(i, 0)
    })

# 바이너리 & 오빗 계산
bin_reg = (t_reg_cv / 2) * pkgs[my_p]["bin"]
bin_mon = (t_game_cv / 2) * pkgs[my_p]["bin"]
orb_reg = int((t_reg_cv / 2) // 5460) * 450
orb_mon = int((t_game_cv / 2) // 5460) * 450

total_reg_bonus = sum(s['r_u'] for s in stats) + bin_reg + orb_reg
total_mon_bonus = sum(s['m_u'] for s in stats) + bin_mon + orb_mon
net_monthly_profit = total_mon_bonus - monthly_exp

# --- 5. 리포트 출력 ---
st.title(t["title"])
st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader(t["section1"])
    st.write(f"• **초기 투자금:** ${init_cost:,}")
    st.write(f"• **월 유지비:** ${monthly_exp:,.2f}")

with col2:
    st.subheader(t["section2"])
    st.info(f"💡 **5대까지 총 인원:** {total_people}명")
    st.write(f"(1대 {l1}명 기준, 각 {dup}명씩 복제)")

st.divider()

st.subheader(t["section3"])
c1, c2, c3 = st.columns(3)
c1.metric(t["reg_total"], f"${total_reg_bonus:,.1f}")
c2.metric(t["mon_total"], f"${total_mon_bonus:,.1f}")
c3.metric(t["net_profit"], f"${net_monthly_profit:,.1f}")

st.write(f"### 🚩 {t['recoup_head']}")

# 리쿱 텍스트 해설
if total_reg_bonus >= init_cost:
    st.success(f"{t['recoup_now']} 등록 보너스(${total_reg_bonus:,.1f})가 초기 비용(${init_cost:,})보다 많습니다.")
else:
    remaining = init_cost - total_reg_bonus
    if net_monthly_profit > 0:
        months = remaining / net_monthly_profit
        st.warning(f"초기 비용 중 남은 **${remaining:,.1f}**을 회수하는 데 약 **{months:.1f}개월**이 소요됩니다.")
        st.write(t["recoup_desc"])
    else:
        st.error("현재 월 순수익이 마이너스입니다. 조직 규모를 키워야 리쿱이 가능합니다.")

st.divider()
# 상세 수량 확인용 테이블 (선택 사항)
with st.expander("🔍 세대별 상세 데이터 보기"):
    st.table(pd.DataFrame(stats))
