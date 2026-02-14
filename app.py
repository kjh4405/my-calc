import streamlit as st

# 앱 화면 설정
st.set_page_config(page_title="DHP 비지니스 수익계산기", layout="wide")

st.title("🚀 DHP비지니스 수익계산기 (Ver 2.1)")
st.write("레벨별 유니레벨 차등 요율 및 4레벨 복제 모델")

# --- 설정값 입력란 ---
st.sidebar.header("📌 설정값 입력")

package_info = {
    "Basic": {"cv": 72, "binary": 0.05, "sub": 30, "limit": 2},
    "Standard": {"cv": 216, "binary": 0.06, "sub": 30, "limit": 3},
    "Premium": {"cv": 504, "binary": 0.07, "sub": 0, "limit": 4},
    "Ultimate": {"cv": 1080, "binary": 0.08, "sub": 0, "limit": 5}
}

# 1. 나의 설정
my_pkg = st.sidebar.selectbox("나의 패키지 등급", list(package_info.keys()), index=2) # 기본값 Premium
my_game_type = st.sidebar.selectbox("나의 게임 선택", ["$20 게임", "$40 게임"], index=0)
my_game_count = st.sidebar.number_input("나의 한 달 게임 횟수", value=120)

# 2. 조직 설정
partner_pkg = st.sidebar.selectbox("파트너 패키지 등급", list(package_info.keys()), index=2)
lv1_count = st.sidebar.number_input("나의 직접 소개 (1레벨)", value=2)
duplication = st.sidebar.radio("하위 복제 인원 (2~4레벨)", [2, 3], index=0)

# --- 계산 로직 ---

# A. 조직 구성 및 유니레벨 계산 (Premium 기준 4레벨까지만)
p_cv = package_info[partner_pkg]["cv"]
limit = package_info[my_pkg]["limit"] # 내 등급에 따른 수령 한계 레벨

# 각 레벨별 인원 및 유니레벨 수익 (사용자 제시 요율 적용)
rates = {1: 0.03, 2: 0.05, 3: 0.08, 4: 0.05, 5: 0.02} # 5단계는 보너스

lv_data = {}
total_unilevel = 0
current_count = lv1_count

for i in range(1, 5): # 4레벨까지만 계산
    if i > 1:
        current_count = current_count * duplication
    
    # 내 등급 한계까지만 수익 발생
    if i <= limit:
        lv_revenue = (current_count * p_cv) * rates[i]
    else:
        lv_revenue = 0
        
    lv_data[i] = {"count": current_count, "revenue": lv_revenue}
    total_unilevel += lv_revenue

total_people = sum([d["count"] for d in lv_data.values()])

# B. 1회성 보너스 (오빗/바이너리)
total_reg_cv_half = (total_people * p_cv) / 2
orbit_count = total_reg_cv_half // 5460
income_orbit = orbit_count * 450
income_binary = total_reg_cv_half * package_info[my_pkg]["binary"]

# C. 나의 월 지출
cost_game = my_game_count * (20 if my_game_type == "$20 게임" else 40)
cost_sub = package_info[my_pkg]["sub"]
total_cost = cost_game + cost_sub

# --- 화면 출력 ---
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("총 인원 (4단계)", f"{total_people:,} 명")
c2.metric("나의 월 지출", f"${total_cost:,}")
c3.metric("유니레벨 합계", f"${total_unilevel:,.2f}")

st.subheader("📊 상세 수익 구조")
tab1, tab2, tab3 = st.tabs(["유니레벨 상세", "전체 수익 합계", "나의 유지비용"])

with tab1:
    st.write(f"**레벨별 유니레벨 수익 분석 ({my_pkg} 등급 기준)**")
    for i, data in lv_data.items():
        st.write(f"- {i}레벨 ({rates[i]*100}%): {data['count']}명 × {p_cv}CV = ${data['revenue']:,.2f}")
    st.info(f"**유니레벨 최종 합계: ${total_unilevel:,.2f}**")

with tab2:
    st.write("### 💰 1회성 수익 총계")
    st.write(f"- 오빗 보너스: ${income_orbit:,.0f}")
    st.write(f"- 바이너리 보너스: ${income_binary:,.2f}")
    st.write(f"- 유니레벨 보너스: ${total_unilevel:,.2f}")
    st.success(f"**총합: ${(income_orbit + income_binary + total_unilevel):,.2f}**")

with tab3:
    st.write(f"- 게임 비용: ${cost_game:,.0f}")
    st.write(f"- 월 구독료: ${cost_sub:,.0f}")
    st.error(f"**나의 총 월 지출: ${total_cost:,.0f}**")
