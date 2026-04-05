# llm_client.py — Unified LLM provider helper
#
# Auto-detects whichever API key / local model you have configured and wraps
# it in a common interface so all Stage 4 scripts work regardless of provider.
#
# Supported providers (in priority order):
#   Claude  → set ANTHROPIC_API_KEY   (https://console.anthropic.com)
#   OpenAI  → set OPENAI_API_KEY      (https://platform.openai.com)
#   Gemini  → set GOOGLE_API_KEY      (https://aistudio.google.com)
#   Ollama  → set OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B  (local, no key needed — https://ollama.com)
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
    elif os.environ.get("OLLAMA_MODEL"):
        model = os.environ["OLLAMA_MODEL"]
        print(f"Provider: Ollama (local) — model: {model}")
        return "ollama", _OllamaClient(model)
    else:
        print(
            "\nNo provider configured. Choose one:\n"
            "  set ANTHROPIC_API_KEY=...    (Claude — cloud)\n"
            "  set OPENAI_API_KEY=...       (OpenAI — cloud)\n"
            "  set GOOGLE_API_KEY=...       (Gemini — cloud, free tier)\n"
            "  set OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B   (Ollama — local, no key needed)\n"
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


class _OllamaClient:
    """Ollama — runs any model locally, no API key required.

    Install Ollama: https://ollama.com
    Pull a model:   ollama pull huihui_ai/qwen3.5-abliterated:2B
    Set env var:    set OLLAMA_MODEL=huihui_ai/qwen3.5-abliterated:2B
    """

    def __init__(self, model: str):
        try:
            import ollama as _ollama
        except ImportError:
            raise ImportError("Run: pip install ollama")
        self._ollama = _ollama
        self.model = model

    def _build_messages(self, system: str, messages: list) -> list:
        return [{"role": "system", "content": system}] + messages

    def chat(self, system: str, messages: list, max_tokens: int = 600) -> str:
        response = self._ollama.chat(
            model=self.model,
            messages=self._build_messages(system, messages),
            options={"num_predict": max_tokens},
        )
        return response["message"]["content"]

    def stream(self, system: str, messages: list, max_tokens: int = 600):
        """Yield text chunks as they arrive."""
        for chunk in self._ollama.chat(
            model=self.model,
            messages=self._build_messages(system, messages),
            options={"num_predict": max_tokens},
            stream=True,
        ):
            content = chunk.get("message", {}).get("content", "")
            if content:
                yield content
