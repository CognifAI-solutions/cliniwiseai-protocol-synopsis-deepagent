import asyncio
import logging

import httpx
from clerk_backend_api import Clerk
from clerk_backend_api.security import AuthenticateRequestOptions
from langgraph_sdk import Auth

from settings import app_settings

auth = Auth()

clerk_sdk = Clerk(bearer_auth=app_settings.clerk_secret_key)

logger = logging.getLogger(__name__)
@auth.authenticate
async def authenticate(authorization: str | None) -> Auth.types.MinimalUserDict:
    if not authorization:
        raise Auth.exceptions.HTTPException(status_code=401, detail="Unauthorized")

    request = httpx.Request(
        "GET", "https://api", headers={"Authorization": authorization}
    )
    request_state = await asyncio.to_thread(
        clerk_sdk.authenticate_request,
        request,
        AuthenticateRequestOptions(),
    )

    if not request_state.is_signed_in:
        raise Auth.exceptions.HTTPException(status_code=401, detail="Unauthorized")

    payload = request_state.payload
    user_id = payload.get("sub") if payload else None
    clerk_user = (
        await asyncio.to_thread(clerk_sdk.users.get, user_id=user_id)
        if user_id
        else None
    )

    if not clerk_user:
        raise Auth.exceptions.HTTPException(status_code=401, detail="Unauthorized")

    return {
        "identity": clerk_user.id,
        "display_name": f"{clerk_user.first_name} {clerk_user.last_name}",
        "is_authenticated": True,
        "permissions": [],
    }