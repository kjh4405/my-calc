import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP Global Analyzer", layout="wide")

# --- 1. 데이터 정의 (팩 가격 및 수식 보존) ---
pkgs = {
    "Basic": {"price": 120, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 480, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1200, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2640, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 6}
}

# --- 2. 6개 국어 텍스트 사전 정의 ---
st.sidebar.header("🌐 Language Settings")
lang = st.sidebar.selectbox("Select Language", ["Korean", "English", "Japanese", "Chinese", "Thai", "Vietnamese"])

if lang == "Korean":
    t = {
        "title": "🚀 DHP 비지니스 종합 수익 분석", "sidebar_h": "📌 설정",
        "my_p": "내 패키지 등급", "my_gc": "나의 월 게임수 (120단위)", "pa_p": "파트너 패키지 등급", "l1": "1대 직접소개 인원", "dup": "하위 복제 인원 (2~6대)",
        "m1": "총 산하 인원 (4대 고정)", "m2": "초기 비용", "m3": "나의 월 지출", "m4": "총 등록 보너스", "m5": "월 연금 수익", "m6": "월 순수익(현금)",
        "tab1": "📊 보너스 상세내역", "tab2": "💰 ADIL 기대수익", "tab3": "💳 지출/구조 상세",
        "detail_h": "보너스 유형별 상세 리포트", "item": "항목", "reg_s": "1회성 등록 수익", "mon_s": "매달 연금 수익",
        "adil_h": "🪙 ADIL 토큰 가치 분석", "adil_info": "120게임당 7.5회 1위 당첨 확률을 기반으로 한 가치 분석입니다.",
        "listing": "ADIL 시세", "hold_v": "보유 가치", "win_v": "1위 당첨 기대가치",
        "exp_h": "💳 지출 상세 근거", "init_h": "초기 비용 합계", "mon_h": "월간 실질 지출", "total_h": "종합 지출액"
    }
elif lang == "English":
    t = {
        "title": "🚀 DHP Business Revenue Analysis", "sidebar_h": "📌 Settings",
        "my_p": "My Package Tier", "my_gc": "Monthly Games (Unit: 120)", "pa_p": "Partner Tier", "l1": "Direct Referrals", "dup": "Duplication Rate",
        "m1": "Total Org. (4 Gen)", "m2": "Initial Cost", "m3": "Monthly Exp.", "m4": "Total Reg. Bonus", "m5": "Recurring Income", "m6": "Net Profit",
        "tab1": "📊 Bonus Details", "tab2": "💰 ADIL Projection", "tab3": "💳 Breakdown",
        "detail_h": "Detailed Bonus Report", "item": "Category", "reg_s": "One-time Registration", "mon_s": "Monthly Recurring",
        "adil_h": "🪙 ADIL Token Value Analysis", "adil_info": "Analysis based on 7.5 wins per 120 games probability.",
        "listing": "ADIL Price", "hold_v": "Holding Value", "win_v": "1st Place Expected Value",
        "exp_h": "💳 Expense Breakdown", "init_h": "Total Initial Cost", "mon_h": "Monthly Practical Expense", "total_h": "Grand Total Expense"
    }
elif lang == "Japanese":
    t = {
        "title": "🚀 DHP ビジネス総合収益分析", "sidebar_h": "📌 設定",
        "my_p": "自分のパッケージ等級", "my_gc": "月間プレイ回数 (120単位)", "pa_p": "パートナーの等級", "l1": "1代目の紹介人数", "dup": "複製人数 (2段目以降)",
        "m1": "総組織人数 (4代固定)", "m2": "初期費用", "m3": "月間支出", "m4": "登録ボーナス合計", "m5": "月間権利収入", "m6": "月間純利益",
        "tab1": "📊 ボーナス詳細", "tab2": "💰 ADIL期待収益", "tab3": "💳 支出詳細",
        "detail_h": "ボーナス詳細レポート", "item": "項目", "reg_s": "登録収入(単発)", "mon_s": "継続月間収入",
        "adil_h": "🪙 ADILトークン価値分析", "adil_info": "120ゲームあたり7.5回の1位当選確率に基づいた価値分析です。",
        "listing": "ADIL価格", "hold_v": "保有価値", "win_v": "1位当選期待価値",
        "exp_h": "💳 支出詳細根拠", "init_h": "初期費用合計", "mon_h": "月間実質支出", "total_h": "総合支出額"
    }
