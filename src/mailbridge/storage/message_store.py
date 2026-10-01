from pathlib import Path
from datetime import datetime


STORAGE_DIR = Path("data/messages")


def save_message(
    sender: str,
    recipient: str,
    subject: str,
    body: str
) -> Path:

    STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    file_path = STORAGE_DIR / f"{timestamp}.txt"

    content = (
        f"From: {sender}\n"
        f"To: {recipient}\n"
        f"Subject: {subject}\n"
        f"\n"
        f"{body}"
    )

    file_path.write_text(content, encoding="utf-8")

    print(f"Message saved: {file_path}")

    return file_path