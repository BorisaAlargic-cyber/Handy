"""
LLM utilities for Handy – two non-trivial LLM features:

Feature 1 – Natural language job parsing (multi-call, structured output):
  parse_job_request(text) → dict with extracted search parameters
  explain_top_match(job_summary, provider) → string narrative

Feature 2 – Job description enhancer (booking page):
  enhance_job_description(raw_desc, category) → polished professional brief
"""

import json
import os
import anthropic

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        _client = anthropic.Anthropic(api_key=api_key)
    return _client


# ── FEATURE 1a: Parse free-text job request into structured search params ──────

PARSE_SYSTEM = """You are a job-intake parser for Handy, a home-services marketplace.
Extract search parameters from the user's natural-language request.

Return ONLY valid JSON — no markdown, no explanation, no backticks — with these exact keys:
{
  "category":      one of ["All","Electrician","Cleaning","Plumber","Handyman","Gardening"],
  "urgency":       one of ["ASAP (today/tomorrow)","This week","Flexible"],
  "max_price":     integer hourly rate in euros (default 60 if not mentioned),
  "max_distance":  integer km (default 5 if not mentioned),
  "preferred_day": one of ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] (best guess from context, default "Mon"),
  "min_rating":    float between 4.0 and 5.0 (default 4.5 if not mentioned),
  "job_summary":   string, 1–2 sentence plain-English summary of the job
}

Rules:
- Infer category from job description keywords (e.g. pipe/leak/boiler → Plumber, wiring/fuse/socket → Electrician)
- If multiple categories fit, pick the most specific one
- "today","urgent","emergency","ASAP","right now" → urgency = "ASAP (today/tomorrow)"
- "this week","soon","few days" → urgency = "This week"
- No time pressure mentioned → urgency = "Flexible"
- Budget/price hints: "cheap","budget" → max_price=35; "don't mind paying" → max_price=90
- Nearby/close → max_distance=2; no preference → max_distance=5"""


def parse_job_request(text: str) -> dict | None:
    """
    Call 1: Extract structured search params from free-text job request.
    Returns a dict or None on failure.
    """
    client = _get_client()
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=400,
            system=PARSE_SYSTEM,
            messages=[{"role": "user", "content": text}],
        )
        raw = response.content[0].text.strip()
        return json.loads(raw)
    except Exception:
        return None


# ── FEATURE 1b: Generate personalised match explanation ────────────────────────

EXPLAIN_SYSTEM = """You are a concise, helpful assistant for Handy, a home-services marketplace.
Given a job request and the top-matched provider, write a 2–3 sentence explanation of why
this provider is the best match. Be specific: reference the job details, the provider's
specialisms, tags, experience and price. Keep it warm and reassuring. No markdown, plain text."""


def explain_top_match(job_summary: str, provider: dict) -> str:
    """
    Call 2: Given the parsed job summary and top provider, explain the recommendation.
    Returns explanation string, or empty string on failure.
    """
    client = _get_client()
    prompt = (
        f"Job: {job_summary}\n\n"
        f"Provider: {provider['name']}, {provider['category']}, "
        f"{provider['experience']} years experience, €{provider['price']}/hr, "
        f"{provider['distance']} km away, rating {provider['rating']}/5. "
        f"Tags: {', '.join(provider['tags'])}. "
        f"Bio: {provider['bio']}"
    )
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            system=EXPLAIN_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception:
        return ""


# ── FEATURE 2: Enhance job description for the booking page ───────────────────

ENHANCE_SYSTEM = """You are a professional assistant helping homeowners communicate
clearly with tradespeople. Rewrite the user's rough job description into a concise,
professional job brief that a tradesperson would find useful.

Rules:
- Keep it under 80 words
- Use plain, direct language — no fluff
- Structure: what the problem is → what needs doing → any relevant details (location in home, symptoms, urgency)
- Do NOT invent details that weren't mentioned
- Return plain text only, no markdown, no bullet points"""


def enhance_job_description(raw_desc: str, category: str) -> str:
    """
    Call 3 (booking page): Rewrite rough job description into professional brief.
    Returns enhanced string, or original text on failure.
    """
    client = _get_client()
    prompt = f"Service type: {category}\nRaw description: {raw_desc}"
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=200,
            system=ENHANCE_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception:
        return raw_desc
