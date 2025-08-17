import json
from pathlib import Path

HISTORY_FILE = Path(__file__).parent / "history.json"


def save_summary_history(original, saved, summary):
    if HISTORY_FILE.exists():
        data = json.loads(HISTORY_FILE.read_text())
    else:
        data = []

    data.append(
        {"original_filename": original, "saved_filename": saved, "summary": summary}
    )

    data = data[-5:]
    HISTORY_FILE.write_text(json.dumps(data, indent=2))


def get_summary_history():
    if HISTORY_FILE.exists():
        return json.loads(HISTORY_FILE.read_text())
    return []
