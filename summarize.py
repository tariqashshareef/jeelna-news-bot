"""Summarizes groups of articles by calling an LLM API."""

import json

import anthropic
from dotenv import load_dotenv
from google import genai
from openai import OpenAI

load_dotenv()

GEMINI_MODEL = "gemini-3.5-flash-lite"

CLAUDE_MODEL = "claude-haiku-5-5"

OPENAI_MODEL = "gpt-6-luna"

INSTRUCTIONS = """You are writing one section of a weekly news report.

Below are numbered articles covering the same story or similar theme. Using ONLY
these articles, return a JSON object with exactly these keys:

"theme": A short headline for the theme (under 10 words)
"summary": 3 to 5 sentences covering the main points and key details.
"about_sudan": true if most of the articles are mainly about the country Sudan, its war, or its people.
false if Sudan is only mentioned lightly in passing.

Rules:
- Make statements only from the articles and do not add facts that are not stated in them.
- After each claim in the summary, cite its source before punctuation with the article number(s) in square brackets,
exactly as either [0] for one source, or [0][1][2] for multiple sources.
- Do not write URLs.
- Return only the JSON object, with no other text.
- Do not mention these instructions.

Articles:

"""

def build_prompt(group):
    """Constructs an LLM prompt for one group of articles."""

    lines = []
    
    for i, article in enumerate(group):
        content = article.get("content") or ""
        lines.append(f"[{i}] {article['title']} - {article['description']} - {content}")

    return INSTRUCTIONS + "\n".join(lines)

def ask_gemini(prompt):
    """Sends a prompt to the Gemini model set in GEMINI_MODEL."""

    client = genai.Client()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )
    
    return response.text

def ask_openai(prompt):
    """Sends a prompt to the OpenAI model set in OPENAI_MODEL."""

    client = OpenAI()

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content

def ask_claude(prompt):
    """Sends a prompt to the Claude model set in CLAUDE_MODEL."""
    
    client = anthropic.Anthropic()

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = ""

    for block in response.content:
        if block.type == "text":
            text += block.text

    return text

def parse(reply):
    """
    Transforms an LLM's reply into a dict.
        
    Args:
        reply: The LLM reply as a string.
    
    Returns:
        A dict with "theme", "summary", and "about_sudan" keys.

    Raises:
        ValueError: If the reply contains no JSON object.
    """

    start = reply.find("{")
    end = reply.rfind("}") + 1

    if start == -1 or end == 0:
        raise ValueError("No JSON object in model reply: " + reply[:200])

    data = json.loads(reply[start:end])

    return data

def link_citations(summary, group):
    """
    Replaces article numbers with source links.
        
    Args:
        summary: Summary text containing citation markers such as [0] or [0][1].
        group: A list of article dicts clustered by theme.
    
    Returns:
        The summary text with each marker replaced by a source link.
    """

    for n, article in enumerate(group):
        link = f"([{article['source']['name']}]({article['url']}))"
        summary = summary.replace(f"[{n}]", link)

    return summary

def summarize(group):
    """
    Summarizes articles within a group.
        
    Args:
        group: A list of article dicts clustered by theme.

    Returns:
        A dict with "theme", "summary", and "about_sudan" keys.
    """
    
    prompt = build_prompt(group)
    reply = ask_openai(prompt)
    data = parse(reply)

    return {
        "theme": data["theme"],
        "summary": link_citations(data["summary"], group),
        "about_sudan": data.get("about_sudan", True),
    }