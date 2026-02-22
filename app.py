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

# --- 2. 다국어 사전 (일본어 번역 전문성 강화 및 한국어 제거) ---
lang_options = ["Korean", "English", "Japanese", "Chinese", "Thai", "Vietnamese"]
lang = st.sidebar.selectbox("🌐 Select Language", lang_options)

t_all = {
    "Korean": {
        "unit": "게임", "title": "📊 DHP 글로벌 수익 및 ADIL 자산 분석", "sidebar_h": "📌 조건 입력",
        "my_p": "내 패키지 등급", "my_gc": "나의 월 게임수", "pa_p": "파트너 패키지 등급", "pa_gc": "파트너 월 게임수", "l1": "직접 소개", "dup": "복제",
        "m1": "총 조직", "m2": "총 가입 보너스", "m3": "월 보너스 합계", "m4": "ADIL 월 획득량",
        "tab1": "👥 유니레벨", "tab2": "⚖️ 바이너리", "tab3": "🚀 오빗(ORBIT)", "tab4": "🪙 ADIL 가치", "tab5": "💸 지출/수익",
        "exp_init": "초기 투자금 (패키지+가입비)", "exp_month": "월 유지비", "net_profit": "월 예상 순수익",
        "col_gen": "세대", "col_people": "인원", "col_reg": "등록($)", "col_mon": "연금($)",
        "matching_cv": "매칭 CV", "bonus_usd": "보너스($)", "cycle": "사이클",
        "adil_info": "120게임 중 7.5게임당 1위 ($30 가치의 ADIL 획득 / 시세 $0.4 기준 562.5개)",
        "ref_title": "ℹ️ 참고용 비용 안내", "ref_init": "🔹 초기 등록 비용", "ref_month": "🔹 월간 유지비 상세",
        "ref_init_sub": "(패키지 가격 + 가입비 $60 포함)",
        "profit_info": "💡 순수익은 매달 발생하는 보너스 합계에서 고정 유지비($110.25)를 차감하여 계산됩니다.",
        "msg_extra": "고정유지비 + 자격유지비", "msg_waived": "240게임 플레이로 추가비용 면제됨"
    },
    "Japanese": {
        "unit": "ゲーム", 
        "title": "📊 DHP & ADIL 総合収益分析", 
        "sidebar_h": "📌 条件設定", 
        "my_p": "自分のパッケージ等級", 
        "my_gc": "自分の月間プレイ数", 
        "pa_p": "パートナーのパッケージ等級", 
        "pa_gc": "パートナーの月間プレイ数",
        "l1": "直紹介数", 
        "dup": "複製数", 
        "m1": "組織規模", 
        "m2": "登録報酬合計", 
        "m3": "月間報酬合計", 
        "m4": "ADIL月間獲得量", 
        "tab1": "👥 ユニレベル", 
        "tab2": "⚖️ バイナリー", 
        "tab3": "🚀 オービット", 
        "tab4": "🪙 ADIL評価額", 
        "tab5": "💸 収支分析", 
        "exp_init": "初期投資額", 
        "exp_month": "月間維持費", 
        "net_profit": "月間純利益", 
        "col_gen": "世代", 
        "col_people": "人数", 
        "col_reg": "登録報酬($)", 
        "col_mon": "継続報酬($)", 
        "matching_cv": "マッチングCV", 
        "bonus_usd": "報酬($)", 
        "cycle": "サイクル", 
        "adil_info": "120ゲーム中、平均7.5回1位獲得時（$30相当のADIL獲得 / $0.4換算で562.5個）",
        "ref_title": "ℹ️ 費用案内（参考）", 
        "ref_init": "🔹 初期登録費用", 
        "ref_month": "🔹 月間維持費詳細",
        "ref_init_sub": "（パッケージ価格 + 入会費 $60 を含む）",
        "profit_info": "💡 純利益は、毎月の報酬合計から固定維持費（$110.25）を差し引いて算出されます。",
        "msg_extra": "固定維持費 + 資格維持費", 
        "msg_waived": "240ゲーム以上のプレイにより追加費用免除"
    },
    "English": {
        "unit": " Games", "title": "📊 DHP & ADIL Total Analysis", "sidebar_h": "📌 Settings",
        "my_p": "My Tier", "my_gc": "My Games", "pa_p": "Partner Tier", "pa_gc": "Partner Games", "l1": "Directs", "dup": "Dup",
        "m1": "Total Org", "m2": "Total Reg. Bonus", "m3": "Total Monthly", "m4": "Monthly ADIL",
        "tab1": "👥 Unilevel", "tab2": "⚖️ Binary", "tab3": "🚀 ORBIT", "tab4": "🪙 ADIL Value", "tab5": "💸 Cash Flow",
        "exp_init": "Initial Investment", "exp_month": "Monthly Expense", "net_profit": "Net Monthly Profit",
        "col_gen": "Gen", "col_people": "People", "col_reg": "Reg($)", "col_mon": "Monthly($)",
        "matching_cv": "Matching CV", "bonus_usd": "Bonus($)", "cycle": "Cycle",
        "adil_info": "1st place in 7.5 out of 120 games ($30 worth of ADIL / 562.5 ADIL at $0.4)",
        "ref_title": "ℹ️ Reference Cost Info", "ref_init": "🔹 Initial Reg. Cost", "ref_month": "🔹 Monthly Detail",
        "ref_init_sub": "(Includes Pkg + $60 fee)",
        "profit_info": "💡 Net profit is total monthly bonuses minus fixed expense ($110.25).",
        "msg_extra": "Fixed Expense + Maintenance Fee", "msg_waived": "Extra fee waived with 240 games"
    },
    "Chinese": {
        "unit": " 游戏", "title": "📊 DHP & ADIL 综合资产分析", "sidebar_h": "📌 设置", "my_p": "我的等级", "my_gc": "每月游戏次数", "pa_p": "伙伴等级", "pa_gc": "伙伴每月游戏", "l1": "直接推荐", "dup": "复制", "m1": "总组织", "m2": "总注册奖", "m3": "总月度奖", "m4": "每月 ADIL", "tab1": "👥 多层次", "tab2": "双轨制", "tab3": "🚀 轨道", "tab4": "🪙 ADIL 估值", "tab5": "💸 现金流", "exp_init": "初始投资", "exp_month": "每月支出", "net_profit": "每月净利润", 
        "col_gen": "代", "col_people": "人数", "col_reg": "注册($)", "col_mon": "月度($)", "matching_cv": "Matching CV", "bonus_usd": "奖金($)", "cycle": "循环", "adil_info": "120场游戏中获得7.5场第1名 (价值$30的ADIL / $0.4时为562.5个)", 
        "ref_title": "ℹ️ 参考费用信息", "ref_init": "🔹 初始注册费用", "ref_month": "🔹 每月维持费明세", "ref_init_sub": "(含套餐 + $60 注册费)", 
        "profit_info": "💡 净利润从每月奖金总额中减去固定支出 ($110.25) 计算。", "msg_extra": "固定支出 + 资格维持费", "msg_waived": "240场游戏免除额外费"
    }
}
t = t_all.get(lang, t_all["Korean"])

