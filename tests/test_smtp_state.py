import smtplib


HOST = "127.0.0.1"
PORT = 2525
TIMEOUT = 5


def test_data_without_mail_from():
    with smtplib.SMTP(
        HOST,
        PORT,
        timeout=TIMEOUT
    ) as client:
        client.ehlo()

        code, message = client.docmd("DATA")

        assert code == 503
        assert b"MAIL FROM required" in message

    print(
        "PASS: DATA without MAIL FROM -> 503"
    )


def test_rcpt_without_mail_from():
    with smtplib.SMTP(
        HOST,
        PORT,
        timeout=TIMEOUT
    ) as client:
        client.ehlo()

        code, message = client.rcpt(
            "receiver@example.com"
        )

        assert code == 503
        assert b"MAIL FROM required" in message

    print(
        "PASS: RCPT TO without MAIL FROM -> 503"
    )


def test_data_without_rcpt_to():
    with smtplib.SMTP(
        HOST,
        PORT,
        timeout=TIMEOUT
    ) as client:
        client.ehlo()

        code, _ = client.mail(
            "sender@example.com"
        )
        assert code == 250

        code, message = client.docmd("DATA")

        assert code == 503
        assert b"RCPT TO required" in message

    print(
        "PASS: DATA without RCPT TO -> 503"
    )


def test_transaction_resets_after_message():
    with smtplib.SMTP(
        HOST,
        PORT,
        timeout=TIMEOUT
    ) as client:
        client.ehlo()

        code, _ = client.mail(
            "first@example.com"
        )
        assert code == 250

        code, _ = client.rcpt(
            "receiver1@example.com"
        )
        assert code == 250

        code, _ = client.data(
            "From: first@example.com\r\n"
            "To: receiver1@example.com\r\n"
            "Subject: First message\r\n"
            "\r\n"
            "This is the first message."
        )
        assert code == 250

        # After DATA succeeds, the transaction
        # must be reset. Therefore DATA cannot
        # immediately start another message.
        code, message = client.docmd("DATA")

        assert code == 503
        assert b"MAIL FROM required" in message

    print(
        "PASS: SMTP transaction resets after DATA"
    )


if __name__ == "__main__":
    test_data_without_mail_from()
    test_rcpt_without_mail_from()
    test_data_without_rcpt_to()
    test_transaction_resets_after_message()

    print()
    print("All SMTP state tests passed.")
