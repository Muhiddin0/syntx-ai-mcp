# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install requests
```

Run: `python main.py`

## Architecture

Single-file Python client (`main.py`) for the syntx.ai API. `Syntx` class wraps all API calls. Auth uses Telegram-based OAuth flow; image generation is async with polling.

### Auth flow (2-step)

1. `POST /api/v1/auth/startauth` → `{"uuid": "..."}` — initiates Telegram bot login
2. Poll `GET /api/v1/auth/token/{uuid}` until `{"complete": true, "token": "JWT"}` — user must approve in Telegram

### Image generation flow (2-step)

1. `POST /api/v1/design/generate?ai_name=banana` with `{chat_uuid, prompt, settings}` → returns message with `task_id`, image not ready yet
2. Poll `GET /api/v1/chats/{chat_uuid}/{message_id}` until `object_url` is populated in `message_object[].object_url`

Bearer token goes in `Authorization` header for authenticated endpoints.

### Image settings

- `model_type`: `"banana"` (default image model)
- `aspect_ratio`: `"16:9"`, `"9:16"`, `"1:1"`, `"4:3"`, `"3:4"`, `"4:5"`, `"5:4"`, `"3:2"`, `"2:3"`, `"21:9"`
- `n`: number of images
- `image_url`: list of reference images (or empty)

### API base

`https://api.syntx.ai/api/v1/` — browser-like headers required (User-Agent, sec-ch-ua, etc.)