elif lang == "Chinese":
    t = {
        "title": "🚀 DHP 业务综合收益分析", "sidebar_h": "📌 设置",
        "my_p": "我的套餐等级", "my_gc": "每月游戏次数 (120单位)", "pa_p": "伙伴套餐等级", "l1": "第一代直接推荐人数", "dup": "下级复制人数 (2-6代)",
        "m1": "总组织人数 (固定4代)", "m2": "初始费用", "m3": "每月支出", "m4": "总注册奖金", "m5": "每月年金收益", "m6": "每月净利润",
        "tab1": "📊 奖金详情", "tab2": "💰 ADIL 预期收益", "tab3": "💳 支出/结构详情",
        "detail_h": "按类型划分的奖金详情报告", "item": "项目", "reg_s": "一次性注册收益", "mon_s": "每月年金收益",
        "adil_h": "🪙 ADIL 代币价值分析", "adil_info": "基于每 120 场比赛 7.5 次获得第一名的概率进行分析。",
        "listing": "ADIL 价格", "hold_v": "持有价值", "win_v": "第一名预期价值",
        "exp_h": "💳 支出明细依据", "init_h": "初始费用合计", "mon_h": "每月实际支出", "total_h": "总支出金额"
    }
elif lang == "Thai":
    t = {
        "title": "🚀 DHP วิเคราะห์รายได้รวมทางธุรกิจ", "sidebar_h": "📌 การตั้งค่า",
        "my_p": "ระดับแพ็คเกจของฉัน", "my_gc": "จำนวนเกมต่อเดือน (หน่วย 120)", "pa_p": "ระดับแพ็คเกจคู่ค้า", "l1": "จำนวนผู้แนะนำตรง", "dup": "อัตราการทำซ้ำ",
        "m1": "จำนวนคนรวม (4 รุ่น)", "m2": "ต้นทุนเริ่มต้น", "m3": "ค่าใช้จ่ายรายเดือน", "m4": "โบนัสการสมัครรวม", "m5": "รายได้ต่อเนื่องรายเดือน", "m6": "กำไรสุทธิต่อเดือน",
        "tab1": "📊 รายละเอียดโบนัส", "tab2": "💰 การคาดการณ์ ADIL", "tab3": "💳 รายละเอียดค่าใช้จ่าย",
        "detail_h": "รายงานโบนัสตามประเภท", "item": "รายการ", "reg_s": "รายได้จากการสมัคร", "mon_s": "รายได้รายเดือน",
        "adil_h": "🪙 วิเคราะห์มูลค่าโทเค็น ADIL", "adil_info": "การวิเคราะห์ตามโอกาสชนะอันดับ 1 ที่ 7.5 ครั้งต่อ 120 เกม",
        "listing": "ราคา ADIL", "hold_v": "มูลค่าที่ถือครอง", "win_v": "มูลค่าคาดการณ์เมื่อชนะ",
        "exp_h": "💳 รายละเอียดค่าใช้จ่าย", "init_h": "รวมต้นทุนเริ่มต้น", "mon_h": "ค่าใช้จ่ายรายเดือนจริง", "total_h": "ยอดรวมค่าใช้จ่ายทั้งหมด"
    }
