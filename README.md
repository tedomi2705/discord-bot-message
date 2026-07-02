## Discord message bot

Tạo file `.env`:

```env
TOKEN=your_discord_TOKEN
CHANNEL_ID=your_channel_id
```

Hoặc gửi tin nhắn trực tiếp cho user:

```env
TOKEN=your_discord_TOKEN
USER_ID=your_user_id
```

Chỉ cấu hình một trong `CHANNEL_ID` hoặc `USER_ID`. Nếu có cả hai, chương trình sẽ báo lỗi.

Nếu không có `CHANNEL_ID` và `USER_ID`, chương trình sẽ hỏi đích gửi khi chạy.

Chạy bot:

```bash
uv run python main.py
```
