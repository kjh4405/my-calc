import streamlit as st

# 앱 화면 설정
st.set_page_config(page_title="Orbit 수익 시뮬레이터", layout="wide")

st.title("🚀 Orbit 비즈니스 수익 계산기")
st.write("나의 조직 규모에 따른 실시간 수익 시뮬레이션")

# 사이드바: 입력창
st.sidebar.header("📌 설정값 입력")
b2_rate = st.sidebar.selectbox("나의 패키지 등급 (요율)", [0.05, 0.06, 0.07, 0.08], index=3, format_func=lambda x: f"{int(x*100)}%")
b3_cv = st.sidebar.number_input("산하 등록 패키지 CV", value=1080)
b4_people = st.sidebar.slider("직접 소개 인원 (1레벨)", 2, 10, 2)
b5_games = st.sidebar.number_input("1인당 월간 게임수", value=120)

# 계산 로직 (5단계 누적)
lv1 = b4_people
lv2 = b4_people**2
lv3 = b4_people**3
lv4 = b4_people**4
lv5 = b4_people**5
total_people = lv1 + lv2 + lv3 + lv4 + lv5

# 1. 1회성 수익
total_reg_cv = total_people * b3_cv
weak_leg_cv = total_reg_cv / 2
orbit_count = weak_leg_cv // 5460
orbit_money = orbit_count * 450
binary_money = weak_leg_cv * b2_rate

# 2. 매달 수익
total_game_cv = total_people * b5_games * 0.6
game_weak_cv = total_game_cv / 2
game_orbit_count = game_weak_cv // 5460
game_orbit_money = game_orbit_count * 450
game_binary_money = game_weak_cv * b2_rate

# 결과 화면 구성
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 조직 규모")
    st.metric("5단계 총 인원", f"{total_people:,} 명")
    st.write(f"1레벨({lv1}) → 2레벨({lv2}) → 3레벨({lv3}) → 4레벨({lv4}) → 5레벨({lv5})")

with col2:
    st.subheader("💰 1회성 등록 수익")
    st.write(f"총 발생 CV: {total_reg_cv:,} CV")
    st.metric("오빗 보너스", f"${orbit_money:,.0f}")
    st.metric("바이너리 보너스", f"${binary_money:,.0f}")

st.divider()

st.subheader("📅 매달 예상 연금 수익 (게임)")
c1, c2, c3 = st.columns(3)
c1.metric("총 게임 CV", f"{total_game_cv:,.0f}")
c2.metric("매달 오빗", f"${game_orbit_money:,.0f}")
c3.metric("매달 바이너리", f"${game_binary_money:,.0f}")

st.success(f"예상 월 총합: **${(game_orbit_money + game_binary_money):,.0f}**")
