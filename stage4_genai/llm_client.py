# llm_client.py — Unified LLM provider helper
#
# Auto-detects whichever API key you have set and wraps it in a
# common interface so all Stage 4 scripts work regardless of provider.
#
# Supported providers (set ONE of these environment variables):
#   Claude  → ANTHROPIC_API_KEY   (https://console.anthropic.com)
#   OpenAI  → OPENAI_API_KEY      (https://platform.openai.com)
#   Gemini  → GOOGLE_API_KEY      (https://aistudio.google.com)
#
# Usage:
#   from llm_client import get_client
#   provider, client = get_client()
#   response = client.chat(system="You are...", messages=[{"role": "user", "content": "..."}])

import os


def get_client():
    """
    Auto-detect available API key and return (provider_name, client).
    Priority: Claude → OpenAI → Gemini
    Returns ("none", None) if no key is found.
    """
    if os.environ.get("ANTHROPIC_API_KEY"):
        print("Provider: Claude (Anthropic)")
        return "claude", _ClaudeClient()
    elif os.environ.get("OPENAI_API_KEY"):
        print("Provider: OpenAI")
        return "openai", _OpenAIClient()
    elif os.environ.get("GOOGLE_API_KEY"):
        print("Provider: Gemini (Google)")
        return "gemini", _GeminiClient()
    else:
        print(
            "\nNo API key found. Set one of:\n"
            "  set ANTHROPIC_API_KEY=...   (Claude)\n"
            "  set OPENAI_API_KEY=...      (OpenAI)\n"
            "  set GOOGLE_API_KEY=...      (Gemini)\n"
        )
        return "none", None


# ── Provider implementations ───────────────────────────────────────────────────

class _ClaudeClient:
    """Anthropic Claude — claude-sonnet-4-6"""

    def __init__(self):
        try:
            import anthropic
        except ImportError:
            raise ImportError("Run: pip install anthropic")
        self._client = anthropic.Anthropic()
        self.model = "claude-sonnet-4-6"

    def chat(self, system: str, messages: list, max_tokens: int = 600) -> str:
        response = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        return response.content[0].text

    def stream(self, system: str, messages: list, max_tokens: int = 600):
        """Yield text chunks as they arrive."""
        with self._client.messages.stream(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        ) as s:
            for chunk in s.text_stream:
                yield chunk


class _OpenAIClient:
    """OpenAI — gpt-4o-mini (fast and cheap; swap model for gpt-4o if needed)"""

    def __init__(self):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("Run: pip install openai")
        self._client = OpenAI()
        self.model = "gpt-4o-mini"

    def chat(self, system: str, messages: list, max_tokens: int = 600) -> str:
        full = [{"role": "system", "content": system}] + messages
        response = self._client.chat.completions.create(
            model=self.model,
            messages=full,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    def stream(self, system: str, messages: list, max_tokens: int = 600):
        """Yield text chunks as they arrive."""
        full = [{"role": "system", "content": system}] + messages
        stream = self._client.chat.completions.create(
            model=self.model,
            messages=full,
            max_tokens=max_tokens,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta


class _GeminiClient:
    """Google Gemini — gemini-1.5-flash"""

    def __init__(self):
        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("Run: pip install google-generativeai")
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self._genai = genai
        self.model = "gemini-1.5-flash"

    def _build_prompt(self, system: str, messages: list) -> str:
        """Gemini uses a single prompt string rather than a message list."""
        parts = [system, ""]
        for msg in messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            parts.append(f"{role}: {msg['content']}")
        parts.append("Assistant:")
        return "\n".join(parts)

    def chat(self, system: str, messages: list, max_tokens: int = 600) -> str:
        model = self._genai.GenerativeModel(self.model)
        response = model.generate_content(
            self._build_prompt(system, messages),
            generation_config={"max_output_tokens": max_tokens},
        )
        return response.text

    def stream(self, system: str, messages: list, max_tokens: int = 600):
        """Yield text chunks as they arrive."""
        model = self._genai.GenerativeModel(self.model)
        response = model.generate_content(
            self._build_prompt(system, messages),
            generation_config={"max_output_tokens": max_tokens},
            stream=True,
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text
