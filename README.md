# Syntx MCP Server

Syntx MCP Server is a small Python MCP server for using the Syntx.ai image generation API from MCP-compatible clients such as Claude Desktop, Claude Code, Cursor, VS Code, or any client that supports stdio or Streamable HTTP MCP servers.

The server handles Telegram-based Syntx authentication, creates image chats, starts image generation jobs, polls for finished images, and lists previous image chats/messages.

## Features

- Telegram login flow for Syntx.ai
- Persistent local token storage
- Image chat creation
- Async image generation with polling
- Chat and message listing
- stdio transport for local MCP clients
- Streamable HTTP transport for clients that connect over HTTP

## Requirements

- Python 3.10 or newer
- A Syntx.ai account that can authenticate through the Syntx Telegram bot
- An MCP-compatible client

Python packages:

```bash
pip install "mcp[cli]" requests uvicorn
```

## Quick Start

Clone or copy this repository, then create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]" requests uvicorn
```

Run the MCP server over stdio:

```bash
python mcp_server.py
```

For HTTP mode:

```bash
python mcp_server.py --http --host 127.0.0.1 --port 8000
```

## MCP Client Configuration

This repository can be used in two complementary ways:

- As an MCP server: clients call the real Syntx tools from `mcp_server.py`.
- As a Claude skill: agents read `.claude/skills/syntx/SKILL.md` to learn when and how to use the Syntx MCP tools.

### VS Code

This repository already includes `.vscode/mcp.json`:

```json
{
  "servers": {
    "syntx": {
      "type": "stdio",
      "command": "${workspaceFolder}/.venv/bin/python",
      "args": ["${workspaceFolder}/mcp_server.py"]
    }
  }
}
```

After installing dependencies, reload VS Code or restart the MCP server from the MCP panel.

### Claude Desktop

Add this server to your Claude Desktop MCP configuration. Replace `/absolute/path/to/syntx` with the actual repository path.

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

Restart Claude Desktop after saving the configuration.

### Claude Project Skill

This repository includes a project skill at:

```text
.claude/skills/syntx/SKILL.md
```

That skill does not replace the MCP server. It teaches Claude how to use the Syntx MCP tools correctly: authenticate through Telegram, generate images, poll for results, inspect old chats, and handle common errors.

Use both together for the best experience:

1. Configure the `syntx` MCP server.
2. Keep `.claude/skills/syntx/SKILL.md` in the project.
3. Ask Claude for Syntx image generation or Syntx chat/image retrieval.

### Claude Code

From this repository:

```bash
claude mcp add syntx .venv/bin/python mcp_server.py
```

Or use absolute paths:

```bash
claude mcp add syntx /absolute/path/to/syntx/.venv/bin/python /absolute/path/to/syntx/mcp_server.py
```

### Streamable HTTP

Start the server:

```bash
python mcp_server.py --http --host 127.0.0.1 --port 8000
```

Then configure your MCP client to connect to the Streamable HTTP endpoint exposed by the FastMCP app on that host and port. The exact URL format depends on the client.

## Authentication Flow

Syntx uses Telegram authentication. The MCP server stores the returned bearer token in:

```text
~/.syntx_token.json
```

The token is local to the machine and user account running the server.

1. Call `syntx_login_telegram`.
2. Open the returned Telegram bot link.
3. Approve login in Telegram.
4. Call `syntx_check_auth` with the returned UUID.
5. After success, authenticated tools can be used.

To remove the saved token, call `syntx_logout`.

## Available Tools

### `syntx_login_telegram`

Starts Telegram authentication.

Input: none

Returns:

- Telegram bot authentication link
- UUID to pass into `syntx_check_auth`

Example prompt:

```text
Use syntx_login_telegram so I can connect my Syntx account.
```

### `syntx_check_auth`

Checks whether Telegram authentication is complete and saves the token.

Input:

- `uuid` string: UUID returned by `syntx_login_telegram`

Returns:

- Success message when token is saved
- Waiting message if Telegram approval is not complete yet

Example prompt:

```text
Check Syntx auth with UUID abc123...
```

### `syntx_create_chat`

Creates a new Syntx image chat.

Input:

- `title` string, optional: chat title. Default is `New chat`.

Returns:

- Created chat UUID

Example prompt:

```text
Create a Syntx image chat titled "Product mockups".
```

### `syntx_generate_image`

Starts image generation. If `chat_uuid` is omitted, the server creates a new image chat automatically.

Inputs:

- `prompt` string, required: image prompt
- `chat_uuid` string, optional: existing chat UUID
- `aspect_ratio` string, optional: default `16:9`
- `n` integer, optional: number of images, default `1`
- `model_type` string, optional: default `banana`

Supported aspect ratios:

```text
21:9, 16:9, 9:16, 5:4, 4:5, 4:3, 3:4, 3:2, 2:3, 1:1
```

Returns:

- Message telling you generation has started
- Chat UUID to use with `syntx_get_image`

Example prompt:

```text
Generate a 16:9 image in Syntx: a clean futuristic workspace, realistic lighting.
```

### `syntx_get_image`

Polls an image chat until the generated image is ready.

Input:

- `chat_uuid` string, required

Returns:

- "Image not ready yet" while generation is running
- Final image URL and preview URLs when ready
- "No pending image found" if the server has no saved pending message for that chat

Example prompt:

```text
Check whether the Syntx image for chat UUID ... is ready.
```

### `syntx_list_chats`

Lists image chats.

Inputs:

- `page_size` integer, optional: default `50`
- `search` string, optional: filter by title/search text

Returns:

- Chat UUIDs, titles, and message counts

Example prompt:

```text
List my latest Syntx image chats.
```

### `syntx_get_chat_messages`

Lists messages in an image chat, including prompts and image URLs.

Inputs:

- `chat_uuid` string, required
- `page_size` integer, optional: default `20`

Returns:

- Prompt texts
- Image URLs and previews
- Pagination summary

Example prompt:

```text
Show messages from this Syntx chat UUID: ...
```

### `syntx_logout`

Removes the saved token from `~/.syntx_token.json`.

Input: none

Returns:

- Logout status

Example prompt:

```text
Log out from Syntx.
```

## Typical Workflow

1. Authenticate:

```text
Call syntx_login_telegram.
```

2. Open the returned Telegram link and approve the login.

3. Complete auth:

```text
Call syntx_check_auth with the UUID from step 1.
```

4. Generate an image:

```text
Call syntx_generate_image with prompt "A cinematic product photo of a black smart speaker on a walnut desk" and aspect_ratio "16:9".
```

5. Poll result:

```text
Call syntx_get_image with the returned chat UUID until the image URL is ready.
```

## Local Files

The server writes two files in the current user's home directory:

```text
~/.syntx_token.json
~/.syntx_state.json
```

`~/.syntx_token.json` stores the Syntx bearer token after login.

`~/.syntx_state.json` stores in-progress image message IDs by `chat_uuid`, so `syntx_get_image` can fetch the completed image after Syntx finishes generation.

Do not commit these files or share them with other users.

## Troubleshooting

### `Not authenticated. Call syntx_login_telegram first.`

Run `syntx_login_telegram`, approve the Telegram login, then call `syntx_check_auth` with the UUID.

### `Not authenticated yet. Approve in Telegram and try again.`

Telegram approval has not completed. Open the bot link, approve login, wait a few seconds, and call `syntx_check_auth` again.

### `Image not ready yet. Try again in a few seconds.`

Image generation is still running. Call `syntx_get_image` again after a short delay.

### `No pending image found for this chat_uuid.`

The local state file does not contain a pending message ID for that chat. This can happen if the server was not used to start the generation, state was deleted, or generation finished before the server observed the in-progress item. Use `syntx_get_chat_messages` to inspect the chat history.

### HTTP server starts but client cannot connect

Use `--host 127.0.0.1` for local-only access. If connecting from another machine, use `--host 0.0.0.0` and make sure firewall/network rules allow the chosen port.

## Security Notes

- The server disables FastMCP DNS rebinding protection in code because it is intended to be run in controlled local/client environments.
- Prefer stdio transport for local desktop clients.
- If using HTTP mode, bind to `127.0.0.1` unless you intentionally need network access.
- The saved Syntx token grants access to your Syntx account. Keep `~/.syntx_token.json` private.

## Development

Run the server locally:

```bash
source .venv/bin/activate
python mcp_server.py
```

Run in HTTP mode:

```bash
source .venv/bin/activate
python mcp_server.py --http --host 127.0.0.1 --port 8000
```

Basic import check:

```bash
python -m py_compile mcp_server.py
```

## Project Structure

```text
.
├── README.md
├── SKILL.md
├── CLAUDE.md
├── mcp_server.py
└── .vscode/
    └── mcp.json
```

## Notes

Syntx image generation is asynchronous. `syntx_generate_image` only starts generation; use `syntx_get_image` repeatedly to retrieve the final image URL.
