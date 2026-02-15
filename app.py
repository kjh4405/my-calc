import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP Global Multi-Lang Analyzer", layout="wide")

# --- 1. 데이터 정의 (보존된 수치) ---
pkgs = {
    "Basic": {"price": 120, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 480, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1200, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2640, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 6}
}

# --- 2. 6개 국어 텍스트 사전 정의 (무삭제 전체본) ---
st.sidebar.header("🌐 Language Settings")
lang = st.sidebar.selectbox("Select Language", ["Korean", "English", "Japanese", "Chinese", "Thai", "Vietnamese"])

if lang == "Korean":
    t = {
        "title": "🚀 DHP 비지니스 종합 수익 분석", "sidebar_h": "📌 설정",
        "my_p": "내 패키지 등급", "my_gc": "나의 월 게임수 (120단위)", "pa_p": "파트너 패키지 등급", "l1": "1대 직접소개 인원", "dup": "하위 복제 인원",
        "m1": "총 산하 인원 (4대 고정)", "m2": "초기 비용", "m3": "월 지출액", "m4": "총 등록 보너스", "m5": "월 연금 수익", "m6": "초기비용 리쿱 시기",
        "tab1": "📊 보너스 상세내역", "tab2": "💰 ADIL 기대수익", "tab3": "💳 지출/구조 상세", "tab4": "📜 보너스 계산 공식",
        "recoup_now": "즉시 회수 완료", "recoup_month": "개월 후 회수", "recoup_desc": "💡 리쿱 이후 월 연금 수익은 전액 순수익이 됩니다.",
        "f_one": "1회성 등록 보너스 공식", "f_mon": "매달 연금 보너스 공식",
        "adil_h": "🪙 ADIL 토큰 가치 분석", "adil_info": "120게임당 7.5회 1위 당첨 확률을 기반으로 한 가치 분석입니다.",
        "listing": "ADIL 시세", "hold_v": "보유 가치", "win_v": "1위 당첨 기대가치"
    }
elif lang == "English":
    t = {
        "title": "🚀 DHP Business Revenue Analysis", "sidebar_h": "📌 Settings",
        "my_p": "My Package Tier", "my_gc": "Monthly Games (120)", "pa_p": "Partner Tier", "l1": "Direct Referrals", "dup": "Duplication",
        "m1": "Total Org (4 Gen)", "m2": "Initial Cost", "m3": "Monthly Exp.", "m4": "Total Reg. Bonus", "m5": "Recurring Income", "m6": "Recoup Period",
        "tab1": "📊 Bonus Details", "tab2": "💰 ADIL Projection", "tab3": "💳 Breakdown", "tab4": "📜 Formula",
        "recoup_now": "Instantly Recouped", "recoup_month": "Months to Recoup", "recoup_desc": "💡 After recoup, all recurring income is net profit.",
        "f_one": "Registration Bonus Formula", "f_mon": "Monthly Recurring Bonus Formula",
        "adil_h": "🪙 ADIL Token Value Analysis", "adil_info": "Analysis based on 7.5 wins per 120 games.",
        "listing": "ADIL Price", "hold_v": "Holding Value", "win_v": "1st Place Value"
    }
elif lang == "Japanese":
    t = {
        "title": "🚀 DHP ビジネス総合収益分析", "sidebar_h": "📌 設定",
        "my_p": "自分のパッケージ", "my_gc": "月間プレイ回数", "pa_p": "パートナー等級", "l1": "直接紹介人数", "dup": "複製人数",
        "m1": "総組織人数 (4代固定)", "m2": "初期費用", "m3": "月間支出", "m4": "登録ボーナス合計", "m5": "月間権利収入", "m6": "リクープ時期",
        "tab1": "📊 ボーナス詳細", "tab2": "💰 ADIL期待収益", "tab3": "💳 支出詳細", "tab4": "📜 計算公式",
        "recoup_now": "即時回収完了", "recoup_month": "ヶ月後に回収", "recoup_desc": "💡 リクープ以降、月間権利収入はすべて純利益になります。",
        "f_one": "登録ボーナス公式", "f_mon": "月間権利収入公式",
        "adil_h": "🪙 ADILトークン価値分析", "adil_info": "120ゲームあたり7.5回の当選確率に基づいています。",
        "listing": "ADIL価格", "hold_v": "保有価値", "win_v": "当選期待価値"
    }
elif lang == "Chinese":
    t = {
        "title": "🚀 DHP 业务综合收益分析", "sidebar_h": "📌 设置",
        "my_p": "我的套餐等级", "my_gc": "每月游戏次数", "pa_p": "伙伴套餐等级", "l1": "直接推荐人数", "dup": "复制人数",
        "m1": "总组织人数 (固定4代)", "m2": "初始费用", "m3": "每月支出", "m4": "总注册奖金", "m5": "每月年金收益", "m6": "回本周期",
        "tab1": "📊 奖金详情", "tab2": "💰 ADIL 预期收益", "tab3": "💳 支出详情", "tab4": "📜 计算公式",
        "recoup_now": "即刻回本", "recoup_month": "个月后回本", "recoup_desc": "💡 回本后，每月年金收益即为纯利润。",
        "f_one": "注册奖金公式", "f_mon": "每月年金收益公式",
        "adil_h": "🪙 ADIL 代币价值分析", "adil_info": "基于每120场比赛7.5次中奖概率进行分析。",
        "listing": "ADIL 价格", "hold_v": "持有价值", "win_v": "中奖预期价值"
    }
