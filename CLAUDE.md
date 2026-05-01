# CLAUDE.md

This file gives Claude Code repository-specific context. User-facing setup and usage documentation lives in `README.md`; reusable agent instructions live in `SKILL.md`.

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

## Architecture

This is a single-file FastMCP server in `mcp_server.py`.

The MCP server name is `syntx`. It wraps the Syntx.ai API and exposes tools for Telegram auth, image chat management, image generation, polling, chat history lookup, and logout.

## Auth Flow

1. `syntx_login_telegram` calls `POST /api/v1/auth/startauth`.
2. The response UUID is used to build a Telegram bot login link.
3. The user approves login in Telegram.
4. `syntx_check_auth` calls `GET /api/v1/auth/token/{uuid}` until `complete` is true.
5. The returned bearer token is saved to `~/.syntx_token.json`.

Bearer tokens are sent in the `Authorization` header for authenticated endpoints.

## Image Generation Flow

1. `syntx_generate_image` creates an image chat if no `chat_uuid` is provided.
2. It calls `POST /api/v1/design/generate?ai_name={model_type}`.
3. `syntx_get_image` first checks `GET /api/v1/chats/{chat_uuid}/inprogress`.
4. While an item is in progress, the tool saves its `message_id` in `~/.syntx_state.json`.
5. Once in-progress items disappear, `syntx_get_image` fetches `GET /api/v1/chats/{chat_uuid}/{message_id}` and returns `message_object[].object_url`.

## Tools

- `syntx_login_telegram`
- `syntx_check_auth`
- `syntx_create_chat`
- `syntx_generate_image`
- `syntx_get_image`
- `syntx_list_chats`
- `syntx_get_chat_messages`
- `syntx_logout`

## Image Settings

- `model_type`: `banana` by default
- `aspect_ratio`: `21:9`, `16:9`, `9:16`, `5:4`, `4:5`, `4:3`, `3:4`, `3:2`, `2:3`, `1:1`
- `n`: number of images
- `image_url`: reference images list, currently sent as an empty list by this server

## API Base

```text
https://api.syntx.ai/api/v1
```

Browser-like headers are included in `HEADERS`; Syntx currently expects them for these API calls.
