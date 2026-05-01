---
name: syntx
description: Use this skill when generating images with Syntx.ai, authenticating Syntx through Telegram, managing Syntx image chats, retrieving generated image URLs, or troubleshooting the local syntx MCP server.
---

# Syntx MCP Skill

Use this skill when a user wants to generate images with Syntx.ai through the local `syntx` MCP server, manage Syntx image chats, retrieve generated image URLs, or troubleshoot Syntx MCP authentication.

## What This MCP Server Does

This repository provides a Python FastMCP server named `syntx`.

It exposes tools for:

- Starting Telegram authentication with Syntx.ai
- Checking authentication status and saving the bearer token locally
- Creating image chats
- Starting image generation jobs
- Polling for generated image URLs
- Listing image chats and messages
- Logging out by deleting the saved token

The server file is:

```text
mcp_server.py
```

The server can run through stdio or Streamable HTTP.

## Setup Checklist

Before using the tools, make sure dependencies are installed:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]" requests uvicorn
```

For local MCP clients, prefer stdio:

```bash
python mcp_server.py
```

For HTTP clients:

```bash
python mcp_server.py --http --host 127.0.0.1 --port 8000
```

## Client Configuration

Use this stdio configuration pattern:

```json
{
  "mcpServers": {
    "syntx": {
      "command": "/absolute/path/to/syntx/.venv/bin/python",
      "args": ["/absolute/path/to/syntx/mcp_server.py"]
    }
  }
}
```

For VS Code, this repository includes:

```text
.vscode/mcp.json
```

It points to:

```text
${workspaceFolder}/.venv/bin/python
${workspaceFolder}/mcp_server.py
```

## Authentication Procedure

Authenticated tools require a saved Syntx bearer token.

Token file:

```text
~/.syntx_token.json
```

State file for in-progress image message IDs:

```text
~/.syntx_state.json
```

When the user is not authenticated:

1. Call `syntx_login_telegram`.
2. Give the returned Telegram bot link to the user.
3. Ask the user to approve the login in Telegram.
4. Call `syntx_check_auth` with the returned UUID.
5. If it says auth is not complete, wait briefly and call `syntx_check_auth` again.

Do not ask the user for a Syntx password. Authentication happens through Telegram.

## Tool Reference

### `syntx_login_telegram`

Starts Telegram authentication.

Inputs:

- None

Returns:

- Telegram auth link
- UUID for `syntx_check_auth`

Use first when the user has not logged in or receives an authentication error.

### `syntx_check_auth`

Checks Telegram auth completion and saves the token.

Inputs:

- `uuid`: UUID returned by `syntx_login_telegram`

Returns:

- Success message and token path when authenticated
- Retry message if the user has not approved login yet

### `syntx_create_chat`

Creates an image chat.

Inputs:

- `title`: optional chat title, default `New chat`

Returns:

- Chat UUID

Use when the user wants a named chat or wants to reuse a chat for multiple generations.

### `syntx_generate_image`

Starts image generation.

Inputs:

- `prompt`: required image prompt
- `chat_uuid`: optional existing chat UUID
- `aspect_ratio`: optional, default `16:9`
- `n`: optional image count, default `1`
- `model_type`: optional, default `banana`

Supported aspect ratios:

```text
21:9, 16:9, 9:16, 5:4, 4:5, 4:3, 3:4, 3:2, 2:3, 1:1
```

Important:

- If `chat_uuid` is empty, the server creates a new image chat automatically.
- This tool does not return the final image immediately.
- Use `syntx_get_image` with the returned chat UUID until the image is ready.

### `syntx_get_image`

Polls a chat for a generated image result.

Inputs:

- `chat_uuid`: required chat UUID

Returns:

- "Image not ready yet" while generation is in progress
- Final image URL and preview URLs when ready
- "No pending image found" when local state has no message ID for the chat

Recommended behavior:

- If the image is not ready, wait a few seconds and retry.
- If there is no pending image, call `syntx_get_chat_messages` to inspect chat history.

### `syntx_list_chats`

Lists image chats.

Inputs:

- `page_size`: optional, default `50`
- `search`: optional search string

Returns:

- Chat UUID
- Chat title
- Message count

Use when the user does not know the chat UUID.

### `syntx_get_chat_messages`

Gets messages in a chat.

Inputs:

- `chat_uuid`: required
- `page_size`: optional, default `20`

Returns:

- Prompt messages
- Image URLs
- Preview URL when available
- Message count/pagination summary

Use to inspect previous generations or recover image URLs.

### `syntx_logout`

Deletes the saved auth token.

Inputs:

- None

Returns:

- Logout status

Use when the user wants to disconnect Syntx or refresh credentials.

## Recommended Workflows

### First-Time Login

1. Call `syntx_login_telegram`.
2. Show the returned Telegram link to the user.
3. Wait for the user to approve login.
4. Call `syntx_check_auth` with the UUID.
5. Retry `syntx_check_auth` if approval is still pending.

### Generate a New Image

1. If authentication is missing, complete the login workflow.
2. Call `syntx_generate_image` with the user's prompt and desired settings.
3. Extract the chat UUID from the response.
4. Call `syntx_get_image` with that chat UUID.
5. If not ready, wait and poll again.
6. Return the final image URL to the user.

### Continue an Existing Chat

1. If the user knows the chat UUID, use it directly.
2. If not, call `syntx_list_chats`.
3. Pick the matching chat by title/message count.
4. Call `syntx_generate_image` with `chat_uuid`.
5. Poll with `syntx_get_image`.

### Retrieve Previous Images

1. Call `syntx_list_chats` if the chat UUID is unknown.
2. Call `syntx_get_chat_messages`.
3. Return the relevant image URLs and prompt context.

## Prompting Guidance

When generating images, help the user turn vague requests into useful prompts. Include:

- Subject
- Style or medium
- Composition
- Lighting
- Color palette
- Background/environment
- Output constraints such as aspect ratio

Example:

```text
A realistic product photo of a matte black smart speaker on a walnut desk, soft morning window light, shallow depth of field, clean modern workspace, premium commercial photography, 16:9.
```

Keep prompts concise enough for the image model to follow, but specific enough to guide composition.

## Error Handling

### Authentication error

If a tool raises:

```text
Not authenticated. Call syntx_login_telegram first.
```

Run the authentication workflow.

### Telegram approval pending

If `syntx_check_auth` returns:

```text
Not authenticated yet. Approve in Telegram and try again.
```

Ask the user to approve in Telegram, wait briefly, then retry.

### Image still generating

If `syntx_get_image` returns:

```text
Image not ready yet. Try again in a few seconds.
```

Poll again after a short wait.

### Missing pending state

If `syntx_get_image` returns:

```text
No pending image found for this chat_uuid.
```

Use `syntx_get_chat_messages` to inspect messages for that chat. The image may already be available in chat history, or the generation may have been started outside this MCP server.

## Security Notes

- Never expose the contents of `~/.syntx_token.json`.
- Do not commit token or state files.
- Prefer stdio transport for local clients.
- For HTTP mode, bind to `127.0.0.1` unless remote access is explicitly required.
- The server currently disables FastMCP DNS rebinding protection, so HTTP exposure should be treated carefully.

## Maintenance Notes

The Syntx API base URL used by the server is:

```text
https://api.syntx.ai/api/v1
```

The default image model is:

```text
banana
```

If Syntx changes auth, headers, endpoint paths, response fields, or model names, update `mcp_server.py` and this skill file together.
