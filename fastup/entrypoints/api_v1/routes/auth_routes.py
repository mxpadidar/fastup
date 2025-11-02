import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

auth_router = APIRouter(prefix="/auth")

GITHUB_CLIENT_ID = "Ov23liiXYxsQGe2opHy7"
GITHUB_CLIENT_SECRET = "313f8c8aab2eadca074b7c6a8f9f40720837095d"


@auth_router.get("/oauth/github", response_class=RedirectResponse)
async def start_github_oauth():
    """
    Redirect user to GitHub's authorization endpoint.
    """
    url = "https://github.com/login/oauth/authorize"
    return f"{url}?client_id={GITHUB_CLIENT_ID}"


@auth_router.get("/oauth/callback/github")
async def github_callback(code: str | None = None):
    """
    GitHub redirects back here with ?code=...&state=... (or ?error=...)
    Exchange the code for an access token, fetch the user, then create a local session.
    """
    if not code:
        raise HTTPException(status_code=400, detail="Missing code or state")

    token_url = "https://github.com/login/oauth/access_token"
    headers = {"Accept": "application/json"}
    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            token_url,
            headers=headers,
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
            },
            timeout=10.0,
        )
        token_resp.raise_for_status()
        token_json = token_resp.json()

    access_token = token_json["access_token"]

    async with httpx.AsyncClient() as client:
        user_resp = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10.0,
        )
        user_resp.raise_for_status()
        user_json = user_resp.json()

    return JSONResponse(user_json)
