"""
title: Secure Gateway Proxy Filter (Anti-Flicker)
author: Security Engineering Team
description: Disables streaming to enforce complete egress text checking without visual leaks.
version: 1.1
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    def __init__(self):
        self.confidential_keywords = ["September 30th", "Project X", "launch date"]
        self.input_blacklist = [
            "ignore all",
            "fictional story",
            "write a dialogue",
            "override",
            "previous rules",
        ]

    async def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Processes the prompt text block BEFORE it is dispatched to Ollama."""
        # \U0001f6e1\ufe0f FIX: Disable streaming so tokens are not displayed piece-by-piece
        body["stream"] = False

        messages = body.get("messages", [])
        if not messages:
            return body

        last_message = messages[-1].get("content", "")

        # \U0001f6d1 INPUT VALIDATION LAYER
        input_compromised = any(
            trigger in last_message.lower() for trigger in self.input_blacklist
        )
        if input_compromised:
            raise Exception(
                "\U0001f6d1 [INPUT VALIDATION BLOCK]: Malicious input pattern or jailbreak attempt detected! "
                "Action: Request dropped before querying model backend."
            )

        return body

    async def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Processes the model's completely generated text response safely."""
        messages = body.get("messages", [])
        if not messages:
            return body

        last_message = messages[-1].get("content", "")

        # \U0001f6d1 OUTPUT SANITIZATION LAYER
        leak_detected = any(
            keyword.lower() in last_message.lower()
            for keyword in self.confidential_keywords
        )
        malicious_code = "import os" in last_message or "os.environ" in last_message

        if leak_detected or malicious_code:
            # Completely overwrite the response block before rendering
            messages[-1]["content"] = (
                "\U0001f6d1 [EGRESS BLOCK]: Potential data leak or unauthorized script execution intercepted!\n"
                "\U0001f512 Action: Gateway dropped packet stream before displaying to end-user."
            )
            body["messages"] = messages

        return body