elif lang == "Thai":
    t = {
        "title": "🚀 DHP วิเคราะห์รายได้รวม", "sidebar_h": "📌 การตั้งค่า",
        "my_p": "ระดับแพ็คเกจ", "my_gc": "จำนวนเกม/เดือน", "pa_p": "ระดับพาร์ทเนอร์", "l1": "ผู้แนะนำตรง", "dup": "การทำซ้ำ",
        "m1": "รวมคน (4 รุ่น)", "m2": "ต้นทุนเริ่มต้น", "m3": "จ่ายรายเดือน", "m4": "โบนัสสมัคร", "m5": "รายได้ต่อเนื่อง", "m6": "ระยะเวลาคืนทุน",
        "tab1": "📊 รายละเอียด", "tab2": "💰 ADIL คาดการณ์", "tab3": "💳 โครงสร้าง", "tab4": "📜 สูตรคำนวณ",
        "recoup_now": "คืนทุนทันที", "recoup_month": "เดือนเพื่อคืนทุน", "recoup_desc": "💡 หลังคืนทุน รายได้ต่อเนื่องจะเป็นกำไรสุทธิทั้งหมด",
        "f_one": "สูตรโบนัสสมัคร", "f_mon": "สูตรรายได้รายเดือน",
        "adil_h": "🪙 วิเคราะห์ ADIL", "adil_info": "วิเคราะห์จากโอกาสชนะ 7.5 ครั้ง ต่อ 120 เกม",
        "listing": "ราคา ADIL", "hold_v": "มูลค่าถือครอง", "win_v": "มูลค่าคาดชนะ"
    }
else: # Vietnamese
    t = {
        "title": "🚀 Phân tích thu nhập DHP", "sidebar_h": "📌 Cài đặt",
        "my_p": "Cấp gói của tôi", "my_gc": "Lượt chơi hàng tháng", "pa_p": "Cấp gói đối tác", "l1": "Số người F1", "dup": "Tỷ lệ sao chép",
        "m1": "Tổng thành viên (4 cấp)", "m2": "Vốn ban đầu", "m3": "Chi phí hàng tháng", "m4": "Tổng thưởng đăng ký", "m5": "Thu nhập thụ động", "m6": "Hồi vốn sau",
        "tab1": "📊 Chi tiết thưởng", "tab2": "💰 Dự báo ADIL", "tab3": "💳 Chi tiết chi phí", "tab4": "📜 Công thức",
        "recoup_now": "Hồi vốn ngay lập tức", "recoup_month": "tháng để hồi vốn", "recoup_desc": "💡 Sau khi hồi vốn, thu nhập thụ động là lợi nhuận ròng.",
        "f_one": "Công thức thưởng đăng ký", "f_mon": "Công thức thưởng hàng tháng",
        "adil_h": "🪙 Phân tích Token ADIL", "adil_info": "Dựa trên tỷ lệ thắng 7.5 lần mỗi 120 lượt chơi.",
        "listing": "Giá ADIL", "hold_v": "Giá trị giữ", "win_v": "Giá trị kỳ vọng thắng"
    }

# --- 3. 메인 입력 영역 ---
st.title(t["title"])
st.sidebar.header(t["sidebar_h"])
my_p = st.sidebar.selectbox(t["my_p"], list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input(t["my_gc"], value=120, min_value=120, step=120)
pa_p = st.sidebar.selectbox(t["pa_p"], list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input(t["l1"], value=2, min_value=1)
dup = st.sidebar.radio(t["dup"], [2, 3], index=0)

# --- 4. 핵심 계산 로직 (4대 고정 인원 및 수당) ---
init_cost = pkgs[my_p]["price"] + 60
base_game_cost = (my_gc / 120) * 110.25 
my_gen_cv = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0.0, 72.0 - my_gen_cv)
shortfall_fee = cv_shortfall * 2.0 
monthly_exp = base_game_cost + shortfall_fee

p_reg_cv_value = pkgs[pa_p]["reg_cv"]
# 게임 CV: 프리미엄/얼티밋은 72, 나머지는 36 적용
p_game_cv_value = 72.0 if pkgs[pa_p]["self_rate"] == 0.03 else 36.0
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05}

stats = []
t_reg_cv = t_game_cv = total_people = 0
curr = l1

# 4대까지 고정 인원 및 유니레벨 CV 계산
for i in range(1, 5):
    if i > 1: curr *= dup
    total_people += curr
    r_cv = curr * p_reg_cv_value
    g_cv = curr * (my_gc / 120 * p_game_cv_value)
    t_reg_cv += r_cv
    t_game_cv += g_cv
    stats.append({
        "Gen": f"{i} Gen", 
        "num": curr, 
        "r_u": r_cv * rates[i], 
        "m_u": g_cv * rates[i], 
        "rt": f"{int(rates[i]*100)}%"
    })

