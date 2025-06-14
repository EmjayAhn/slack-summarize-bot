# Slack 대화 요약 봇

이 봇은 Slack 채널의 대화를 자동으로 요약하여 매일 저녁 6시에 보고합니다.
현재 코드는 test를 위해 즉시 요약을 전송하는 것을 포함합니다.

## 설정 방법

1. 필요한 패키지 설치:
```bash
uv sync
```

2. Slack 앱 생성 및 설정:
   - [Slack API 웹사이트](https://api.slack.com/apps)에서 새 앱 생성
   - Bot Token Scopes에 다음 권한 추가: 
     - `channels:history`
     - `chat:write`
     - `channels:read`
     - `users:read`
   - 앱을 워크스페이스에 설치

3. 환경 변수 설정:
   - `.env` 파일을 생성하고 다음 변수들을 설정:
     ```
     SLACK_BOT_TOKEN=xoxb-your-bot-token
     OPENAI_API_KEY=your-openai-api-key
     SLACK_CHANNEL_ID=your-channel-id
     ```

4. 봇 실행:
```bash
uv run main.py
```

## 기능

- 매일 저녁 6시에 자동으로 대화 요약
- OpenAI GPT-4o-mini를 사용한 대화 요약
- 채널의 모든 메시지를 수집하여 요약

## 주의사항

- Slack API 토큰과 OpenAI API 키는 절대 공개하지 마세요
- 봇이 채널에 초대되어 있어야 합니다
- 채널 ID는 채널 URL에서 확인할 수 있습니다