# --- 3. 핵심 계산 로직 (조직 총 게임수 반영) ---
st.sidebar.header(t["sidebar_h"])
my_p = st.sidebar.selectbox(t["my_p"], list(pkgs.keys()), index=2)
my_gc = st.sidebar.number_input(t["my_gc"], value=120, min_value=120, step=120)

# 파트너 월 게임수 조건 추가 (조직 전체 게임수 계산용)
pa_p = st.sidebar.selectbox(t["pa_p"], list(pkgs.keys()), index=2)
pa_gc = st.sidebar.number_input(t.get("pa_gc", "Partner Monthly Games"), value=120, min_value=120, step=120)

l1 = st.sidebar.number_input(t["l1"], value=2, min_value=1)
dup = st.sidebar.radio(t["dup"], [2, 3], index=0)

# 내 ADIL 및 고정 지출
my_adil = (my_gc / 120) * 562.5
init_exp = pkgs[my_p]["price"] + 60
fixed_monthly_exp = (my_gc / 120) * 110.25
extra_72 = 72.0 if (my_p in ["Basic", "Standard"] and my_gc < 240) else 0.0

# 조직 수익 계산 (조직 전체 게임수 반영)
p_reg_cv = pkgs[pa_p]["reg_cv"]
# 파트너의 월 게임수에 비례하여 발생하는 CV (120게임 기준 72 혹은 36)
p_mon_cv = (72.0 if pkgs[pa_p]["self_rate"] >= 0.03 else 36.0) * (pa_gc / 120)

rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05, 5: 0.02}
stats = []; total_people = 0; t_reg_cv = 0; t_mon_cv = 0; curr = l1

