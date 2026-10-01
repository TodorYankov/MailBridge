import asyncio

from mailbridge.message_handler import handle_message


async def handle_client(
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter
):
    writer.write(b"220 MailBridge SMTP Server Ready\r\n")
    await writer.drain()

    # SMTP transaction state
    sender = None
    recipient = None

    while True:
        data = await reader.readline()

        if not data:
            break

        command = data.decode(errors="replace").strip()
        print(f"CLIENT: {command}")

        if (
            command.upper().startswith("EHLO")
            or command.upper().startswith("HELO")
        ):
            writer.write(b"250-Hello\r\n250 OK\r\n")

        elif command.upper().startswith("MAIL FROM:"):
            sender = command[10:].strip()

            # A new MAIL FROM starts a new transaction.
            recipient = None

            print(f"SENDER: {sender}")
            writer.write(b"250 Sender OK\r\n")

        elif command.upper().startswith("RCPT TO:"):
            if sender is None:
                writer.write(
                    b"503 Bad sequence of commands: "
                    b"MAIL FROM required\r\n"
                )
                await writer.drain()
                continue

            recipient = command[8:].strip()

            print(f"RECIPIENT: {recipient}")
            writer.write(b"250 Recipient OK\r\n")

        elif command.upper() == "DATA":
            if sender is None:
                writer.write(
                    b"503 Bad sequence of commands: "
                    b"MAIL FROM required\r\n"
                )
                await writer.drain()
                continue

            if recipient is None:
                writer.write(
                    b"503 Bad sequence of commands: "
                    b"RCPT TO required\r\n"
                )
                await writer.drain()
                continue

            writer.write(
                b"354 End data with <CR><LF>.<CR><LF>\r\n"
            )
            await writer.drain()

            message_lines = []

            while True:
                line = await reader.readline()

                if not line:
                    break

                if line == b".\r\n":
                    break

                message_lines.append(
                    line.decode(errors="replace")
                )

            message = "".join(message_lines)

            handle_message(
                sender,
                recipient,
                message
            )

            writer.write(
                b"250 Message accepted for delivery\r\n"
            )
            await writer.drain()

            # The SMTP transaction is complete.
            # A new message must start with MAIL FROM.
            sender = None
            recipient = None

        elif command.upper() == "QUIT":
            writer.write(b"221 Bye\r\n")
            await writer.drain()
            break

        else:
            writer.write(
                b"502 Command not implemented\r\n"
            )

        await writer.drain()

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(
        handle_client,
        "127.0.0.1",
        2525
    )

    print(
        "MailBridge SMTP Server running "
        "on 127.0.0.1:2525"
    )

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
