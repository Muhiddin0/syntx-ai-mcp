---
name: syntx
description: Use this skill when generating images with Syntx.ai, authenticating Syntx through Telegram, managing Syntx image chats, retrieving generated image URLs, or troubleshooting the local syntx MCP server.
---

# Syntx Image Skill

Generate images with Syntx.ai through the local `syntx` MCP server. This skill is the agent-facing workflow layer; the MCP server provides the actual tools.

## Prerequisites

The project should have dependencies installed:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]" requests uvicorn
```

The MCP server file is:

```text
mcp_server.py
```

Prefer stdio MCP for local clients:

```bash
python mcp_server.py
```

HTTP mode is available when needed:

```bash
python mcp_server.py --http --host 127.0.0.1 --port 8000
```

## MCP Tools

Use these MCP tools when available:

- `syntx_login_telegram`: start Telegram auth and return the bot login link plus UUID.
- `syntx_check_auth`: check Telegram auth completion with the UUID and save the token.
- `syntx_create_chat`: create a Syntx image chat and return the chat UUID.
- `syntx_generate_image`: start an image generation job.
- `syntx_get_image`: poll a chat until the generated image URL is ready.
- `syntx_list_chats`: list image chats by UUID, title, and message count.
- `syntx_get_chat_messages`: retrieve prompts and image URLs from a chat.
- `syntx_logout`: delete the saved auth token.

## Auth Workflow

Syntx auth happens through Telegram. Do not ask for a password.

1. Call `syntx_login_telegram`.
2. Show the returned Telegram link to the user.
3. Wait for the user to approve login in Telegram.
4. Call `syntx_check_auth` with the UUID.
5. If auth is still pending, ask the user to approve in Telegram and retry.

The saved token is stored at:

```text
~/.syntx_token.json
```

Never reveal or print this token.

## Generate Image Workflow

1. If the user is not authenticated, complete the auth workflow.
2. Convert the user request into a clear image prompt.
3. Call `syntx_generate_image`.
4. Save the returned `chat_uuid` from the tool response.
5. Call `syntx_get_image` with that `chat_uuid`.
6. If the image is not ready, wait briefly and poll again.
7. Return the final image URL and useful preview URLs.

Supported aspect ratios:

```text
21:9, 16:9, 9:16, 5:4, 4:5, 4:3, 3:4, 3:2, 2:3, 1:1
```

Default model:

```text
banana
```

## Prompt Guidance

For vague requests, improve the image prompt with:

- Subject
- Style or medium
- Composition
- Lighting
- Background
- Color direction
- Aspect ratio

Example:

```text
A realistic product photo of a matte black smart speaker on a walnut desk, soft morning window light, shallow depth of field, clean modern workspace, premium commercial photography.
```

## Common Requests

- "Generate an image in Syntx" -> use `syntx_generate_image`, then `syntx_get_image`.
- "Create a Syntx chat" -> use `syntx_create_chat`.
- "Check my image" -> use `syntx_get_image` with the known chat UUID.
- "Find old Syntx images" -> use `syntx_list_chats`, then `syntx_get_chat_messages`.
- "Log out of Syntx" -> use `syntx_logout`.
- "Syntx says not authenticated" -> run the auth workflow.

## Error Handling

If a tool says:

```text
Not authenticated. Call syntx_login_telegram first.
```

Run the auth workflow.

If `syntx_check_auth` says:

```text
Not authenticated yet. Approve in Telegram and try again.
```

Ask the user to approve the Telegram login, then retry.

If `syntx_get_image` says:

```text
Image not ready yet. Try again in a few seconds.
```

Poll again after a short wait.

If `syntx_get_image` says:

```text
No pending image found for this chat_uuid.
```

Use `syntx_get_chat_messages` to inspect the chat history.

## Security

Use stdio transport by default. If HTTP mode is used, bind to `127.0.0.1` unless remote access is explicitly required. Treat `~/.syntx_token.json` as a secret.
