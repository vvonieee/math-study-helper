from pathlib import Path

def load_notes(path):
    return Path(path).read_text(encoding='utf-8')

notes = load_notes("notes/sample.md")
print(notes)
