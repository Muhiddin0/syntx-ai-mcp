# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

User-facing setup and usage documentation lives in `README.md`; reusable agent instructions live in `SKILL.md`.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]" requests uvicorn
```

Run over stdio:

```bash
python mcp_server.py
```

Run over Streamable HTTP:

```bash
python mcp_server.py --http --host 127.0.0.1 --port 8000
```

Import/syntax check (no test suite):

```bash
python -m py_compile mcp_server.py
```

## Architecture

Single-file FastMCP server in `mcp_server.py`. MCP server name is `syntx`. Wraps the Syntx.ai API.

`transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False)` is intentional — this server is designed for controlled local client environments.

Two local state files:

- `~/.syntx_token.json` — Syntx bearer token after login
- `~/.syntx_state.json` — in-progress image `message_id` keyed by `chat_uuid`

## Auth Flow

1. `syntx_login_telegram` → `POST /api/v1/auth/startauth` → returns UUID + Telegram bot link.
2. User approves in Telegram.
3. `syntx_check_auth(uuid)` → `GET /api/v1/auth/token/{uuid}` → polls until `complete` is true → saves token to `~/.syntx_token.json`.

Bearer token sent in `Authorization: Bearer {token}` header on all authenticated calls.

## Image Generation Flow

1. `syntx_generate_image` auto-creates a chat if `chat_uuid` is empty, then calls `POST /api/v1/design/generate?ai_name={model_type}`.
2. `syntx_get_image` calls `GET /api/v1/chats/{chat_uuid}/inprogress`.
   - While items exist, saves `message_id` from the first item to `~/.syntx_state.json` and returns "not ready".
   - Once inprogress is empty, reads `message_id` from state file and fetches `GET /api/v1/chats/{chat_uuid}/{message_id}`.
   - Returns `object_url` from the first `message_object` entry with `object_type == "image"`.
   - **Edge case**: if state file has no entry for `chat_uuid` when inprogress empties (e.g. server restarted mid-generation), returns "No pending image found". Use `syntx_get_chat_messages` to recover.

## Image Edit Flow

1. `syntx_upload_image(file_paths)` → `POST /api/v1/chats/upload-files` → returns CDN URLs.
2. Pass those URLs as `image_urls` to `syntx_generate_image`.
3. Poll with `syntx_get_image` as usual.

## Image Settings

- `model_type`: `banana` (default), `midjourney`, `seedream`, `sora-images`, `flux`, `runway-frames`, `imagen4`, `higgsfield-soul`, `ideogram`, `wan_image`, `grok_image`
- `aspect_ratio`: `21:9`, `16:9`, `9:16`, `5:4`, `4:5`, `4:3`, `3:4`, `3:2`, `2:3`, `1:1`
- `n`: number of images

## Video Generation Flow

1. `syntx_upload_image(file_paths)` → CDN URLs.
2. `syntx_generate_video(prompt, image_urls, ...)` creates a chat with `scope: "video"`, calls `POST /api/v1/video/generate?ai_name={model_type}`.
   - Payload uses `chat_id` (not `chat_uuid`) — this is the only endpoint with that field name.
   - Settings include `type: "image"` (image-to-video), `video_duration`, `upscale: 0`.
3. `syntx_get_video` polls `GET /api/v1/chats/{chat_uuid}/inprogress` — same state file logic as images.
   - Done response has `object_type: "video"`, `object_url` is `.mp4`, thumbnail in `metadata.preview_url` (not `metadata.preview`).

Video model options: `veo3fast_r`, `veo3`. Aspect ratio: `16:9`, `9:16`.

## Tools

- `syntx_login_telegram`
- `syntx_check_auth`
- `syntx_create_chat`
- `syntx_upload_image` — upload local files to CDN, returns URLs
- `syntx_generate_image` — accepts optional `image_urls` for editing; response message contains the `chat_uuid` as plain text
- `syntx_get_image`
- `syntx_generate_video` — image-to-video; requires `image_urls` from CDN
- `syntx_get_video`
- `syntx_list_chats`
- `syntx_get_chat_messages`
- `syntx_logout`

## API Base

```text
https://api.syntx.ai/api/v1
```

Browser-like headers in `HEADERS` constant — Syntx requires them for these endpoints.
