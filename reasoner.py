import os
import requests
import json
from typing import Dict, Any, Optional

class LLMReasoner:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY", "").strip()
        self.model = os.getenv("LLM_MODEL", "gemini-1.5-flash").strip()
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower().strip()

    def enhance_insight_explanation(self, insight_data: Dict[str, Any]) -> str:
        """
        Synthesizes a business-friendly explanation.
        Falls back to rule-based template if no API key is provided or request fails.
        """
        if not self.api_key:
            return self._fallback_explanation(insight_data)

        prompt = (
            f"You are PRISM's business reasoning engine. Synthesize a concise 2-sentence executive summary "
            f"for this grounded analytical finding:\n"
            f"Metric: {insight_data.get('metric_name')}\n"
            f"Change: {insight_data.get('change_pct')}%\n"
            f"Segment: {insight_data.get('affected_segment')}\n"
            f"What Happened: {insight_data.get('what_happened')}\n"
            f"Do not hallucinate numbers outside this data."
        )

        try:
            if self.provider == "gemini":
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                res = requests.post(url, json=payload, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                    return text
            elif self.provider in ["openai", "groq"]:
                base_url = "https://api.openai.com/v1" if self.provider == "openai" else "https://api.groq.com/openai/v1"
                headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": self.model if self.provider == "openai" else "llama-3.1-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 150
                }
                res = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=5)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"].strip()
        except Exception:
            pass

        return self._fallback_explanation(insight_data)

    def _fallback_explanation(self, insight_data: Dict[str, Any]) -> str:
        metric = insight_data.get("metric_name", "Metric").title()
        pct = insight_data.get("change_pct", 0.0)
        seg = insight_data.get("affected_segment", "Overall")
        direction = "decreased" if pct < 0 else "increased"

        return (
            f"Analysis reveals that {metric} {direction} by {abs(pct):.1f}% in the current period, "
            f"with variance heavily concentrated in {seg}. Grounded evidence indicates operational factors require review."
        )

reasoner = LLMReasoner()
