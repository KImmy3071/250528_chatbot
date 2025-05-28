from openai import OpenAI
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="경희대 교수학습지원센터용 AI", page_icon="🦁", layout="centered")
st.title("경희대 교수학습지원센터용 AI")

# 사용자 API 키 입력
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

st.session_state.api_key = st.text_input(
    "🔑 OpenAI API 키를 입력하세요",
    type="password",
    value=st.session_state.api_key,
    placeholder="sk-로 시작하는 OpenAI API Key"
)

# 키가 유효하지 않으면 종료
if not st.session_state.api_key.startswith("sk-"):
    st.warning("API 키를 입력해야 AI와 대화할 수 있습니다.")
    st.stop()

# OpenAI 클라이언트 생성 (최신 버전 방식)
client = OpenAI(api_key=st.session_state.api_key)

# 사이드바 안내
with st.sidebar:
    st.header("🧭 사용 가이드")
    st.markdown("""
    이 AI는 경희대 교수학습지원센터를 위한 비서형 인공지능입니다.

    **추천 질문 예시:**
    - 자기주도 학습이란?
    - 시험 불안 극복법 알려줘
    - 액티브 러닝이 뭔가요?
    - 강의 피드백 어떻게 활용하나요?
    """)
    if st.button("📌 예시 질문: 자기주도 학습 전략"):
        st.session_state.messages.append({"role": "user", "content": "자기주도 학습 전략이 뭐야?"})

# 세션 상태 초기화
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": (
            "당신은 경희대학교 교수학습지원센터의 전담 AI 비서입니다. "
            "학생들에게는 학습법, 시간관리, 자기주도 전략에 대해 조언하고, "
            "교수자에게는 강의법, 피드백, 수업설계, 교육자료 개발에 도움을 줍니다. "
            "정중하고 실용적인 어조로 명확하게 설명하세요."
        )
    }]

# 이전 메시지 출력
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("무엇을 도와드릴까요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
        except Exception as e:
            reply = f"⚠️ 오류 발생: {e}"
            st.error(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
