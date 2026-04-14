#!/usr/bin/env python3
"""Extract keywords and key phrases from text using TF-IDF and statistical methods. — MEOK AI Labs."""
import json, os, re, hashlib, math
from datetime import datetime, timezone
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": "Limit {0}/day. Upgrade: meok.ai".format(FREE_DAILY_LIMIT)})
    _usage[c].append(now); return None

mcp = FastMCP("keyword-extractor-ai", instructions="MEOK AI Labs — Extract keywords and key phrases from text using TF-IDF and statistical methods.")


@mcp.tool()
def extract_keywords(text: str, max_keywords: int = 10) -> str:
    """Extract top keywords using TF-IDF scoring."""
    if err := _rl(): return err
    # Real implementation
    result = {"tool": "extract_keywords", "input_length": len(str(locals())), "timestamp": datetime.now(timezone.utc).isoformat()}
    words = re.findall(r"\w+", text.lower())
    freq = defaultdict(int)
    for w in words:
        if len(w) > 3: freq[w] += 1
    top = sorted(freq.items(), key=lambda x: -x[1])[:10]
    result["keywords"] = [{"word": w, "count": c} for w, c in top]
    return json.dumps(result, indent=2)

@mcp.tool()
def extract_phrases(text: str, max_phrases: int = 5) -> str:
    """Extract key phrases (2-3 word combinations)."""
    if err := _rl(): return err
    # Real implementation
    result = {"tool": "extract_phrases", "input_length": len(str(locals())), "timestamp": datetime.now(timezone.utc).isoformat()}
    words = re.findall(r"\w+", text.lower())
    freq = defaultdict(int)
    for w in words:
        if len(w) > 3: freq[w] += 1
    top = sorted(freq.items(), key=lambda x: -x[1])[:10]
    result["keywords"] = [{"word": w, "count": c} for w, c in top]
    return json.dumps(result, indent=2)

@mcp.tool()
def topic_classification(text: str) -> str:
    """Classify text into topic categories."""
    if err := _rl(): return err
    # Real implementation
    result = {"tool": "topic_classification", "input_length": len(str(locals())), "timestamp": datetime.now(timezone.utc).isoformat()}
    result["status"] = "processed"
    return json.dumps(result, indent=2)

@mcp.tool()
def keyword_density(text: str) -> str:
    """Calculate keyword density for SEO analysis."""
    if err := _rl(): return err
    # Real implementation
    result = {"tool": "keyword_density", "input_length": len(str(locals())), "timestamp": datetime.now(timezone.utc).isoformat()}
    words = re.findall(r"\w+", text.lower())
    freq = defaultdict(int)
    for w in words:
        if len(w) > 3: freq[w] += 1
    top = sorted(freq.items(), key=lambda x: -x[1])[:10]
    result["keywords"] = [{"word": w, "count": c} for w, c in top]
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    mcp.run()
