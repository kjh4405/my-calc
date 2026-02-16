import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP Global & ADIL Analyzer", layout="wide")

# --- 1. 패키지 및 기본 데이터 ---
pkgs = {
    "Basic": {"price": 120, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015},
    "Standard": {"price": 480, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015},
    "Premium": {"price": 1200, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03},
    "Ultimate": {"price": 2640, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03}
}

# --- 2. 6개 국어 완벽 번역 사전 ---
lang_options = ["Korean", "English", "Japanese", "Chinese", "Thai", "Vietnamese"]
lang = st.sidebar.selectbox("🌐 Select Language", lang_options)

t_all = {
    "Korean": {
        "title": "📊 DHP 수익 및 ADIL 자산 분석 리포트",
        "sidebar_h": "📌 조건 입력", "my_p": "내 패키지 등급", "my_gc": "나의 월 게임수 (120단위)",
        "pa_p": "파트너 패키지 등급", "l1": "직접 소개 인원 (1대)", "dup": "복제 인원 (2~5대)",
        "m1": "총 조직", "m2": "총 가입 보너스", "m3": "월 보너스 합계", "m4": "ADIL 월 획득량",
        "tab1": "👥 유니레벨 상세", "tab2": "🪙 ADIL 가치평가", "tab3": "💸 지출/수익 분석",
        "exp_init": "초기 투자금 (패키지+가입비)", "exp_month": "월 유지비 (구독료+부족분)",
        "net_profit": "월 예상 순수익 (보너스 - 유지비)",
        "col_gen": "세대", "col_people": "인원", "col_reg": "등록수당($)", "col_mon": "연금수당($)"
    },
    "English": {
        "title": "📊 DHP & ADIL Asset Analysis Report",
        "sidebar_h": "📌 Settings", "my_p": "My Tier", "my_gc": "Monthly Games (120)",
        "pa_p": "Partner Tier", "l1": "Direct Referrals (1st)", "dup": "Duplication (2-5th)",
        "m1": "Total Org", "m2": "Total Reg. Bonus", "m3": "Monthly Bonus", "m4": "Monthly ADIL",
        "tab1": "👥 Unilevel", "tab2": "🪙 ADIL Valuation", "tab3": "💸 Cash Flow",
        "exp_init": "Initial Investment", "exp_month": "Monthly Expense",
        "net_profit": "Monthly Net Profit",
        "col_gen": "Gen", "col_people": "People", "col_reg": "Reg($)", "col_mon": "Monthly($)"
    },
    "Japanese": {"title": "📊 DHP 収益とADIL資産分析レポート", "sidebar_h": "📌 条件入力", "my_p": "マイパッケージ", "my_gc": "月間プレイ数", "pa_p": "パートナー等級", "l1": "直接紹介(1代)", "dup": "複製(2~5代)", "m1": "総組織", "m2": "登録報酬合計", "m3": "月間報酬合計", "m4": "ADIL月間獲得量", "tab1": "👥 ユニレベル詳細", "tab2": "🪙 ADIL価値評価", "tab3": "💸 支出/収益分析", "exp_init": "初期投資額", "exp_month": "月間維持費", "net_profit": "月間純利益", "col_gen": "世代", "col_people": "人数", "col_reg": "登録報酬($)", "col_mon": "権利収入($)"},
    "Chinese": {"title": "📊 DHP 收益与 ADIL 资产分析报告", "sidebar_h": "📌 设置", "my_p": "我的等级", "my_gc": "每月游戏次数", "pa_p": "伙伴等级", "l1": "直接推荐(1代)", "dup": "复制(2~5代)", "m1": "总组织", "m2": "总注册奖金", "m3": "月度奖金总额", "m4": "每月 ADIL", "tab1": "👥 多层次详情", "tab2": "🪙 ADIL 估值", "tab3": "💸 现金流分析", "exp_init": "初始投资", "exp_month": "每月支出", "net_profit": "每月净利润", "col_gen": "代", "col_people": "人数", "col_reg": "注册奖($)", "col_mon": "月度奖($)"},
    "Thai": {"title": "📊 รายงานการวิเคราะห์รายได้ DHP & ADIL", "sidebar_h": "📌 ตั้งค่า", "my_p": "ระดับของฉัน", "my_gc": "เกมต่อเดือน", "pa_p": "ระดับพาร์ทเนอร์", "l1": "แนะนำตรง(รุ่น 1)", "dup": "การทำซ้ำ(รุ่น 2~5)", "m1": "จำนวนคนรวม", "m2": "โบนัสสมัครรวม", "m3": "รวมรายได้รายเดือน", "m4": "ADIL ต่อเดือน", "tab1": "👥 รายละเอียดรายได้", "tab2": "🪙 การประเมินค่า ADIL", "tab3": "💸 วิเคราะห์รายจ่าย", "exp_init": "เงินลงทุนเริ่มต้น", "exp_month": "ค่าใช้จ่ายรายเดือน", "net_profit": "กำไรสุทธิรายเดือน", "col_gen": "รุ่น", "col_people": "จำนวนคน", "col_reg": "โบนัสสมัคร($)", "col_mon": "รายได้รายเดือน($)"},
    "Vietnamese": {"title": "📊 Báo cáo phân tích thu nhập DHP & ADIL", "sidebar_h": "📌 Cài đặt", "my_p": "Cấp của tôi", "my_gc": "Số lượt chơi/tháng", "pa_p": "Cấp đối tác", "l1": "Trực tiếp(F1)", "dup": "Sao chép(F2~F5)", "m1": "Tổng tổ chức", "m2": "Tổng thưởng ĐK", "m3": "Tổng thưởng tháng", "m4": "ADIL hàng tháng", "tab1": "👥 Chi tiết thu nhập", "tab2": "🪙 Định giá ADIL", "tab3": "💸 Phân tích dòng tiền", "exp_init": "Vốn đầu tư ban đầu", "exp_month": "Chi phí hàng tháng", "net_profit": "Lợi nhuận ròng", "col_gen": "Thế hệ", "col_people": "Số người", "col_reg": "Thưởng ĐK($)", "col_mon": "Thưởng tháng($)"}
}
t = t_all.get(lang, t_all["Korean"])

