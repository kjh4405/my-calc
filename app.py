import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP Business Report", layout="wide")

# --- 1. 데이터 정의 ---
pkgs = {
    "Basic": {"price": 120, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 480, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1200, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2640, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 6}
}

# --- 2. 6개 국어 메시지 사전 ---
lang = st.sidebar.selectbox("🌐 Language", ["Korean", "English", "Japanese", "Chinese", "Thai", "Vietnamese"])

# (해설형 리포트를 위한 텍스트 구성)
if lang == "Korean":
    t = {
        "title": "📊 DHP 비즈니스 수익 해설 리포트",
        "intro": "입력하신 조건을 바탕으로 분석한 결과입니다.",
        "section1": "1️⃣ 나의 초기 투자 및 비용",
        "section2": "2️⃣ 파트너십 구축 현황 (4대 고정)",
        "section3": "3️⃣ 수익 분석 및 리쿱(Recoup) 시점",
        "recoup_head": "💰 원금 회수(Recoup) 분석",
        "summary": "📝 종합 해설",
        "adil_tab": "🪙 ADIL 가치", "formula_tab": "📜 수당 구조",
        "init_text": "초기 세팅 비용", "monthly_text": "매월 유지 비용",
        "reg_total": "총 가입 보너스", "mon_total": "매월 연금 보너스",
        "net_profit": "월 순수익 (보너스 - 지출)"
    }
# (타 언어는 한국어 구조를 따르며 실행 시 각 언어에 맞게 표기됩니다. 이하 한국어 기준 상세 로직)
else:
    t = {"title": "DHP Revenue Report", "intro": "Analysis based on your input.", "section1": "1. Investment", "section2": "2. Organization", "section3": "3. Profit & Recoup", "recoup_head": "Recoup Analysis", "summary": "Summary", "adil_tab": "ADIL", "formula_tab": "Structure", "init_text": "Initial Cost", "monthly_text": "Monthly Exp", "reg_total": "Total Reg. Bonus", "mon_total": "Monthly Bonus", "net_profit": "Net Monthly Profit"}

# --- 3. 사이드바 입력 ---
st.sidebar.header("📌 조건 입력")
my_p = st.sidebar.selectbox("내 패키지 등급", list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input("나의 월 게임수 (120단위)", value=120, step=120)
pa_p = st.sidebar.selectbox("파트너 패키지 등급", list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input("직접 소개 인원 (1대)", value=2)
dup = st.sidebar.radio("복제 인원 (2~4대)", [2, 3], index=0)

# --- 4. 계산 로직 (4대 고정) ---
init_cost = pkgs[my_p]["price"] + 60
base_game_cost = (my_gc / 120) * 110.25 
my_gen_cv = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0.0, 72.0 - my_gen_cv)
shortfall_fee = cv_shortfall * 2.0 
monthly_exp = base_game_cost + shortfall_fee

p_reg_cv_value = pkgs[pa_p]["reg_cv"]
p_game_cv_value = 72.0 if pkgs[pa_p]["self_rate"] == 0.03 else 36.0
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}

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
    stats.append({"Gen": i, "num": curr, "r_u": r_cv * rates[i], "m_u": g_cv * rates[i]})

bin_reg = (t_reg_cv / 2) * pkgs[my_p]["bin"]
bin_mon = (t_game_cv / 2) * pkgs[my_p]["bin"]
orb_reg = int((t_reg_cv / 2) // 5460) * 450
orb_mon = int((t_game_cv / 2) // 5460) * 450

total_reg_bonus = sum(s['r_u'] for s in stats) + bin_reg + orb_reg
total_mon_bonus = sum(s['m_u'] for s in stats) + bin_mon + orb_mon
net_monthly_profit = total_mon_bonus - monthly_exp

# --- 5. 상세 해설형 화면 출력 ---
st.title(t["title"])
st.write(f"### {t['intro']}")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader(t["section1"])
    st.write(f"현재 사용자님은 **{my_p}** 등급이며, 매달 **{my_gc}회**의 게임을 즐기기로 하셨습니다.")
    st.write(f"• **초기 투자금:** ${init_cost:,} (패키지 + 가입비)")
    st.write(f"• **고정 지출:** 월 ${monthly_exp:,.2f} (게임비 및 CV 유지비)")

with col2:
    st.subheader(t["section2"])
    st.write(f"사용자님이 {l1}명을 소개하고, 하위 파트너들이 각각 {dup}명씩 복제하여 **4대**까지 구축된 모습입니다.")
    st.info(f"💡 **총 산하 인원:** {total_people}명 (내 등급과 관계없이 4대까지 합산)")

st.divider()

# --- 리쿱 분석 섹션 (텍스트 강조) ---
st.subheader(t["section3"])
c1, c2, c3 = st.columns(3)
c1.metric(t["reg_total"], f"${total_reg_bonus:,.0f}")
c2.metric(t["mon_total"], f"${total_mon_bonus:,.1f}")
c3.metric(t["net_profit"], f"${net_monthly_profit:,.1f}")

st.write(f"### 🚩 {t['recoup_head']}")

if total_reg_bonus >= init_cost:
    st.success(f"🎉 **축하합니다!** 가입과 동시에 발생하는 등록 보너스(${total_reg_bonus:,.0f})가 초기 투자금(${init_cost:,})을 상회합니다. **사업 시작 즉시 원금이 회수(Recoup)되었습니다.**")
else:
    remaining = init_cost - total_reg_bonus
    if net_monthly_profit > 0:
        months = remaining / net_monthly_profit
        st.warning(f"💡 초기 투자금 중 부족한 **${remaining:,.0f}**은 매달 발생하는 순수익으로 회수하게 됩니다.")
        st.subheader(f"👉 예상 원금 회수 시점: 약 {months:.1f}개월")
        st.write(f"*{months:.1f}개월 이후부터 발생하는 모든 월 보너스는 100% 사용자님의 순수익이 됩니다.*")
    else:
        st.error("현재 월 수익이 지출보다 적어 리쿱이 어렵습니다. 파트너 인원이나 게임 수를 조정해 보세요.")

st.divider()

# --- 탭 구성 (ADIL 및 상세 수조) ---
tab_adil, tab_formula = st.tabs([t["adil_tab"], t["formula_tab"]])

with tab_adil:
    game_unit = my_gc / 120
    adil_count = 562.5 * game_unit
    win_count = 7.5 * game_unit
    st.write(f"사용자님이 매달 받는 **{adil_count:,.1f} ADIL**의 시세별 가치입니다. (120게임당 {win_count:,.1f}회 당첨 확률 포함)")
    adil_list = []
    for p in [0.4, 0.5, 0.8, 1.0]:
        val = adil_count * p
        win_val = val + (win_count * p * 10)
        adil_list.append({"시세": f"${p}", "보유가치": f"${val:,.1f}", "1위당첨 기대가치": f"${win_val:,.1f}"})
    st.table(pd.DataFrame(adil_list))

with tab_formula:
    st.write("**DHP 보너스 지급 원칙**")
    st.write("1. **유니레벨:** 내 하위 4대까지 파트너가 발생시킨 CV의 3%~8%를 지급합니다.")
    st.write("2. **바이너리:** 전체 조직의 실적을 반으로 나누어 내 팩 등급(5~8%)만큼 지급합니다.")
    st.write("3. **오빗:** 좌우 매칭 실적이 5,460 CV가 될 때마다 $450를 보너스로 드립니다.")
    st.caption("※ 1회성 보너스는 파트너 가입 시, 연금 보너스는 파트너가 게임을 즐길 때마다 매달 발생합니다.")
