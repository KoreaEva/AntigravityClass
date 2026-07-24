import random
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="숫자 맞추기 게임",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. 커스텀 CSS 스타일링 (세련된 UI 구현)
st.markdown("""
<style>
    /* 메인 타이틀 파스텔 글래디언트 */
    .title-text {
        font-size: 2.6rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 50%, #EC4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle-text {
        font-size: 1.05rem;
        text-align: center;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    /* 카드 스타일 */
    .status-card {
        background-color: #F3F4F6;
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    /* 히스토리 아이템 */
    .history-item {
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .up-tag {
        background-color: #FEF3C7;
        color: #92400E;
        border-left: 4px solid #F59E0B;
    }
    .down-tag {
        background-color: #DBEAFE;
        color: #1E40AF;
        border-left: 4px solid #3B82F6;
    }
    .correct-tag {
        background-color: #D1FAE5;
        color: #065F46;
        border-left: 4px solid #10B981;
    }
</style>
""", unsafe_allow_html=True)


# 3. 게임 세션 초기화 함수
def reset_game():
    st.session_state.target_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []
    st.session_state.feedback = None


# 세션 상태 초기화 (처음 실행 시)
if "target_number" not in st.session_state:
    reset_game()

if "best_score" not in st.session_state:
    st.session_state.best_score = None


# 4. 사이드바 (게임 규칙 & 최고 기록 & 리셋)
with st.sidebar:
    st.header("🎮 게임 메뉴")
    
    st.markdown("### 📜 규칙 안내")
    st.markdown("""
    - **1부터 100 사이**의 숫자를 맞추는 게임입니다.
    - 입력한 값에 따라 **UP / DOWN** 힌트가 제공됩니다.
    - 최소한의 시도 횟수로 정답을 맞춰보세요!
    """)
    
    st.divider()
    
    # 최고 기록 표시
    st.markdown("### 🏆 최고 기록 (최저 시도)")
    if st.session_state.best_score is not None:
        st.metric(label="최고 기록", value=f"{st.session_state.best_score}회")
    else:
        st.info("아직 기록이 없습니다. 정답을 맞춰보세요!")

    st.divider()
    
    if st.button("🔄 게임 새로 시작", use_container_width=True):
        reset_game()
        st.rerun()


# 5. 메인 UI (웰컴 메시지 & 헤더)
st.markdown("<div class='title-text'>🎮 숫자 맞추기 게임</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-text'>1부터 100 사이의 숫자를 맞춰보세요! 🎯</div>", unsafe_allow_html=True)

# 메트릭 컬럼 (현재 시도 횟수)
col1, col2 = st.columns(2)
with col1:
    st.metric(label="📊 현재 시도 횟수", value=f"{st.session_state.attempts}회")
with col2:
    st.metric(label="🏆 최고 기록", value=f"{st.session_state.best_score}회" if st.session_state.best_score else "-")

st.divider()


# 6. 입력 처리 제출 함수
def handle_guess():
    guess = st.session_state.user_guess
    if guess is None:
        return
    
    st.session_state.attempts += 1
    target = st.session_state.target_number
    
    if guess < target:
        msg = f"⬆️  UP! {guess}보다 더 큰 숫자입니다."
        st.session_state.feedback = ("up", msg)
        st.session_state.history.insert(0, (st.session_state.attempts, guess, "UP (더 큼)", "up-tag"))
    elif guess > target:
        msg = f"⬇️  DOWN! {guess}보다 더 작은 숫자입니다."
        st.session_state.feedback = ("down", msg)
        st.session_state.history.insert(0, (st.session_state.attempts, guess, "DOWN (더 작음)", "down-tag"))
    else:
        msg = f"🎉 정답입니다! {st.session_state.attempts}번 만에 맞추셨습니다!"
        st.session_state.feedback = ("correct", msg)
        st.session_state.history.insert(0, (st.session_state.attempts, guess, "정답! 🎯", "correct-tag"))
        st.session_state.game_over = True
        
        # 최고 기록 업데이트
        if st.session_state.best_score is None or st.session_state.attempts < st.session_state.best_score:
            st.session_state.best_score = st.session_state.attempts


# 7. 메인 게임 입력 및 상태 안내
if not st.session_state.game_over:
    with st.form(key="guess_form", clear_on_submit=True):
        st.number_input(
            "1~100 사이의 숫자를 입력하세요:",
            min_value=1,
            max_value=100,
            step=1,
            key="user_guess"
        )
        submit_button = st.form_submit_button(label="🎯 정답 확인", on_click=handle_guess, use_container_width=True)

    # 피드백 메시지 표시
    if st.session_state.feedback:
        fb_type, fb_msg = st.session_state.feedback
        if fb_type == "up":
            st.warning(fb_msg)
        elif fb_type == "down":
            st.info(fb_msg)

else:
    # 정답을 맞춘 경우 (축하 및 다시 시작 안내)
    st.balloons()
    st.success(f"🎉 축하합니다! 정답은 **{st.session_state.target_number}**였습니다!")
    st.info(f"총 **{st.session_state.attempts}회** 만에 성공하셨습니다! 👏")
    
    col_retry, col_space = st.columns([1, 1])
    with col_retry:
        if st.button("🔄 다시 시도하기", type="primary", use_container_width=True):
            reset_game()
            st.rerun()

# 8. 이전 시도 기록 (히스토리)
if st.session_state.history:
    st.divider()
    st.subheader("📜 시도 기록")
    for attempt_num, guess_val, status_text, css_class in st.session_state.history:
        st.markdown(
            f"""
            <div class='history-item {css_class}'>
                <span>#{attempt_num}회차 시도: <strong>{guess_val}</strong></span>
                <span>{status_text}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
