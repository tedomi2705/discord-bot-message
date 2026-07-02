import asyncio
import os

import discord
from dotenv import load_dotenv


def target_label(target_type: str, target: object) -> str:
    name = getattr(target, "name", None) or getattr(target, "global_name", None)
    if not name:
        name = getattr(target, "display_name", None) or str(target)

    prefix = "channel" if target_type == "channel" else "user"
    return f"{prefix} {name} ({target.id})"


async def run_bot(token: str, target_type: str, target_id: int) -> None:
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready() -> None:
        try:
            if target_type == "channel":
                target = client.get_channel(target_id) or await client.fetch_channel(target_id)
                if not hasattr(target, "send"):
                    raise TypeError("Channel này không hỗ trợ gửi tin nhắn.")
            else:
                target = await client.fetch_user(target_id)

            print(f"Bot đã sẵn sàng, gửi tới {target_label(target_type, target)}.")
            print("Nhấn Ctrl+C hoặc Ctrl+D để thoát.")
            while not client.is_closed():
                try:
                    message = await asyncio.to_thread(input, "Nhập tin nhắn cần gửi: ")
                except EOFError:
                    break

                message = message.strip()
                if not message:
                    continue

                await target.send(message)
                print("Đã gửi tin nhắn.")
        finally:
            await client.close()

    await client.start(token)


def parse_id(name: str, value: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise SystemExit(f"{name} phải là số") from exc


def main() -> None:
    load_dotenv()

    token = os.getenv("TOKEN")
    if not token:
        raise SystemExit("Thiếu TOKEN trong .env")

    channel_id_text = os.getenv("CHANNEL_ID")
    user_id_text = os.getenv("USER_ID")

    if channel_id_text and user_id_text:
        raise SystemExit("Chỉ được cấu hình một trong CHANNEL_ID hoặc USER_ID")

    if channel_id_text:
        target_type = "channel"
        target_id = parse_id("CHANNEL_ID", channel_id_text)
    elif user_id_text:
        target_type = "user"
        target_id = parse_id("USER_ID", user_id_text)
    else:
        target_type = input("Gửi tới channel hay user? [channel/user]: ").strip().lower()
        if target_type not in {"channel", "user"}:
            raise SystemExit("Đích gửi phải là channel hoặc user")

        id_name = "CHANNEL_ID" if target_type == "channel" else "USER_ID"
        target_id_text = input(f"Nhập {id_name}: ").strip()
        if not target_id_text:
            raise SystemExit(f"Thiếu {id_name}")

        target_id = parse_id(id_name, target_id_text)

    try:
        asyncio.run(run_bot(token, target_type, target_id))
    except KeyboardInterrupt:
        print("\nThoát.")


if __name__ == "__main__":
    main()
