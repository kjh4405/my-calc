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

# --- 2. 6개 국어 사전 (사용자 일본어 번역 절대 보존) ---
lang_options = ["Korean", "English", "Japanese", "Chinese", "Thai", "Vietnamese"]
lang = st.sidebar.selectbox("🌐 Select Language", lang_options)

t_all = {
    "Korean": {
        "unit": "명", "title": "📊 DHP 글로벌 수익 및 ADIL 자산 분석", "sidebar_h": "📌 조건 입력",
        "my_p": "내 패키지 등급", "my_gc": "나의 월 게임수", "pa_p": "파트너 패키지 등급", "l1": "직접 소개", "dup": "복제",
        "m1": "총 조직", "m2": "총 가입 보너스", "m3": "월 보너스 합계", "m4": "ADIL 월 획득량",
        "tab1": "👥 유니레벨", "tab2": "⚖️ 바이너리", "tab3": "🚀 오빗(ORBIT)", "tab4": "🪙 ADIL 가치", "tab5": "💸 지출/수익",
        "exp_init": "초기 투자금 (패키지+가입비)", "exp_month": "고정 월 유지비", "net_profit": "월 예상 순수익",
        "col_gen": "세대", "col_people": "인원", "col_reg": "등록($)", "col_mon": "연금($)",
        "matching_cv": "매칭 CV", "bonus_usd": "보너스($)", "cycle": "사이클",
        "adil_info": "120게임 중 7.5게임당 1위 ($30 가치의 ADIL 획득 / 시세 $0.4 기준 562.5개)",
        "ref_title": "ℹ️ 참고용 비용 안내", "ref_init": "🔹 초기 등록 비용", "ref_month": "🔹 월간 유지 비용 상세",
        "ref_init_sub": "(패키지 가격 + 가입비 $60 포함)", "ref_low_sub": "(고정 유지비 $110.25 + 72 CV 유지를 위한 추가비용 포함)",
        "ref_high_sub": "(고정 유지비 $110.25로 모든 조건 충족)",
        "profit_info": "💡 순수익은 매달 발생하는 보너스 합계에서 고정 유지비($110.25)를 차감하여 계산됩니다."
    },
    "English": {
        "unit": "People", "title": "📊 DHP & ADIL Total Analysis", "sidebar_h": "📌 Settings",
        "my_p": "My Tier", "my_gc": "Monthly Games", "pa_p": "Partner Tier", "l1": "Direct", "dup": "Dup",
        "m1": "Total Org", "m2": "Total Reg. Bonus", "m3": "Total Monthly", "m4": "Monthly ADIL",
        "tab1": "👥 Unilevel", "tab2": "⚖️ Binary", "tab3": "🚀 ORBIT", "tab4": "🪙 ADIL Value", "tab5": "💸 Cash Flow",
        "exp_init": "Initial Investment", "exp_month": "Fixed Monthly Expense", "net_profit": "Net Monthly Profit",
        "col_gen": "Gen", "col_people": "People", "col_reg": "Reg($)", "col_mon": "Monthly($)",
        "matching_cv": "Matching CV", "bonus_usd": "Bonus($)", "cycle": "Cycle",
        "adil_info": "1st place in 7.5 out of 120 games ($30 worth of ADIL / 562.5 ADIL at $0.4)",
        "ref_title": "ℹ️ Reference Cost Info", "ref_init": "🔹 Initial Registration Cost", "ref_month": "🔹 Monthly Maintenance Detail",
        "ref_init_sub": "(Includes Pkg + $60 fee)", "ref_low_sub": "(Fixed $110.25 + extra cost for 72 CV)",
        "ref_high_sub": "(Fixed $110.25 covers everything)",
        "profit_info": "💡 Net profit is calculated by subtracting the fixed expense ($110.25) from total monthly bonuses."
    },
    "Japanese": {
        "unit": "人", "title": "📊 DHP & ADIL 総合資産分析", "sidebar_h": "📌 設定", "my_p": "マイパッケージ", "my_gc": "月間プレイ数", "pa_p": "パートナーパッケージ", "l1": "直接紹介", "dup": "複製人数", "m1": "総組織", "m2": "등록報酬計", "m3": "月間報酬計", "m4": "ADIL獲得量", "tab1": "👥 ユニレベル", "tab2": "⚖️ 바이너리", "tab3": "🚀 オービット", "tab4": "🪙 ADIL評価", "tab5": "💸 支出/収益", "exp_init": "初期投資", "exp_month": "固定月間維持費", "net_profit": "月間純利益", "col_gen": "レベル", "col_people": "人数", "col_reg": "登録($)", "col_mon": "月間($)", "matching_cv": "Matching CV", "bonus_usd": "報酬($)", "cycle": "サイクル", "adil_info": "120ゲーム中7.5回1位 ($30相当のADIL獲得 / 0.4ドル基準 562.5個)",
        "ref_title": "ℹ️ 参考用費用案内", "ref_init": "🔹 初期登録費用", "ref_month": "🔹 月間維持費詳細",
        "ref_init_sub": "(パッケージ価格 + 加入費 $60 含む)", "ref_low_sub": "(固定維持費 $110.25 + 72 CV維持の追加費用含む)",
        "ref_high_sub": "(固定維持費 $110.25ですべて充足)",
        "profit_info": "💡 純利益は、毎月の報酬合計から固定維持費($110.25)を差し引いて計算されます。"
    },
    "Chinese": {"unit": "人", "title": "📊 DHP & ADIL 综合资产分析", "sidebar_h": "📌 设置", "my_p": "我的等级", "my_gc": "每月游戏次数", "pa_p": "伙伴等级", "l1": "直接推荐", "dup": "复制", "m1": "总组织", "m2": "总注册奖", "m3": "总月度奖", "m4": "每月 ADIL", "tab1": "👥 多层次", "tab2": "⚖️ 双轨制", "tab3": "🚀 轨道", "tab4": "🪙 ADIL 估值", "tab5": "💸 现金流", "exp_init": "初始投资", "exp_month": "固定每月支出", "net_profit": "每月净利润", "col_gen": "代", "col_people": "人数", "col_reg": "注册($)", "col_mon": "月度($)", "matching_cv": "Matching CV", "bonus_usd": "奖金($)", "cycle": "循环", "adil_info": "120场游戏中获得7.5场第1名 (价值$30的ADIL / $0.4时为562.5个)", "ref_title": "ℹ️ 参考费用信息", "ref_init": "🔹 初始注册费用", "ref_month": "🔹 每月维持费明细", "ref_init_sub": "(含套餐 + $60 注册费)", "ref_low_sub": "(含 $110.25 固定费 + 72 CV 额外费)", "ref_high_sub": "(固定 $110.25 覆盖所有条件)", "profit_info": "💡 净利润通过从每月奖金总额中减去固定支出 ($110.25) 计算得出。"},
    "Thai": {"unit": "คน", "title": "📊 วิเคราะห์ DHP & ADIL ทั้งหมด", "sidebar_h": "📌 ตั้งค่า", "my_p": "ระดับของฉัน", "my_gc": "เกมต่อเดือน", "pa_p": "ระดับพาร์ทเนอร์", "l1": "แนะนำตรง", "dup": "การทำซ้ำ", "m1": "คนรวม", "m2": "โบนัสสมัคร", "m3": "โบนัสรายเดือน", "m4": "ADIL ต่อเดือน", "tab1": "👥 ยูนิเลเวล", "tab2": "⚖️ ไบนารี", "tab3": "🚀 ออร์บิท", "tab4": "🪙 ประเมิน ADIL", "tab5": "💸 วิเคราะห์จ่าย", "exp_init": "เงินลงทุน", "exp_month": "ค่าบำรุงรายเดือนคงที่", "net_profit": "กำไรสุทธิรายเดือน", "col_gen": "รุ่น", "col_people": "คน", "col_reg": "สมัคร($)", "col_mon": "รายเดือน($)", "matching_cv": "Matching CV", "bonus_usd": "โบนัส($)", "cycle": "รอบ", "adil_info": "ได้ที่ 1 ใน 7.5 จาก 120 เกม (รับ ADIL มูลค่า $30 / 562.5 ADIL ที่ $0.4)", "ref_title": "ℹ️ ข้อมูลค่าใช้จ่ายอ้างอิง", "ref_init": "🔹 ค่าลงทะเบียนเริ่มต้น", "ref_month": "🔹 รายละเอียดค่าบำรุงรายเดือน", "ref_init_sub": "(รวมแพ็คเกจ + ค่าธรรมเนียม $60)", "ref_low_sub": "(รวมค่าบำรุงคงที่ $110.25 + ค่าธรรมเนียมเพิ่มเติมสำหรับ 72 CV)", "ref_high_sub": "($110.25 ครอบคลุมเงื่อนไขทั้งหมด)", "profit_info": "💡 กำไรสุทธิคำนวณโดยนำโบนัสรวมรายเดือนลบด้วยรายจ่ายคงที่ ($110.25)"},
    "Vietnamese": {"unit": "Người", "title": "📊 Phân tích DHP & ADIL tổng thể", "sidebar_h": "📌 Cài đặt", "my_p": "Cấp của tôi", "my_gc": "Lượt chơi/tháng", "pa_p": "Cấp đối tác", "l1": "Trực tiếp", "dup": "Sao chép", "m1": "Tổng tổ chức", "m2": "Thưởng ĐK", "m3": "Thưởng tháng", "m4": "ADIL tháng", "tab1": "👥 Unilevel", "tab2": "⚖️ Binary", "tab3": "🚀 ORBIT", "tab4": "🪙 Định giá ADIL", "tab5": "💸 Dòng tiền", "exp_init": "Vốn ban đầu", "exp_month": "Chi phí duy trì cố định", "net_profit": "Lợi nhuận ròng hàng tháng", "col_gen": "Thế hệ", "col_people": "Số người", "col_reg": "Thưởng ĐK", "col_mon": "Thưởng tháng", "matching_cv": "Matching CV", "bonus_usd": "Thưởng($)", "cycle": "Chu kỳ", "adil_info": "Đạt giải nhất 7.5 trong 120 trận (Nhận $30 ADIL / 562.5 ADIL tại $0.4)", "ref_title": "ℹ️ Thông tin chi phí tham khảo", "ref_init": "🔹 Chi phí đăng ký ban đầu", "ref_month": "🔹 Chi tiết chi phí duy trì hàng tháng", "ref_init_sub": "(Bao gồm gói + phí $60)", "ref_low_sub": "(Gồm $110.25 cố định + chi phí bổ sung cho 72 CV)", "ref_high_sub": "(Cố định $110.25 đáp ứng mọi điều kiện)", "profit_info": "💡 Lợi nhuận ròng được tính bằng cách lấy tổng thưởng hàng tháng trừ đi chi phí cố định ($110.25)"}
}
t = t_all.get(lang, t_all["Korean"])

