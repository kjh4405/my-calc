import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP Global Total Analyzer", layout="wide")

# --- 1. 패키지 데이터 정의 ---
pkgs = {
    "Basic": {"price": 120, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015},
    "Standard": {"price": 480, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015},
    "Premium": {"price": 1200, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03},
    "Ultimate": {"price": 2640, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03}
}

# --- 2. 6개 국어 사전 (요청하신 문구 수정 반영) ---
lang_options = ["Korean", "English", "Japanese", "Chinese", "Thai", "Vietnamese"]
lang = st.sidebar.selectbox("🌐 Select Language", lang_options)

t_all = {
    "Korean": {
        "unit": "명", "title": "📊 DHP 글로벌 수익 및 ADIL 자산 분석", "sidebar_h": "📌 조건 입력",
        "my_p": "내 패키지 등급", "my_gc": "나의 월 게임수", "pa_p": "파트너 패키지 등급", "l1": "직접 소개", "dup": "복제",
        "m1": "총 조직", "m2": "총 가입 보너스", "m3": "월 보너스 합계", "m4": "ADIL 월 획득량",
        "tab1": "👥 유니레벨", "tab2": "⚖️ 바이너리", "tab3": "🚀 오빗(ORBIT)", "tab4": "🪙 ADIL 가치", "tab5": "💸 지출/수익",
        "exp_init": "초기 투자금 (패키지+가입비)", "exp_month": "월 유지비 (구독료+부족분)", "net_profit": "월 예상 순수익",
        "col_gen": "세대", "col_people": "인원", "col_reg": "등록($)", "col_mon": "연금($)",
        "matching_cv": "매칭 CV", "bonus_usd": "보너스($)", "cycle": "사이클",
        "adil_info": "120게임 중 7.5게임당 1위 ($30 가치의 ADIL 획득 / 시세 $0.4 기준 562.5개)"
    },
    "English": {
        "unit": "People", "title": "📊 DHP & ADIL Total Analysis", "sidebar_h": "📌 Settings",
        "my_p": "My Tier", "my_gc": "Monthly Games", "pa_p": "Partner Tier", "l1": "Direct", "dup": "Dup",
        "m1": "Total Org", "m2": "Total Reg. Bonus", "m3": "Total Monthly", "m4": "Monthly ADIL",
        "tab1": "👥 Unilevel", "tab2": "⚖️ Binary", "tab3": "🚀 ORBIT", "tab4": "🪙 ADIL Value", "tab5": "💸 Cash Flow",
        "exp_init": "Initial Investment", "exp_month": "Monthly Expense", "net_profit": "Net Profit",
        "col_gen": "Gen", "col_people": "People", "col_reg": "Reg($)", "col_mon": "Monthly($)",
        "matching_cv": "Matching CV", "bonus_usd": "Bonus($)", "cycle": "Cycle",
        "adil_info": "1st place in 7.5 out of 120 games ($30 worth of ADIL / 562.5 ADIL at $0.4)"
    },
    "Japanese": {"unit": "人", "title": "📊 DHP & ADIL 総合資産分析", "sidebar_h": "📌 設定", "my_p": "マイパッケージ", "my_gc": "月間プレイ数", "pa_p": "パートナーパッケージ", "l1": "直接紹介", "dup": "複製人数", "m1": "総組織", "m2": "登録報酬計", "m3": "月間報酬計", "m4": "ADIL獲得量", "tab1": "👥 ユニレベル", "tab2": "⚖️ バイナリー", "tab3": "🚀 オービット", "tab4": "🪙 ADIL評価", "tab5": "💸 支出/収益", "exp_init": "初期投資", "exp_month": "月間維持費", "net_profit": "月間純利益", "col_gen": "レベル", "col_people": "人数", "col_reg": "登録($)", "col_mon": "月間($)", "matching_cv": "Matching CV", "bonus_usd": "報酬($)", "cycle": "サイクル", "adil_info": "120ゲーム中7.5回1位 ($30相当のADIL獲得 / 0.4ドル基準 562.5個)"},
    "Chinese": {"unit": "人", "title": "📊 DHP & ADIL 综合资产分析", "sidebar_h": "📌 设置", "my_p": "我的等级", "my_gc": "每月游戏次数", "pa_p": "伙伴等级", "l1": "直接推荐", "dup": "复制", "m1": "总组织", "m2": "总注册奖", "m3": "总月度奖", "m4": "每月 ADIL", "tab1": "👥 多层次", "tab2": "⚖️ 双轨制", "tab3": "🚀 轨道", "tab4": "🪙 ADIL 估值", "tab5": "💸 现金流", "exp_init": "初始投资", "exp_month": "每月支出", "net_profit": "每月净利润", "col_gen": "代", "col_people": "人数", "col_reg": "注册($)", "col_mon": "月度($)", "matching_cv": "Matching CV", "bonus_usd": "奖金($)", "cycle": "循环", "adil_info": "120场游戏中获得7.5场第1名 (价值$30的ADIL / $0.4时为562.5个)"},
    "Thai": {"unit": "คน", "title": "📊 วิเคราะห์ DHP & ADIL ทั้งหมด", "sidebar_h": "📌 ตั้งค่า", "my_p": "ระดับของฉัน", "my_gc": "เกมต่อเดือน", "pa_p": "ระดับพาร์ทเนอร์", "l1": "แนะนำตรง", "dup": "การทำซ้ำ", "m1": "คนรวม", "m2": "โบนัสสมัคร", "m3": "โบนัสรายเดือน", "m4": "ADIL ต่อเดือน", "tab1": "👥 ยูนิเลเวล", "tab2": "⚖️ ไบนารี", "tab3": "🚀 ออร์บิท", "tab4": "🪙 ประเมิน ADIL", "tab5": "💸 วิเคราะห์จ่าย", "exp_init": "เงินลงทุน", "exp_month": "รายจ่ายเดือน", "net_profit": "กำไรสุทธิ", "col_gen": "รุ่น", "col_people": "คน", "col_reg": "สมัคร($)", "col_mon": "รายเดือน($)", "matching_cv": "Matching CV", "bonus_usd": "โบนัส($)", "cycle": "รอบ", "adil_info": "ได้ที่ 1 ใน 7.5 จาก 120 เกม (รับ ADIL มูลค่า $30 / 562.5 ADIL ที่ $0.4)"},
    "Vietnamese": {"unit": "Người", "title": "📊 Phân tích DHP & ADIL tổng thể", "sidebar_h": "📌 Cài đặt", "my_p": "Cấp của tôi", "my_gc": "Lượt chơi/tháng", "pa_p": "Cấp đối tác", "l1": "Trực tiếp", "dup": "Sao chép", "m1": "Tổng tổ chức", "m2": "Thưởng ĐK", "m3": "Thưởng tháng", "m4": "ADIL tháng", "tab1": "👥 Unilevel", "tab2": "⚖️ Binary", "tab3": "🚀 ORBIT", "tab4": "🪙 Định giá ADIL", "tab5": "💸 Dòng tiền", "exp_init": "Vốn ban đầu", "exp_month": "Chi phí tháng", "net_profit": "Lợi nhuận ròng", "col_gen": "Thế hệ", "col_people": "Số người", "col_reg": "Thưởng ĐK", "col_mon": "Thưởng tháng", "matching_cv": "Matching CV", "bonus_usd": "Thưởng($)", "cycle": "Chu kỳ", "adil_info": "Đạt giải nhất 7.5 trong 120 trận (Nhận $30 ADIL / 562.5 ADIL tại $0.4)"}
}
t = t_all.get(lang, t_all["Korean"])

