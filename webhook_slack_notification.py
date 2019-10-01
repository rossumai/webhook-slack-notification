#!/usr/bin/env python3
import functools
import hashlib
import hmac
import os

import messages
import responder

api = responder.API()
SLACK_URL = os.getenv("SLACK_URL")
SECRET_KEY = os.getenv("SECRET_KEY", "secret")


def rossum_signature_required(view):
    @functools.wraps(view)
    async def wrapper(req: responder.Request, resp: responder.Response):
        digest = hmac.new(SECRET_KEY.encode(), await req.content, hashlib.sha1).hexdigest()
        if not hmac.compare_digest(req.headers["X-Elis-Signature"], f"sha1={digest}"):
            resp.status_code = api.status_codes.HTTP_401
        else:
            await view(req, resp)

    return wrapper


@api.route("/webhook")
@rossum_signature_required
async def webhook(req: responder.Request, resp: responder.Response) -> None:
    annotation = (await req.media())["annotation"]
    message = f"Status {annotation['previous_status']} ↝ {annotation['status']}"
    m = messages.SlackWebhook(body=message, auth=SLACK_URL)
    m.send_async()


if __name__ == "__main__":
    api.run()