for i in range(1, 6):
    if i > 1: curr *= dup
    total_people += curr
    r_cv = curr * p_reg_cv
    m_cv = curr * p_mon_cv
    t_reg_cv += r_cv; t_mon_cv += m_cv
    stats.append({
        t["col_gen"]: f"{i} Gen", 
        t["col_people"]: f"{int(curr)}", 
        t["col_reg"]: f"{(r_cv * rates[i]):.1f}", 
        t["col_mon"]: f"{(m_cv * rates[i]):.1f}"
    })

# 바이너리/오빗 계산
bin_rate = pkgs[my_p]["bin"]; m_reg_cv = t_reg_cv / 2; m_mon_cv = t_mon_cv / 2
bin_reg_bonus = m_reg_cv * bin_rate; bin_mon_bonus = m_mon_cv * bin_rate
orb_c_reg = int(m_reg_cv // 5460); orb_r_bonus = orb_c_reg * 450
orb_c_mon = int(m_mon_cv // 5460); orb_m_bonus = orb_c_mon * 450
total_mon_bonus = sum([float(s[t["col_mon"]]) for s in stats]) + bin_mon_bonus + orb_m_bonus
net_profit = total_mon_bonus - fixed_monthly_exp

# --- 4. 화면 출력 ---
st.title(t["title"])

with st.expander(t["ref_title"]):
    c_i1, c_i2 = st.columns(2)
    with c_i1:
        st.write(f"**{t['ref_init']}:** `${init_exp:,.2f}`")
        st.caption(t["ref_init_sub"])
    with c_i2:
        if extra_72 > 0:
            st.write(f"**{t['ref_month']}:** `${fixed_monthly_exp:,.2f} + $72.0` ⚠️")
            st.info(f"💡 {my_p} ({my_gc}{t['unit']}): {t['msg_extra']}")
        else:
            st.write(f"**{t['ref_month']}:** `${fixed_monthly_exp:,.2f}` ✅")
            if (my_p in ["Basic", "Standard"]) and my_gc >= 240:
                st.success(f"✨ {my_p} ({my_gc}{t['unit']}): {t['msg_waived']}")

st.divider()

# 메인 지표
m1_col, m2_col, m3_col, m4_col = st.columns(4)
total_org_games = int(total_people * pa_gc)
unit_txt = " 人" if lang == "Japanese" else f" {t['unit']}"
m1_col.metric(t["m1"], f"{total_people}{unit_txt}", f"{total_org_games:,} Total Games")
m2_col.metric(t["m2"], f"${(sum([float(s[t['col_reg']]) for s in stats]) + bin_reg_bonus + orb_r_bonus):,.2f}")
m3_col.metric(t["m3"], f"${total_mon_bonus:,.2f}")
m4_col.metric(t["m4"], f"{my_adil:,.1f} ADIL")

st.divider()

# 탭 UI
tabs = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"], t["tab5"]])
with tabs[0]: st.table(pd.DataFrame(stats))
with tabs[1]: st.table(pd.DataFrame({"Type": ["Registration", "Monthly"], t["matching_cv"]: [f"{m_reg_cv:,.1f}", f"{m_mon_cv:,.1f}"], t["bonus_usd"]: [f"${bin_reg_bonus:,.1f}", f"${bin_mon_bonus:,.1f}"]}))
with tabs[2]: st.table(pd.DataFrame({"Type": ["Registration", "Monthly"], t["cycle"]: [f"{orb_c_reg}x", f"{orb_c_mon}x"], t["bonus_usd"]: [f"${orb_r_bonus:,.1f}", f"${orb_m_bonus:,.1f}"]}))
with tabs[3]:
    st.info(f"💡 {t['adil_info']}")
    st.table(pd.DataFrame([{"ADIL Price": f"${p}", "Value": f"${(my_adil*p):,.1f}"} for p in [0.4, 1.0, 2.0, 5.0]]))
with tabs[4]:
    st.info(t["profit_info"])
    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**🔴 {t['exp_init']}:** `${init_exp:,.2f}`")
        if extra_72 > 0:
            st.write(f"**🟠 {t['exp_month']}:** `${fixed_monthly_exp:,.2f} + $72.0` 👈")
            st.caption(f"({my_p} {my_gc}{t['unit']}: {t['msg_extra']})")
        else:
            st.write(f"**🟠 {t['exp_month']}:** `${fixed_monthly_exp:,.2f}`")
    with c2: st.success(f"**💰 {t['net_profit']}: ${net_profit:,.2f}**")
