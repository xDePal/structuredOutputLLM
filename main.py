import json
import os
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional, Literal

# --- Config ---
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)
MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

# --- Schema ---
class Mention(BaseModel):
    product: Literal["app", "website", "not_applicable"]
    sentiment: Literal["positive", "negative", "neutral"]
    needs_response: bool
    response: Optional[str] = None
    support_ticket_description: Optional[str] = None

# --- Hardcoded mention ---
mention = "@techcorp great app and you are piece of shit"

# --- API call ---
completion = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": """Extract structured info from social media mentions. 
Respond only with valid JSON using exactly these fields:
- product: one of 'app', 'website', 'not_applicable'
- sentiment: one of 'positive', 'negative', 'neutral'
- needs_response: true or false
- response: optional string, null if not needed
- support_ticket_description: fill this field if there is a bug or an issue, null if not needed
"""},
        {"role": "user", "content": mention},
    ],
    response_format={"type": "json_object"},
)

# --- Parse ---
data = json.loads(completion.choices[0].message.content)
result = Mention(**data)

# --- Output ---
print(result)