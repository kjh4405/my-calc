import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHP Global Multi-Lang Analyzer", layout="wide")

# --- 1. 데이터 정의 ---
pkgs = {
    "Basic": {"price": 120, "reg_cv": 72, "bin": 0.05, "self_rate": 0.015, "lim": 2},
    "Standard": {"price": 480, "reg_cv": 216, "bin": 0.06, "self_rate": 0.015, "lim": 3},
    "Premium": {"price": 1200, "reg_cv": 504, "bin": 0.07, "self_rate": 0.03, "lim": 4},
    "Ultimate": {"price": 2640, "reg_cv": 1080, "bin": 0.08, "self_rate": 0.03, "lim": 6}
}

# --- 2. 6개 국어 통합 사전 ---
lang_options = ["Korean", "English", "Japanese", "Chinese", "Thai", "Vietnamese"]
lang = st.sidebar.selectbox("🌐 Select Language", lang_options)

t_all = {
    "Korean": {
        "title": "📊 DHP 글로벌 수익 상세 리포트",
        "sidebar_h": "📌 조건 입력",
        "my_p": "내 패키지 등급", "my_gc": "나의 월 게임수 (120단위)", "pa_p": "파트너 패키지 등급", "l1": "직접 소개 인원 (1대)", "dup": "복제 인원 (2~5대)",
        "m1": "총 산하 인원", "m2": "총 가입 보너스", "m3": "매월 연금 보너스", "m4": "월 예상 순수익",
        "tab1": "👥 유니레벨 상세", "tab2": "⚖️ 바이너리 상세", "tab3": "🚀 오빗(ORBIT) 상세",
        "recoup_h": "💰 원금 회수(Recoup) 최종 해설", "recoup_now": "🎉 즉시 회수 완료!", "recoup_wait": "예상 원금 회수 시점:",
        "recoup_desc": "💡 리쿱 이후 발생하는 모든 보너스는 순수익이 됩니다.", "init_cost": "초기 투자금",
        "u_desc": "세대별 파트너 실적(CV)에 따른 요율 보너스", "b_desc": "팀 소실적 매칭 보너스", "o_desc": "5,460 CV 달성 시 추가 보너스"
    },
    "English": {
        "title": "📊 DHP Business Detail Report",
        "sidebar_h": "📌 Settings",
        "my_p": "My Tier", "my_gc": "Monthly Games (120)", "pa_p": "Partner Tier", "l1": "Direct Referrals (1st)", "dup": "Duplication (2-5th)",
        "m1": "Total Org", "m2": "Total Reg. Bonus", "m3": "Monthly Bonus", "m4": "Net Profit",
        "tab1": "👥 Unilevel", "tab2": "⚖️ Binary", "tab3": "🚀 ORBIT",
        "recoup_h": "💰 Recoup Analysis", "recoup_now": "🎉 Instantly Recouped!", "recoup_wait": "Estimated Recoup Period:",
        "recoup_desc": "💡 All bonuses after recoup are 100% net profit.", "init_cost": "Initial Investment",
        "u_desc": "Generation-based CV rate bonus", "b_desc": "Team weak-leg matching bonus", "o_desc": "Extra bonus per 5,460 CV"
    },
    "Japanese": {
        "title": "📊 DHP 収益詳細レポート",
        "sidebar_h": "📌 設定",
        "my_p": "自分のパッケージ", "my_gc": "月間プレイ数", "pa_p": "パートナー等級", "l1": "直接紹介 (1代)", "dup": "複製人数 (2-5代)",
        "m1": "総組織人数", "m2": "登録ボーナス合計", "m3": "月間権利収入", "m4": "月間純利益",
        "tab1": "👥 ユニレベル", "tab2": "⚖️ バイナリ", "tab3": "🚀 ORBIT",
        "recoup_h": "💰 原価回収(Recoup)解説", "recoup_now": "🎉 即時回収完了！", "recoup_wait": "予想回収時期:",
        "recoup_desc": "💡 回収後のすべてのボーナスは純利益になります。", "init_cost": "初期投資額",
        "u_desc": "世代別のCV率に基づくボーナス", "b_desc": "チームの小実績マッチングボーナス", "o_desc": "5,460 CV達成時の追加ボーナス"
    },
    "Chinese": {
        "title": "📊 DHP 业务收益详细报告",
        "sidebar_h": "📌 设置",
        "my_p": "我的等级", "my_gc": "每月游戏次数", "pa_p": "伙伴等级", "l1": "直接推荐 (1代)", "dup": "复制人数 (2-5代)",
        "m1": "总组织人数", "m2": "总注册奖金", "m3": "每月年金收益", "m4": "每月净利润",
        "tab1": "👥 多层次", "tab2": "⚖️ 双轨制", "tab3": "🚀 轨道(ORBIT)",
        "recoup_h": "💰 回本周期分析", "recoup_now": "🎉 即刻回本！", "recoup_wait": "预计回本时间:",
        "recoup_desc": "💡 回本后的所有奖金均为纯利润。", "init_cost": "初始投资",
        "u_desc": "基于世代CV比率的奖金", "b_desc": "团队小对碰奖金", "o_desc": "每达 5,460 CV 的额外奖金"
    },
    "Thai": {
        "title": "📊 DHP รายงานรายละเอียดรายได้",
        "sidebar_h": "📌 การตั้งค่า",
        "my_p": "ระดับของฉัน", "my_gc": "เกมต่อเดือน", "pa_p": "ระดับพาร์ทเนอร์", "l1": "แนะนำตรง (รุ่น 1)", "dup": "การทำซ้ำ (รุ่น 2-5)",
        "m1": "จำนวนคนรวม", "m2": "โบนัสสมัครรวม", "m3": "รายได้รายเดือน", "m4": "กำไรสุทธิ",
        "tab1": "👥 ยูนิเลเวล", "tab2": "⚖️ ไบนารี", "tab3": "🚀 ออร์บิท",
        "recoup_h": "💰 วิเคราะห์การคืนทุน", "recoup_now": "🎉 คืนทุนทันที!", "recoup_wait": "ระยะเวลาคืนทุนคาดการณ์:",
        "recoup_desc": "💡 รายได้หลังจากคืนทุนคือกำไรสุทธิทั้งหมด", "init_cost": "เงินลงทุนเริ่มต้น",
        "u_desc": "โบนัสตามเปอร์เซ็นต์ CV แต่ละรุ่น", "b_desc": "โบนัสจับคู่ทีม", "o_desc": "โบนัสพิเศษเมื่อครบ 5,460 CV"
    },
    "Vietnamese": {
        "title": "📊 Báo cáo chi tiết thu nhập DHP",
        "sidebar_h": "📌 Cài đặt",
        "my_p": "Cấp của tôi", "my_gc": "Lượt chơi/tháng", "pa_p": "Cấp đối tác", "l1": "Trực tiếp (F1)", "dup": "Sao chép (F2-F5)",
        "m1": "Tổng thành viên", "m2": "Tổng thưởng ĐK", "m3": "Thu nhập thụ động", "m4": "Lợi nhuận ròng",
        "tab1": "👥 Unilevel", "tab2": "⚖️ Binary", "tab3": "🚀 ORBIT",
        "recoup_h": "💰 Phân tích hồi vốn", "recoup_now": "🎉 Hồi vốn ngay lập tức!", "recoup_wait": "Thời gian hồi vốn dự kiến:",
        "recoup_desc": "💡 Tất cả thu nhập sau hồi vốn là lợi nhuận ròng.", "init_cost": "Vốn đầu tư ban đầu",
        "u_desc": "Thưởng theo tỷ lệ CV từng cấp", "b_desc": "Thưởng cân nhánh đội nhóm", "o_desc": "Thưởng thêm mỗi 5,460 CV"
    }
}
t = t_all[lang]

