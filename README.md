# MailBridge

MailBridge is a Python SMTP server and experimental mail service built from scratch for learning email protocols, networking, and backend software engineering.

The project currently implements a working local SMTP server that can receive, parse, validate, and store email messages.

## Current Features

- Async SMTP server built with `asyncio`
- `EHLO` / `HELO` support
- `MAIL FROM`
- `RCPT TO`
- `DATA`
- `QUIT`
- SMTP transaction state validation
- MIME email parsing
- Plain-text body extraction
- Local message storage
- Automated SMTP state tests
- Standard Python `smtplib` client compatibility

## SMTP Flow

```text
Client
  |
  v
EHLO / HELO
  |
  v
MAIL FROM
  |
  v
RCPT TO
  |
  v
DATA
  |
  v
Message Parser
  |
  v
Message Storage
```

Invalid command sequences are rejected.

For example:

```text
EHLO
DATA
```

returns:

```text
503 Bad sequence of commands: MAIL FROM required
```

## Project Structure

```text
MailBridge/
├── src/
│   └── mailbridge/
│       ├── message_handler.py
│       ├── smtp/
│       │   └── server.py
│       └── storage/
│           └── message_store.py
│
├── tests/
│   ├── test_client.py
│   └── test_smtp_state.py
│
├── .gitignore
└── README.md
```

## Running the SMTP Server

From the project root:

```powershell
$env:PYTHONPATH="src"
python -m mailbridge.smtp.server
```

The development server listens on:

```text
127.0.0.1:2525
```

## Running the Tests

Keep the SMTP server running in one terminal.

In another terminal run:

```powershell
python tests\test_smtp_state.py
```

and:

```powershell
python tests\test_client.py
```

## Development Status

MailBridge is currently an educational SMTP server under active development.

Planned next steps include:

- Mailbox storage
- Inbox organization
- Multiple recipients
- User accounts
- Authentication
- Database persistence
- Improved SMTP protocol support
- Webmail interface

Long-term experiments may include running MailBridge with a real domain and studying mail delivery infrastructure.

## Tech Stack

- Python 3.12
- `asyncio`
- `smtplib`
- Python `email` package
- Git / GitHub