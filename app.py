import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP Global Analyzer", layout="wide")

# --- 1. 데이터 정의 (가격 및 수식 절대 보존) ---
pkgs = {
    "Basic": {"price": 120, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 480, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1200, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2640, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 6}
}

# --- 2. 언어 선택 및 텍스트 설정 ---
st.sidebar.header("🌐 Language Settings")
lang = st.sidebar.selectbox("Select Language", ["Korean", "English", "Japanese"])

if lang == "Korean":
    t = {
        "title": "🚀 DHP 비지니스 종합 수익 분석",
        "my_p": "내 패키지 등급", "my_gc": "나의 월 게임수 (120단위)",
        "pa_p": "파트너 패키지 등급", "l1": "1대 직접소개 인원", "dup": "하위 복제 인원 (2~6대)",
        "m1": "총 산하 인원", "m2": "초기 비용", "m3": "나의 월 지출", "m4": "총 등록 보너스", "m5": "월 연금 수익", "m6": "종합 순수익",
        "tab1": "📊 보너스 상세내역", "tab2": "💰 ADIL 기대수익", "tab3": "💳 지출/구조 상세",
        "detail": "보너스 유형별 상세 리포트", "item": "항목", "reg_s": "1회성 등록 수익", "mon_s": "매달 연금 수익",
        "adil_title": "🪙 ADIL 코인 가치 분석", "listing": "예상 상장가", "prob": "1위 확률",
        "exp_title": "💳 지출 상세 근거", "init_h": "초기 비용 합계", "mon_h": "월간 실질 지출", "total_h": "종합 지출액"
    }
elif lang == "English":
    t = {
        "title": "🚀 DHP Business Revenue Analysis",
        "my_p": "My Package Tier", "my_gc": "My Monthly Games (Unit: 120)",
        "pa_p": "Partner Package Tier", "l1": "Direct Referrals (1st Gen)", "dup": "Duplication Rate",
        "m1": "Total Org.", "m2": "Initial Cost", "m3": "Monthly Exp.", "m4": "Total Reg. Bonus", "m5": "Recurring Income", "m6": "Net Profit",
        "tab1": "📊 Bonus Details", "tab2": "💰 ADIL Projection", "tab3": "💳 Breakdown",
        "detail": "Bonus Report by Type", "item": "Category", "reg_s": "One-time Registration", "mon_s": "Monthly Recurring",
        "adil_title": "🪙 ADIL Token Value Analysis", "listing": "Listing Price", "prob": "Win Probability",
        "exp_title": "💳 Expense Breakdown", "init_h": "Total Initial Cost", "mon_h": "Monthly Practical Expense", "total_h": "Grand Total Expense"
    }
else: # Japanese
    t = {
        "title": "🚀 DHP ビジネス総合収益分析",
        "my_p": "自分のパッケージ等級", "my_gc": "月間プレイ回数 (120単位)",
        "pa_p": "パートナーの等級", "l1": "1代目の紹介人数", "dup": "複製人数 (2段目以降)",
        "m1": "総組織人数", "m2": "初期費用", "m3": "月間支出", "m4": "登録ボーナス合計", "m5": "月間権利収入", "m6": "総合純利益",
        "tab1": "📊 ボーナス詳細", "tab2": "💰 ADIL期待収益", "tab3": "💳 支出詳細",
        "detail": "ボーナス詳細レポート", "item": "項目", "reg_s": "登録収入(単발)", "mon_s": "継続月間収入",
        "adil_title": "🪙 ADILトークン価値分析", "listing": "予想上場価格", "prob": "1位当選確率",
        "exp_title": "💳 支出詳細根拠", "init_h": "初期費用合計", "mon_h": "月間実質支出", "total_h": "総合支出額"
    }

st.title(t["title"])

# --- 3. 사이드바 입력 ---
my_p = st.sidebar.selectbox(t["my_p"], list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input(t["my_gc"], value=120, min_value=120, step=120)
pa_p = st.sidebar.selectbox(t["pa_p"], list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input(t["l1"], value=2, min_value=1)
dup = st.sidebar.radio(t["dup"], [2, 3], index=0)

# --- 4. 계산 로직 (기존 수식 100% 보존) ---
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
        stats.append({"Gen": f"{i} Gen", "num": curr, "r_u": u_reg, "m_u": u_mon, "rt": f"{int(rates[i]*100)}%"})

w_reg_cv, w_mon_cv = t_reg_cv / 2, t_game_cv / 2
bin_reg = w_reg_cv * pkgs[my_p]["bin"]
bin_mon = w_mon_cv * pkgs[my_p]["bin"]
orb_reg = int(w_reg_cv // 5460) * 450
orb_mon = int(w_mon_cv // 5460) * 450

total_reg_bonus = sum(s['r_u'] for s in stats) + bin_reg + orb_reg
total_mon_bonus = sum(s['m_u'] for s in stats) + bin_mon + orb_mon
net_profit = (total_reg_bonus + total_mon_bonus) - total_expense_sum

# --- 5. 화면 출력 ---
st.divider()
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric(t["m1"], f"{total_people:,}")
m2.metric(t["m2"], f"${init_cost:,}")
m3.metric(t["m3"], f"${monthly_exp:,.2f}")
m4.metric(t["m4"], f"${total_reg_bonus:,.0f}")
m5.metric(t["m5"], f"${total_mon_bonus:,.1f}")
m6.metric(t["m6"], f"${net_profit:,.1f}")

tabs = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

with tabs[0]:
    st.subheader(t["detail"])
    detail_data = [
        {t["item"]: "Unilevel", t["reg_s"]: f"${sum(s['r_u'] for s in stats):,.1f}", t["mon_s"]: f"${sum(s['m_u'] for s in stats):,.1f}"},
        {t["item"]: "Binary", t["reg_s"]: f"${bin_reg:,.1f}", t["mon_s"]: f"${bin_mon:,.1f}"},
        {t["item"]: "Orbit", t["reg_s"]: f"${orb_reg:,.0f}", t["mon_s"]: f"${orb_mon:,.0f}"},
    ]
    st.table(pd.DataFrame(detail_data))

with tabs[1]:
    st.subheader(f"{t['adil_title']} ({ (my_gc/120)*562.5:,.0f} EA)")
    adil_prices = [0.1, 0.5, 1.0, 2.0]
    win_rates = [1/16, 2/16, 4/16]
    adil_results = []
    for p in adil_prices:
        row = {t["listing"]: f"${p}"}
        for r in win_rates:
            col_name = f"{t['prob']} {r*100:.1f}%"
            row[col_name] = f"${((my_gc/120)*562.5 * p * (1+r)):,.1f}"
        adil_results.append(row)
    st.table(pd.DataFrame(adil_results))

with tabs[2]:
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"**[{t['exp_title']}]**")
        st.write(f"- {t['init_h']}: ${init_cost:,}")
        st.write(f"- {t['mon_h']}: ${monthly_exp:,.2f}")
        st.markdown(f"### {t['total_h']}: ${total_expense_sum:,.2f}")
    with col_b:
        st.write("**[Organization Structure]**")
        st.write(pd.DataFrame(stats)[["Gen", "num", "rt"]].rename(columns={"Gen":"Generation", "num":"People", "rt":"Rate"}))