# --- 3. 사이드바 입력 ---
st.sidebar.header(t["sidebar_h"])
my_p = st.sidebar.selectbox(t["my_p"], list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input(t["my_gc"], value=120, min_value=120, step=120)
pa_p = st.sidebar.selectbox(t["pa_p"], list(pkgs.keys()), index=2)
l1 = st.sidebar.number_input(t["l1"], value=2, min_value=1)
dup = st.sidebar.radio(t["dup"], [2, 3], index=0)

# --- 4. 계산 로직 (5대 고정) ---
init_cost = pkgs[my_p]["price"] + 60
base_game_cost = (my_gc / 120) * 110.25 
my_gen_cv = my_gc * (20 * pkgs[my_p]["self_rate"])
cv_shortfall = max(0.0, 72.0 - my_gen_cv)
shortfall_fee = cv_shortfall * 2.0 
monthly_exp = base_game_cost + shortfall_fee

p_reg_cv_value = pkgs[pa_p]["reg_cv"]
p_game_cv_value = 72.0 if pkgs[pa_p]["self_rate"] == 0.03 else 36.0
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05, 5: 0.02}

stats = []
t_reg_cv = t_game_cv = total_people = 0
curr = l1

for i in range(1, 6):
    if i > 1: curr *= dup
    total_people += curr
    r_cv = curr * p_reg_cv_value
    g_cv = curr * (my_gc / 120 * p_game_cv_value)
    t_reg_cv += r_cv
    t_game_cv += g_cv
    stats.append({
        "Generation": f"{i} Gen", 
        "People": int(curr), 
        "Reg Bonus ($)": round(r_cv * rates[i], 1), 
        "Monthly Bonus ($)": round(g_cv * rates[i], 1)
    })