# 바이너리 & 오빗 계산
w_reg_cv, w_mon_cv = t_reg_cv / 2, t_game_cv / 2
bin_reg = w_reg_cv * pkgs[my_p]["bin"]
bin_mon = w_mon_cv * pkgs[my_p]["bin"]
orb_reg = int(w_reg_cv // 5460) * 450
orb_mon = int(w_mon_cv // 5460) * 450

total_reg_bonus = sum(s['r_u'] for s in stats) + bin_reg + orb_reg
total_mon_bonus = sum(s['m_u'] for s in stats) + bin_mon + orb_mon

# 리쿱 시기 계산
net_monthly_profit = total_mon_bonus - monthly_exp
if total_reg_bonus >= init_cost:
    recoup_result = t["recoup_now"]
else:
    if net_monthly_profit > 0:
        months = (init_cost - total_reg_bonus) / net_monthly_profit
        recoup_result = f"{months:.1f} {t['recoup_month']}"
    else:
        recoup_result = "N/A"

# --- 5. 결과 메트릭 출력 ---
st.divider()
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric(t["m1"], f"{total_people:,}")
m2.metric(t["m2"], f"${init_cost:,}")
m3.metric(t["m3"], f"${monthly_exp:,.2f}")
m4.metric(t["m4"], f"${total_reg_bonus:,.0f}")
m5.metric(t["m5"], f"${total_mon_bonus:,.1f}")
m6.metric(t["m6"], recoup_result)
st.write(f"*{t['recoup_desc']}*")

# --- 6. 상세 분석 탭 ---
tabs = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"]])

with tabs[0]: # 보너스 상세
    detail_data = [
        {"Bonus Type": "Unilevel", "One-time (Reg)": f"${sum(s['r_u'] for s in stats):,.1f}", "Monthly (Recur)": f"${sum(s['m_u'] for s in stats):,.1f}"},
        {"Bonus Type": "Binary", "One-time (Reg)": f"${bin_reg:,.1f}", "Monthly (Recur)": f"${bin_mon:,.1f}"},
        {"Bonus Type": "Orbit", "One-time (Reg)": f"${orb_reg:,.0f}", "Monthly (Recur)": f"${orb_mon:,.0f}"},
    ]
    st.table(pd.DataFrame(detail_data))

with tabs[1]: # ADIL 수익 시뮬레이션
    game_unit = my_gc / 120
    adil_count = 562.5 * game_unit
    win_count = 7.5 * game_unit
    st.subheader(f"{t['adil_h']} ({adil_count:,.1f} ADIL)")
    st.info(f"💡 {t['adil_info']}")
    prices = [0.4, 0.5, 0.8, 1.0]
    adil_results = []
    for p in prices:
        hold_val = adil_count * p
        exp_val = hold_val + (win_count * p * 10) # 1위 당첨 시 추가 가치 보정
        adil_results.append({t["listing"]: f"${p}", t["hold_v"]: f"${hold_val:,.1f}", t["win_v"]: f"${exp_val:,.1f}"})
    st.table(pd.DataFrame(adil_results))

with tabs[2]: # 지출 및 구조 상세
    st.write(pd.DataFrame(stats)[["Gen", "num", "rt"]].rename(columns={"num":"People", "rt":"Rate"}))

with tabs[3]: # 수식 공개 (LaTeX)
    st.subheader(t["tab4"])
    c_one, c_mon = st.columns(2)
    with c_one:
        st.markdown(f"### 🟢 {t['f_one']}")
        st.latex(r"Unilevel = \sum_{n=1}^{4} (PartnerCV \times Rate_n)")
        st.latex(r"Binary = \frac{\sum RegCV}{2} \times MyRate")
        st.latex(r"Orbit = \lfloor \frac{\sum RegCV / 2}{5460} \rfloor \times \$450")
    with c_mon:
        st.markdown(f"### 🔵 {t['f_mon']}")
        st.latex(r"Unilevel = \sum_{n=1}^{4} (GameCV \times Rate_n)")
        st.latex(r"Binary = \frac{\sum GameCV}{2} \times MyRate")
        st.latex(r"Orbit = \lfloor \frac{\sum GameCV / 2}{5460} \rfloor \times \$450")
    st.info("CV Reference: 120 Games = 36 CV (Basic/Standard) / 72 CV (Premium/Ultimate)")

# --- 7. 리쿱 시점 차트 시각화 (추가) ---
st.divider()
st.subheader("📈 Cumulative Cash Flow Projection")
months_range = list(range(0, 13))
cash_flow = []
for m in months_range:
    if m == 0:
        val = total_reg_bonus - init_cost
    else:
        val = (total_reg_bonus - init_cost) + (net_monthly_profit * m)
    cash_flow.append(val)

chart_data = pd.DataFrame({"Month": months_range, "Net Balance ($)": cash_flow})
st.line_chart(chart_data.set_index("Month"))
