import os
import schedule
import time
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from openai import OpenAI

# 환경 변수 로드
load_dotenv()

# Slack 클라이언트 초기화
slack_token = os.getenv("SLACK_BOT_TOKEN")
client = WebClient(token=slack_token)

# OpenAI 클라이언트 초기화
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_user_name(user_id):
    """사용자 ID로부터 실제 이름을 가져옵니다."""
    try:
        response = client.users_info(user=user_id)
        if response["ok"]:
            user = response["user"]
            # 실명이 있으면 실명을, 없으면 display_name을, 그것도 없으면 real_name을 사용
            return user.get("real_name") or user.get("profile", {}).get("display_name") or user.get("name")
    except SlackApiError as e:
        print(f"Error fetching user info: {e}")
    return user_id

def get_channel_messages(channel_id):
    """특정 채널의 메시지를 가져옵니다."""
    try:
        # 오늘 자정부터 현재까지의 메시지를 가져옵니다
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        result = client.conversations_history(
            channel=channel_id,
            oldest=str(today.timestamp())
        )
        return result["messages"]
    except SlackApiError as e:
        print(f"Error fetching messages: {e}")
        return []

def summarize_messages(messages):
    """메시지들을 요약합니다."""
    if not messages:
        return "오늘 대화가 없습니다."
    
    # 메시지들을 하나의 문자열로 결합 (사용자 이름 포함)
    conversation = "\n".join([
        f"{get_user_name(msg.get('user', 'Unknown'))}: {msg.get('text', '')}"
        for msg in messages
    ])
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "당신은 대화를 요약하는 전문가입니다. 주어진 대화를 간단하고 명확하게 요약해주세요. 그리고 가능하면 bullet point로 요약가능했으면 좋겠어."},
                {"role": "user", "content": f"다음 대화를 요약해주세요:\n\n{conversation}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error summarizing messages: {e}")
        return "메시지 요약 중 오류가 발생했습니다."

def send_summary():
    """요약을 채널에 전송합니다."""
    channel_id = os.getenv("SLACK_CHANNEL_ID")
    messages = get_channel_messages(channel_id)
    summary = summarize_messages(messages)
    
    try:
        client.chat_postMessage(
            channel=channel_id,
            text=f"*오늘의 대화 요약*\n\n{summary}"
        )
    except SlackApiError as e:
        print(f"Error sending summary: {e}")

def main():
    # 스케줄링 부분 주석 처리
    # 서버에 실행해 두면 매일 오후 6시에 summary 전송
    # schedule.every().day.at("18:00").do(send_summary)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)
    
    # 즉시 실행
    print("대화 요약을 시작합니다...")
    send_summary()
    print("요약이 완료되었습니다.")

if __name__ == "__main__":
    main()
