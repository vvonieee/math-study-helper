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

def get_text(response):
    return "".join(
        block.text for block in response.content if block.type == "text"
    )

def make_problem(notes):
    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1000,
        system=SYSTEM,
        messages=[{
            "role": "user",
            "content": f"[교안]\n{notes}\n\n"
                       "위 교안만 근거로 연습 문제 1개를 만들어줘."
                       "정답과 풀이는 알려주지 마."
        }],
    )
    return get_text(response)

HINT_SYSTEM = (
    "너는 수학 공부를 돕는 튜터야."
    "반드시 아래 [교안]에 있는 내용만 근거로 삼아."
    "학생이 막힌 부분에서 교안의 어떤 개념이나 공식을 떠올리면 좋을지 힌트를 줘."
    "최종 정답이나 완성된 풀이는 절대 알려주지 말고, 다음 한 걸음만 안내해."
    "힌트는 3문장 이내로 짧게 제공해."
)

def give_hint(notes, problem, stuck):
    response = client.messages.create(
        model="claude-haiku-5-5",
        max_tokens=1000,
        system=HINT_SYSTEM,
        messages=[{
            "role": "user",
            "content": f"[교안]\n{notes}\n\n"
                       f"[문제]\n{problem}\n\n"
                       f"[학생이 막힌 부분]\n{stuck}"
        }],
    )
    return get_text(response)

notes = load_notes("notes/sample.md")
problem = make_problem(notes)
print(problem)
print()

stuck = input("풀다가 막힌 부분을 적어줘: ")
print()
print(give_hint(notes, problem, stuck))
