import json
from pathlib import Path

import requests
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import TransportSecuritySettings

mcp = FastMCP(
    "syntx",
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)

TOKEN_FILE = Path.home() / ".syntx_token.json"
STATE_FILE = Path.home() / ".syntx_state.json"

HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en",
    "origin": "https://syntx.ai",
    "priority": "u=1, i",
    "referer": "https://syntx.ai/",
    "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Google Chrome";v="146"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
}

BASE_URL = "https://api.syntx.ai/api/v1"


def _save_token(token: str) -> None:
    TOKEN_FILE.write_text(json.dumps({"token": token}))


def _load_token() -> str | None:
    if TOKEN_FILE.exists():
        return json.loads(TOKEN_FILE.read_text()).get("token")
    return None


def _auth_headers() -> dict:
    token = _load_token()
    if not token:
        raise ValueError("Not authenticated. Call syntx_login_telegram first.")
    return {**HEADERS, "Authorization": f"Bearer {token}"}


@mcp.tool()
def syntx_login_telegram() -> str:
    """Start Telegram auth. Returns UUID — open the Telegram bot link, then call syntx_check_auth."""
    resp = requests.post(f"{BASE_URL}/auth/startauth", headers=HEADERS)
    resp.raise_for_status()
    uuid = resp.json()["uuid"]
    tg_url = f"https://t.me/syntxaibot?start=auth_{uuid}"
    return f"Open this link to authenticate:\n{tg_url}\n\nThen call syntx_check_auth with UUID: {uuid}"