# 바이너리 & 오빗 계산
bin_rate = pkgs[my_p]["bin"]
bin_reg = (t_reg_cv / 2) * bin_rate
bin_mon = (t_game_cv / 2) * bin_rate

orb_count_reg = int((t_reg_cv / 2) // 5460)
orb_reg = orb_count_reg * 450
orb_count_mon = int((t_game_cv / 2) // 5460)
orb_mon = orb_count_mon * 450

total_reg_bonus = sum(s['Reg Bonus ($)'] for s in stats) + bin_reg + orb_reg
total_mon_bonus = sum(s['Monthly Bonus ($)'] for s in stats) + bin_mon + orb_mon
net_monthly_profit = total_mon_bonus - monthly_exp

# --- 5. 리포트 출력 ---
st.title(t["title"])
st.divider()

m1, m2, m3, m4 = st.columns(4)
m1.metric(t["m1"], f"{total_people}명")
m2.metric(t["m2"], f"${total_reg_bonus:,.1f}")
m3.metric(t["m3"], f"${total_mon_bonus:,.1f}")
m4.metric(t["m4"], f"${net_monthly_profit:,.1f}")

st.divider()

# --- 6. 상세 탭 섹션 ---
tab1, tab2, tab3 = st.tabs([t["tab1"], t["tab2"], t["tab3"]])

with tab1:
    st.subheader(t["tab1"])
    st.write(t["u_desc"])
    st.table(pd.DataFrame(stats))

with tab2:
    st.subheader(t["tab2"])
    st.write(t["b_desc"])
    bin_data = {
        "Metric": ["Total CV", "Matching CV (50%)", "Bonus ($)"],
        "Registration": [f"{t_reg_cv:,.1f} CV", f"{t_reg_cv/2:,.1f} CV", f"${bin_reg:,.1f}"],
        "Monthly": [f"{t_game_cv:,.1f} CV", f"{t_game_cv/2:,.1f} CV", f"${bin_mon:,.1f}"]
    }
    st.table(pd.DataFrame(bin_data))

with tab3:
    st.subheader(t["tab3"])
    st.write(t["o_desc"])
    orb_data = {
        "Metric": ["Matching CV", "Cycles", "Bonus ($)"],
        "Registration": [f"{t_reg_cv/2:,.1f} CV", f"{orb_count_reg}x", f"${orb_reg:,.0f}"],
        "Monthly": [f"{t_game_cv/2:,.1f} CV", f"{orb_count_mon}x", f"${orb_mon:,.0f}"]
    }
    st.table(pd.DataFrame(orb_data))

# --- 7. 리쿱 분석 ---
st.divider()
st.subheader(t["recoup_h"])
if total_reg_bonus >= init_cost:
    st.success(f"{t['recoup_now']} {t['init_cost']}(${init_cost:,}) < {t['m2']}(${total_reg_bonus:,.1f})")
else:
    rem = init_cost - total_reg_bonus
    months = rem / net_monthly_profit if net_monthly_profit > 0 else 0
    st.warning(f"{t['recoup_wait']} 약 {months:.1f}개월 (남은 원금: ${rem:,.1f})")
    st.write(t["recoup_desc"])