# --- 3. 입력 및 계산 로직 ---
st.sidebar.header(t["sidebar_h"])
my_p = st.sidebar.selectbox(t["my_p"], list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input(t["my_gc"], value=120, min_value=120, step=120)
pa_p = st.sidebar.selectbox(t["pa_p"], list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input(t["l1"], value=2, min_value=1)
dup = st.sidebar.radio(t["dup"], [2, 3], index=0)

# [추가] ADIL 획득량 계산 (120게임당 2,000 ADIL 기준, 등급별 효율 적용)
adil_efficiency = 2000 if pkgs[my_p]["self_rate"] >= 0.03 else 1000
my_monthly_adil = (my_gc / 120) * adil_efficiency

# [추가] 지출 현황 계산
init_investment = pkgs[my_p]["price"] + 60 # 패키지 + 가입비
monthly_subscription = (my_gc / 120) * 110.25 # 구독료
my_cv_produced = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0.0, 72.0 - my_cv_produced)
monthly_total_expense = monthly_subscription + (cv_shortfall * 2.0)

# 보너스 계산 (유니레벨 5대)
p_reg_cv = pkgs[pa_p]["reg_cv"]
p_mon_cv = 72.0 if pkgs[pa_p]["self_rate"] >= 0.03 else 36.0
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05, 5: 0.02}

stats = []
total_people = 0; t_reg_cv = 0; t_mon_cv = 0; curr = l1
for i in range(1, 6):
    if i > 1: curr *= dup
    total_people += curr
    r_cv = curr * p_reg_cv
    m_cv = curr * (my_gc / 120 * p_mon_cv)
    t_reg_cv += r_cv; t_mon_cv += m_cv
    # 소수점 1자리 강제 고정
    stats.append({
        t["col_gen"]: f"{i} Gen", t["col_people"]: f"{int(curr)}",
        t["col_reg"]: f"{(r_cv * rates[i]):.1f}", t["col_mon"]: f"{(m_cv * rates[i]):.1f}"
    })

# 합계 계산
total_reg_bonus = sum([float(s[t["col_reg"]]) for s in stats]) + ((t_reg_cv / 2) * pkgs[my_p]["bin"])
total_mon_bonus = sum([float(s[t["col_mon"]]) for s in stats]) + ((t_mon_cv / 2) * pkgs[my_p]["bin"])
net_monthly_profit = total_mon_bonus - monthly_total_expense

# --- 4. 화면 출력 ---
st.title(t["title"])
st.divider()

m1, m2, m3, m4 = st.columns(4)
m1.metric(t["m1"], f"{total_people} {t['unit']}")
m2.metric(t["m2"], f"${total_reg_bonus:,.1f}")
m3.metric(t["m3"], f"${total_mon_bonus:,.1f}")
m4.metric(t["m4"], f"{my_monthly_adil:,.0f} ADIL")

st.divider()

tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

with tab1:
    st.table(pd.DataFrame(stats))

with tab2:
    st.subheader("🪙 ADIL Valuation")
    coin_prices = [0.4, 1.0, 2.0, 5.0]
    adil_valuation = []
    for price in coin_prices:
        val = my_monthly_adil * price
        adil_valuation.append({"Price": f"${price}", "Value": f"${val:,.1f}"})
    st.table(pd.DataFrame(adil_valuation))

with tab3:
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**🔴 {t['exp_init']}**")
        st.write(f"Pkg: ${pkgs[my_p]['price']} + Fee: $60 = **${init_investment:,.1f}**")
        st.info(f"**🟠 {t['exp_month']}**")
        st.write(f"Sub: ${monthly_subscription:,.1f} + CV: ${(cv_shortfall*2):,.1f} = **${monthly_total_expense:,.1f}**")
    with col2:
        st.success(f"**💰 {t['net_profit']}**")
        st.write(f"Bonus: ${total_mon_bonus:,.1f} - Exp: ${monthly_total_expense:,.1f}")
        st.subheader(f"${net_monthly_profit:,.1f}")

st.divider()