# --- 3. 핵심 계산 로직 ---
st.sidebar.header(t["sidebar_h"])
my_p = st.sidebar.selectbox(t["my_p"], list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input(t["my_gc"], value=120, min_value=120, step=120)
pa_p = st.sidebar.selectbox(t["pa_p"], list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input(t["l1"], value=2, min_value=1)
dup = st.sidebar.radio(t["dup"], [2, 3], index=0)

# ADIL 및 지출 (120게임 사이클 당 562.5 ADIL 획득으로 정정)
total_adil_per_cycle = 562.5 
my_adil = (my_gc / 120) * total_adil_per_cycle

init_exp = pkgs[my_p]["price"] + 60
base_sub = (my_gc / 120) * 110.25 
cv_short = max(0.0, 72.0 - (my_gc * 20 * pkgs[my_p]["self_rate"]))
month_exp = base_sub + (cv_short * 2.0) 

# 보너스 계산
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
    stats.append({
        t["col_gen"]: f"{i} Gen", t["col_people"]: f"{int(curr)}",
        t["col_reg"]: f"{(r_cv * rates[i]):.1f}", t["col_mon"]: f"{(m_cv * rates[i]):.1f}"
    })

# 바이너리 & 오빗
bin_rate = pkgs[my_p]["bin"]
matching_reg_cv = t_reg_cv / 2
matching_mon_cv = t_mon_cv / 2
bin_reg_bonus = matching_reg_cv * bin_rate
bin_mon_bonus = matching_mon_cv * bin_rate

orb_cycle_reg = int(matching_reg_cv // 5460)
orb_reg_bonus = orb_cycle_reg * 450
orb_cycle_mon = int(matching_mon_cv // 5460)
orb_mon_bonus = orb_cycle_mon * 450

total_reg_bonus = sum([float(s[t["col_reg"]]) for s in stats]) + bin_reg_bonus + orb_reg_bonus
total_mon_bonus = sum([float(s[t["col_mon"]]) for s in stats]) + bin_mon_bonus + orb_mon_bonus
net_profit = total_mon_bonus - month_exp

# --- 4. 화면 출력 ---
st.title(t["title"])

# [추가된 부분] 참고용 비용 안내 메뉴 (최종 손익에 미포함)
with st.expander("ℹ️ 참고용 비용 안내 (Reference Cost Info)"):
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.write(f"**🔹 초기 등록 비용:** `${pkgs[my_p]['price'] + 60:,.1f}`")
        st.caption("(패키지 가격 + 가입비 $60 포함)")
    with col_info2:
        st.write(f"**🔹 월간 예상 게임 비용:** `${(my_gc / 120) * 110.25:,.1f}`")
        st.caption("(120게임당 구독료 $110.25 기준, CV 부족분 제외)")

st.divider()

# 메트릭 출력 (기존과 동일)
m1, m2, m3, m4 = st.columns(4)
m1.metric(t["m1"], f"{total_people} {t['unit']}")
m2.metric(t["m2"], f"${total_reg_bonus:,.1f}")
m3.metric(t["m3"], f"${total_mon_bonus:,.1f}")
m4.metric(t["m4"], f"{my_adil:,.1f} ADIL")

# ... 이하 생략 (기존 탭 구조 유지) ...
