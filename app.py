import streamlit as st
import openai
import os

os.environ["OPENAI_API_KEY"] = st.secrets["api_key"]

client = openai.OpenAI()


# Streamlit app title and caption
st.title("구영초 학사일정")
st.caption("구영초등학교의 학사일정을 물어볼 수 있는 챗봇입니다.")

# 세션 상태에 메시지가 없으면 초기화
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "행사명을 입력해주세요"}]

# 이전 채팅 메시지 표시

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
         st.markdown(f"**🤖 Assistant:** {msg['content']}")
    else:
        st.markdown(f"**👤 You:** {msg['content']}")

# 사용자 입력 처리
prompt = st.text_input("질문을 입력하세요:", key="input")

if prompt:
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"**👤 You:** {prompt}")
    
    # OpenAI API 호출
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=[
            {"role": "system", "content": '''구영초등학교의 학사일정을 알려줘라. 경어체로 답변하여라.
             삼일절: 3월 1일, 입학식 및 개학식: 3월 4일, 인성주간: 3월 5일 ~ 3월 8일, 기초학력 진단검사: 3월 11일~ 3월 13일
             학부모 총회: 3월 15일, 교육과정 설명회: 3월 20일, 선행교육 근절 교육: 3월 26일 ~ 3월 28일, 전교학생회 선거: 4월 10일, 
             1학기 학업성취도 평가: 4월 1일 ~ 4월 5일(2~6학년), 과학의 날 행사: 4월 17일 ~ 4월 19일, 장애인의 날: 4월 19일,
             융합교육(STEAM) 주간: 4월 22일 ~ 4월 24일, 생명존중사랑 생명교육 주간: 4월 29일 ~ 4월 30일, 근로자의 날: 5월 1일,
             대중교통 이용의 날: 5월 3일, 진로교육: 5월 4일 ~ 5월 9일(4~6학년), 대학탐방: 5월 16일 ~ 5월 17일(6학년), 
             재난안전교육주간: 5월 20일 ~ 5월 22일, 재난대피훈련: 5월 28일, 환경교육 주간: 6월 3일 ~ 6월 7일, 현충인 6월 8일, 
             금융, 교통, 마약, 음주운전 예방교육: 6월 10일 ~ 6월 14일, 방과후 교육 방표회: ㅑ6월 15일, 소방대피훈련: 6월 26일~ 6월 28일,
             학예발표회: 7월 22일 ~ 7월 24일, 여름 방학식: 7월 25일, 2학기 개학식: 8월 26일, 독서교육주간: 9월 18일 ~ 9월 20일,
             학교폭력예방교육: 9월 26일 ~ 9월 27일, 2학기 상담 주간 시작: 9월 30일, 예술 교육 주간: 10월 24일 ~ 10월 25일, 
             합동소방훈련: 10월 28일 ~ 10월 29일, 아동학대 예방 교육: 11월 11일 ~ 11월 15일, 겨울방학식 종업식: 25년 1월 10일
             이 이외의 행사에 대해서 질문이 들어오면 죄송합니다. 정보를 찾을 수 없습니다 라고 대답하여라.'''},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Assistant의 응답 출력
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.markdown(f"**🤖 Assistant:** {msg}")