# --- 3. 핵심 계산 로직 ---
st.sidebar.header(t["sidebar_h"])
my_p = st.sidebar.selectbox(t["my_p"], list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input(t["my_gc"], value=120, min_value=120, step=120)
pa_p = st.sidebar.selectbox(t["pa_p"], list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input(t["l1"], value=2, min_value=1)
dup = st.sidebar.radio(t["dup"], [2, 3], index=0)

# ADIL 계산
total_adil_per_cycle = 562.5 
my_adil = (my_gc / 120) * total_adil_per_cycle

# 지출 계산 (수정 로직 반영)
init_exp = pkgs[my_p]["price"] + 60
fixed_monthly_exp = (my_gc / 120) * 110.25  # 모든 패키지 공통 고정 유지비

# Basic/Standard 추가 비용 로직
my_earned_cv = my_gc * 20 * pkgs[my_p]["self_rate"]
cv_short = max(0.0, 72.0 - my_earned_cv)
extra_fee = cv_short * 2.0 if my_p in ["Basic", "Standard"] else 0.0
total_maintenance = fixed_monthly_exp + extra_fee # 참고용 총 지출

# 보너스 계산
p_reg_cv = pkgs[pa_p]["reg_cv"]
p_mon_cv = 72.0 if pkgs[pa_p]["self_rate"] >= 0.03 else 36.0
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05, 5: 0.02}
stats = []; total_people = 0; t_reg_cv = 0; t_mon_cv = 0; curr = l1
for i in range(1, 6):
    if i > 1: curr *= dup
    total_people += curr
    r_cv = curr * p_reg_cv
    m_cv = curr * (my_gc / 120 * p_mon_cv)
    t_reg_cv += r_cv; t_mon_cv += m_cv
    stats.append({t["col_gen"]: f"{i} Gen", t["col_people"]: f"{int(curr)}", t["col_reg"]: f"{(r_cv * rates[i]):.1f}", t["col_mon"]: f"{(m_cv * rates[i]):.1f}"})

bin_rate = pkgs[my_p]["bin"]; matching_reg_cv = t_reg_cv / 2; matching_mon_cv = t_mon_cv / 2
bin_reg_bonus = matching_reg_cv * bin_rate; bin_mon_bonus = matching_mon_cv * bin_rate
orb_cycle_reg = int(matching_reg_cv // 5460); orb_reg_bonus = orb_cycle_reg * 450
orb_cycle_mon = int(matching_mon_cv // 5460); orb_mon_bonus = orb_cycle_mon * 450
total_reg_bonus = sum([float(s[t["col_reg"]]) for s in stats]) + bin_reg_bonus + orb_reg_bonus
total_mon_bonus = sum([float(s[t["col_mon"]]) for s in stats]) + bin_mon_bonus + orb_mon_bonus

# 순이익 계산 (보너스 합계 - 고정 유지비)
net_profit = total_mon_bonus - fixed_monthly_exp

# --- 4. 화면 출력 ---
st.title(t["title"])

# 참고용 비용 안내 (지출 구조 명확화)
with st.expander(t["ref_title"]):
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.write(f"**{t['ref_init']}:** `${init_exp:,.2f}`")
        st.caption(t["ref_init_sub"])
    with col_info2:
        st.write(f"**{t['ref_month']}:** `${total_maintenance:,.2f}`")
        if my_p in ["Basic", "Standard"]:
            st.caption(t["ref_low_sub"])
        else:
            st.caption(t["ref_high_sub"])

st.divider()

m1, m2, m3, m4 = st.columns(4)
m1.metric(t["m1"], f"{total_people} {t['unit']}")
m2.metric(t["m2"], f"${total_reg_bonus:,.2f}")
m3.metric(t["m3"], f"${total_mon_bonus:,.2f}")
m4.metric(t["m4"], f"{my_adil:,.1f} ADIL")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"], t["tab5"]])

with tab1: st.table(pd.DataFrame(stats))
with tab2:
    st.subheader(t["tab2"])
    st.table(pd.DataFrame({"Type": ["Registration", "Monthly"], t["matching_cv"]: [f"{matching_reg_cv:,.1f}", f"{matching_mon_cv:,.1f}"], t["bonus_usd"]: [f"${bin_reg_bonus:,.1f}", f"${bin_mon_bonus:,.1f}"]}))
with tab3:
    st.subheader(t["tab3"])
    st.table(pd.DataFrame({"Type": ["Registration", "Monthly"], t["cycle"]: [f"{orb_cycle_reg}x", f"{orb_cycle_mon}x"], t["bonus_usd"]: [f"${orb_reg_bonus:,.1f}", f"${orb_mon_bonus:,.1f}"]}))
with tab4:
    st.subheader(t["tab4"])
    st.info(f"💡 {t['adil_info']}")
    prices = [0.4, 1.0, 2.0, 5.0]
    st.table(pd.DataFrame([{"ADIL Price": f"${p}", "Value": f"${(my_adil*p):,.1f}"} for p in prices]))
with tab5:
    st.info(t["profit_info"])
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**🔴 {t['exp_init']}:** `${init_exp:,.2f}`")
        st.write(f"**🟠 {t['exp_month']}:** `${fixed_monthly_exp:,.2f}`")
    with c2: st.success(f"**💰 {t['net_profit']}: ${net_profit:,.2f}**")