else: # Vietnamese
    t = {
        "title": "🚀 Phân tích thu nhập kinh doanh DHP", "sidebar_h": "📌 Cài đặt",
        "my_p": "Cấp gói của tôi", "my_gc": "Số lượt chơi hàng tháng (Đơn vị 120)", "pa_p": "Cấp gói đối tác", "l1": "Số người F1", "dup": "Tỷ lệ sao chép",
        "m1": "Tổng số thành viên (4 cấp)", "m2": "Chi phí ban đầu", "m3": "Chi phí hàng tháng", "m4": "Tổng thưởng đăng ký", "m5": "Thu nhập thụ động", "m6": "Lợi nhuận ròng",
        "tab1": "📊 Chi tiết tiền thưởng", "tab2": "💰 Dự báo ADIL", "tab3": "💳 Chi tiết chi phí",
        "detail_h": "Báo cáo chi tiết tiền thưởng", "item": "Hạng mục", "reg_s": "Thưởng đăng ký", "mon_s": "Thưởng hàng tháng",
        "adil_h": "🪙 Phân tích giá trị Token ADIL", "adil_info": "Phân tích dựa trên tỷ lệ thắng giải nhất 7.5 lần mỗi 120 lượt chơi.",
        "listing": "Giá ADIL", "hold_v": "Giá trị nắm giữ", "win_v": "Giá trị kỳ vọng giải nhất",
        "exp_h": "💳 Căn cứ chi phí", "init_h": "Tổng chi phí ban đầu", "mon_h": "Chi phí thực tế hàng tháng", "total_h": "Tổng chi phí tổng thể"
    }

# --- 3. 사이드바 및 메인 타이틀 ---
st.title(t["title"])
st.sidebar.header(t["sidebar_h"])
my_p = st.sidebar.selectbox(t["my_p"], list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input(t["my_gc"], value=120, min_value=120, step=120)
pa_p = st.sidebar.selectbox(t["pa_p"], list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input(t["l1"], value=2, min_value=1)
dup = st.sidebar.radio(t["dup"], [2, 3], index=0)

# --- 4. 계산 로직 (4대 고정 인원수 계산법 적용) ---
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

stats = []
t_reg_cv = t_game_cv = total_people = 0
curr = l1

# 무조건 4대까지의 인원과 수당을 계산하도록 수정
for i in range(1, 7):
    if i > 1: curr *= dup
    if i <= 4: # 여기서 4대 고정 적용
        total_people += curr
        r_cv = curr * p_reg_cv_value
        g_cv = curr * (my_gc / 120 * p_game_cv_value)
        t_reg_cv += r_cv
        t_game_cv += g_cv
        u_reg = r_cv * rates[i]
        u_mon = g_cv * rates[i]
        stats.append({"Gen": f"{i} Gen", "num": curr, "r_u": u_reg, "m_u": u_mon, "rt": f"{int(rates[i]*100)}%"})

# 바이너리 & 오빗 계산 로직
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

with tabs[0]: # 보너스 상세
    st.subheader(t["detail_h"])
    detail_data = [
        {t["item"]: "Unilevel", t["reg_s"]: f"${sum(s['r_u'] for s in stats):,.1f}", t["mon_s"]: f"${sum(s['m_u'] for s in stats):,.1f}"},
        {t["item"]: "Binary", t["reg_s"]: f"${bin_reg:,.1f}", t["mon_s"]: f"${bin_mon:,.1f}"},
        {t["item"]: "Orbit", t["reg_s"]: f"${orb_reg:,.0f}", t["mon_s"]: f"${orb_mon:,.0f}"},
    ]
    st.table(pd.DataFrame(detail_data))

with tabs[1]: # ADIL 분석
    game_unit = my_gc / 120
    adil_count = 562.5 * game_unit
    win_count = 7.5 * game_unit
    st.subheader(f"{t['adil_h']} ({t['hold_v']}: {adil_count:,.1f} ADIL)")
    st.info(f"💡 {t['adil_info']}")
    adil_prices = [0.4, 0.5, 0.8, 1.0]
    adil_results = []
    for p in adil_prices:
        total_value = adil_count * p
        expected_value = total_value + (win_count * p * 10)
        adil_results.append({t["listing"]: f"${p}", t["hold_v"]: f"${total_value:,.1f}", t["win_v"]: f"${expected_value:,.1f}"})
    st.table(pd.DataFrame(adil_results))

with tabs[2]: # 지출 상세
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"**[{t['exp_h']}]**")
        st.write(f"- {t['init_h']}: ${init_cost:,}")
        st.write(f"- {t['mon_h']}: ${monthly_exp:,.2f}")
        st.markdown(f"### {t['total_h']}: ${total_expense_sum:,.2f}")
    with col_b:
        st.write("**[Structure]**")
        st.write(pd.DataFrame(stats)[["Gen", "num", "rt"]].rename(columns={"Gen":"Generation", "num":"People", "rt":"Rate"}))
