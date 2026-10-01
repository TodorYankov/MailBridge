from email import policy
from email.parser import Parser
from mailbridge.storage.message_store import save_message

def handle_message(sender: str, recipient: str, message: str) -> None:
    email_message = Parser(policy=policy.default).parsestr(message)

    from_address = email_message.get("From")
    to_address = email_message.get("To")
    subject = email_message.get("Subject")

    body = email_message.get_body(preferencelist=("plain",))

    if body:
        body_text = body.get_content()
    else:
        body_text = ""

    print("\n========== PARSED EMAIL ==========")
    print(f"SMTP Sender:    {sender}")
    print(f"SMTP Recipient: {recipient}")
    print(f"From:           {from_address}")
    print(f"To:             {to_address}")
    print(f"Subject:        {subject}")
    print("----------------------------------")
    print(body_text)
    print("==================================\n")

    save_message(
        sender=from_address or sender,
        recipient=to_address or recipient,
        subject=subject or "(No Subject)",
        body=body_text
    )