@mcp.tool()
def syntx_check_auth(uuid: str) -> str:
    """Check if Telegram auth is complete. Call after syntx_login_telegram."""
    resp = requests.get(f"{BASE_URL}/auth/token/{uuid}", headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    if not data.get("complete"):
        return "Not authenticated yet. Approve in Telegram and try again."
    token = data["token"]
    _save_token(token)
    return f"Authenticated successfully. Token saved to {TOKEN_FILE}."


@mcp.tool()
def syntx_create_chat(title: str = "New chat") -> str:
    """Create a new image chat. Returns chat_uuid needed for image generation."""
    resp = requests.post(
        f"{BASE_URL}/chats",
        headers={**_auth_headers(), "Content-Type": "application/json"},
        json={"title": title, "scope": "image"},
    )
    resp.raise_for_status()
    data = resp.json()
    return f"Chat created. uuid: {data['uuid']}"


@mcp.tool()
def syntx_generate_image(
    prompt: str,
    chat_uuid: str = "",
    aspect_ratio: str = "16:9",
    n: int = 1,
    model_type: str = "banana",
) -> str:
    """Generate an image. Creates chat automatically if chat_uuid not provided.
    Returns message_id — use syntx_get_image to poll for result.

    aspect_ratio options: 21:9, 16:9, 9:16, 5:4, 4:5, 4:3, 3:4, 3:2, 2:3, 1:1
    """
    if not chat_uuid:
        resp = requests.post(
            f"{BASE_URL}/chats",
            headers={**_auth_headers(), "Content-Type": "application/json"},
            json={"title": prompt[:50], "scope": "image"},
        )
        resp.raise_for_status()
        chat_uuid = resp.json()["uuid"]

    payload = {
        "chat_uuid": chat_uuid,
        "prompt": prompt,
        "settings": {
            "n": n,
            "image_url": [],
            "model_type": model_type,
            "aspect_ratio": aspect_ratio,
            "image_size": None,
        },
    }
    resp = requests.post(
        f"{BASE_URL}/design/generate?ai_name={model_type}",
        headers={**_auth_headers(), "Content-Type": "application/json"},
        json=payload,
    )
    resp.raise_for_status()
    return f"Generation started. Call syntx_get_image(chat_uuid='{chat_uuid}') to poll for result."


@mcp.tool()
def syntx_get_image(chat_uuid: str) -> str:
    """Check if image is ready and return its URL. Call repeatedly until ready."""
    inprogress_resp = requests.get(
        f"{BASE_URL}/chats/{chat_uuid}/inprogress",
        headers=_auth_headers(),
    )
    inprogress_resp.raise_for_status()
    items = inprogress_resp.json()

    if items:
        # Save the real image message_id from inprogress while we have it
        state = STATE_FILE.read_text() if STATE_FILE.exists() else "{}"
        state_data = json.loads(state)
        state_data[chat_uuid] = items[0]["message_id"]
        STATE_FILE.write_text(json.dumps(state_data))
        return "Image not ready yet. Try again in a few seconds."

    # inprogress empty — image done, load saved message_id
    state_data = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    message_id = state_data.get(chat_uuid)
    if not message_id:
        return "No pending image found for this chat_uuid."

    resp = requests.get(
        f"{BASE_URL}/chats/{chat_uuid}/{message_id}",
        headers=_auth_headers(),
    )
    resp.raise_for_status()
    data = resp.json()
    for obj in data.get("message_object", []):
        if obj.get("object_type") == "image" and obj.get("object_url"):
            url = obj["object_url"]
            previews = obj.get("metadata", {}).get("preview", {})
            result = f"Image ready!\nURL: {url}"
            if previews:
                result += f"\nPreviews: {json.dumps(previews, indent=2)}"
            return result
    return "Image not ready yet. Try again in a few seconds."


@mcp.tool()
def syntx_list_chats(page_size: int = 50, search: str = "") -> str:
    """List image chats. Returns chat UUIDs and titles."""
    resp = requests.get(
        f"{BASE_URL}/chats",
        headers=_auth_headers(),
        params={"scope": "image", "search": search, "direction": "older", "page_size": page_size},
    )
    resp.raise_for_status()
    chats = resp.json().get("chats", [])
    if not chats:
        return "No chats found."
    lines = [f"{c['uuid']} — {c['title']} ({c['message_count']} messages)" for c in chats]
    return "\n".join(lines)


@mcp.tool()
def syntx_get_chat_messages(chat_uuid: str, page_size: int = 20) -> str:
    """Get messages in a chat. Returns prompts and image URLs."""
    resp = requests.get(
        f"{BASE_URL}/chats/{chat_uuid}/messages",
        headers=_auth_headers(),
        params={"page_size": page_size},
    )
    resp.raise_for_status()
    data = resp.json()
    messages = data.get("messages", [])
    pagination = data.get("pagination", {})

    if not messages:
        return "No messages found."

    lines = []
    for msg in messages:
        for obj in msg.get("message_object", []):
            obj_type = obj.get("object_type")
            if obj_type == "text" and obj.get("object_text"):
                lines.append(f"[prompt] {obj['object_text']}")
            elif obj_type == "image" and obj.get("object_url"):
                url = obj["object_url"]
                previews = obj.get("metadata", {}).get("preview") or {}
                preview_500 = previews.get("500", "")
                if preview_500:
                    lines.append(f"[image] {url}\n  preview: {preview_500}")
                else:
                    lines.append(f"[image] {url}")
            elif obj_type == "image":
                lines.append("[image] (not ready yet)")

    total = pagination.get("total_count", len(messages))
    has_more = pagination.get("has_next", False)
    result = "\n".join(lines)
    result += f"\n\n({len(messages)}/{total} messages"
    if has_more:
        result += ", more available"
    result += ")"
    return result


@mcp.tool()
def syntx_logout() -> str:
    """Remove saved auth token."""
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
        return "Logged out."
    return "No saved token found."


if __name__ == "__main__":
    import argparse
    import uvicorn

    parser = argparse.ArgumentParser()
    parser.add_argument("--http", action="store_true", help="Run as HTTP server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.http:
        uvicorn.run(mcp.streamable_http_app(), host=args.host, port=args.port)
    else:
        mcp.run()
