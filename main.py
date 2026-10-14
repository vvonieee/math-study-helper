from pathlib import Path
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

SYSTEM = (
    "너는 수학 공부를 돕는 튜터야."
    "반드시 아래 [교안]에 있는 내용만 근거로 삼아."
    "교안에 없는 내용은 다루지 마."
)

def load_notes(path):
    return Path(path).read_text(encoding="utf-8")

def make_problem(notes):
    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=500,
        system=SYSTEM,
        messages=[{
            "role": "user",
            "content": f"[교안]\n{notes}\n\n"
                       "위 교안만 근거로 연습 문제 1개를 만들어줘."
                       "정답과 풀이는 알려주지 마."
        }],
    )
    return response.content[0].text

notes = load_notes("notes/sample.md")
print(make_problem(notes))
