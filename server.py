#!/usr/bin/env python3
"""Extract keywords and key phrases from text using TF-IDF and statistical methods. — MEOK AI Labs."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json, re, math
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": "Limit {0}/day. Upgrade: meok.ai".format(FREE_DAILY_LIMIT)})
    _usage[c].append(now); return None

mcp = FastMCP("keyword-extractor-ai", instructions="MEOK AI Labs — Extract keywords, phrases, and tags from text using TF-IDF and statistical analysis.")

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "could", "should", "may", "might", "shall",
    "can", "this", "that", "these", "those", "it", "its", "i", "me", "my", "we", "our",
    "you", "your", "he", "she", "they", "them", "their", "who", "which", "what", "where",
    "when", "how", "why", "not", "no", "nor", "so", "if", "then", "than", "too", "very",
    "just", "about", "up", "out", "all", "also", "as", "into", "more", "some", "such",
    "only", "other", "new", "like", "each", "much", "both", "after", "before", "between",
    "through", "over", "under", "above", "below", "any", "same", "here", "there",
}

TAG_CATEGORIES = {
    "technology": ["software", "hardware", "programming", "code", "algorithm", "database", "api",
                    "cloud", "server", "network", "machine learning", "artificial intelligence", "ai",
                    "ml", "python", "javascript", "data", "computing", "web", "mobile", "security"],
    "business": ["revenue", "profit", "market", "customer", "strategy", "growth", "sales",
                  "management", "enterprise", "startup", "investment", "roi", "kpi", "analytics"],
    "healthcare": ["patient", "treatment", "diagnosis", "clinical", "medical", "health",
                    "pharmaceutical", "therapy", "hospital", "disease", "symptoms", "doctor"],
    "education": ["learning", "student", "teacher", "course", "curriculum", "training",
                   "university", "school", "knowledge", "skill", "assessment", "degree"],
    "science": ["research", "experiment", "hypothesis", "theory", "study", "analysis",
                 "data", "methodology", "publication", "peer review", "laboratory"],
}


def _tokenize(text: str) -> list:
    words = re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())
    return [w for w in words if w not in STOP_WORDS]


def _tf_scores(words: list) -> dict:
    freq = defaultdict(int)
    for w in words:
        freq[w] += 1
    total = len(words)
    return {w: round(c / total, 6) for w, c in freq.items()}


def _ngrams(words: list, n: int) -> list:
    return [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]


@mcp.tool()
def extract_keywords(text: str, max_keywords: int = 10, min_word_length: int = 3,
                      api_key: str = "") -> str:
    """Extract top keywords using TF-IDF scoring with stop word filtering and frequency analysis."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    words = _tokenize(text)
    words = [w for w in words if len(w) >= min_word_length]

    if not words:
        return {"keywords": [], "error": "No keywords found after filtering",
                "timestamp": datetime.now(timezone.utc).isoformat()}

    tf = _tf_scores(words)
    freq = defaultdict(int)
    for w in words:
        freq[w] += 1

    unique_words = len(set(words))
    idf_boost = {w: math.log(unique_words / max(c, 1)) + 1 for w, c in freq.items()}
    scores = {w: round(tf[w] * idf_boost.get(w, 1), 6) for w in tf}

    ranked = sorted(scores.items(), key=lambda x: -x[1])[:max_keywords]
    keywords = [{"keyword": w, "score": s, "frequency": freq[w],
                  "tf": tf[w], "relevance": round(s / max(ranked[0][1], 0.001) * 100, 1)}
                 for w, s in ranked]

    return {
        "keywords": keywords,
        "total_words": len(words),
        "unique_words": unique_words,
        "vocabulary_richness": round(unique_words / max(len(words), 1), 3),
        "text_length": len(text),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def analyze_density(text: str, target_keywords: str = "", api_key: str = "") -> str:
    """Calculate keyword density for SEO analysis, with target keyword tracking and recommendations."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    all_words = re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())
    total_words = len(all_words)
    content_words = _tokenize(text)

    freq = defaultdict(int)
    for w in content_words:
        freq[w] += 1

    density = []
    for word, count in sorted(freq.items(), key=lambda x: -x[1])[:20]:
        pct = round(count / max(total_words, 1) * 100, 2)
        status = "optimal" if 1.0 <= pct <= 3.0 else "low" if pct < 1.0 else "over-optimized"
        density.append({"keyword": word, "count": count, "density_pct": pct, "status": status})

    target_report = []
    if target_keywords:
        targets = [t.strip().lower() for t in target_keywords.split(",") if t.strip()]
        for target in targets:
            target_words = target.split()
            if len(target_words) == 1:
                count = freq.get(target, 0)
            else:
                count = text.lower().count(target)
            pct = round(count / max(total_words, 1) * 100, 2)
            ideal = 2.0
            target_report.append({
                "keyword": target,
                "count": count,
                "density_pct": pct,
                "ideal_density_pct": ideal,
                "gap": round(ideal - pct, 2),
                "recommendation": "Good" if 1.0 <= pct <= 3.0 else f"Add {max(1, int((ideal - pct) / 100 * total_words))} more occurrences" if pct < 1.0 else "Reduce usage to avoid keyword stuffing",
            })

    return {
        "total_words": total_words,
        "unique_content_words": len(freq),
        "top_keywords_density": density,
        "target_keywords": target_report,
        "seo_notes": [
            "Ideal keyword density: 1-3% for primary keywords",
            "Avoid exceeding 3% to prevent keyword stuffing penalties",
            f"Content length: {'good' if total_words >= 300 else 'short — aim for 300+ words'} ({total_words} words)",
        ],
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def suggest_tags(text: str, max_tags: int = 10, api_key: str = "") -> str:
    """Suggest tags and categories for content based on keyword analysis and topic matching."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    words = _tokenize(text)
    freq = defaultdict(int)
    for w in words:
        freq[w] += 1

    top_words = sorted(freq.items(), key=lambda x: -x[1])[:20]
    single_tags = [w for w, c in top_words if len(w) >= 4][:max_tags]

    bigrams = _ngrams(words, 2)
    bigram_freq = defaultdict(int)
    for bg in bigrams:
        bigram_freq[bg] += 1
    phrase_tags = [bg for bg, c in sorted(bigram_freq.items(), key=lambda x: -x[1])[:5] if c >= 2]

    category_scores = {}
    text_lower = text.lower()
    for category, indicators in TAG_CATEGORIES.items():
        score = sum(1 for ind in indicators if ind in text_lower)
        if score > 0:
            category_scores[category] = score

    ranked_categories = sorted(category_scores.items(), key=lambda x: -x[1])
    primary_category = ranked_categories[0][0] if ranked_categories else "general"

    all_tags = list(dict.fromkeys(single_tags + phrase_tags))[:max_tags]
    hashtags = ["#" + t.replace(" ", "") for t in all_tags]

    return {
        "tags": all_tags,
        "phrase_tags": phrase_tags,
        "hashtags": hashtags,
        "categories": [{"category": cat, "score": sc} for cat, sc in ranked_categories[:5]],
        "primary_category": primary_category,
        "total_tags": len(all_tags),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def compare_keywords(text_a: str, text_b: str, api_key: str = "") -> str:
    """Compare keywords between two texts to find common, unique, and differentiating terms."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    words_a = _tokenize(text_a)
    words_b = _tokenize(text_b)
    freq_a = defaultdict(int)
    freq_b = defaultdict(int)
    for w in words_a:
        freq_a[w] += 1
    for w in words_b:
        freq_b[w] += 1

    set_a = set(freq_a.keys())
    set_b = set(freq_b.keys())

    common = set_a & set_b
    only_a = set_a - set_b
    only_b = set_b - set_a

    common_details = sorted([{"keyword": w, "count_a": freq_a[w], "count_b": freq_b[w],
                               "ratio": round(freq_a[w] / max(freq_b[w], 1), 2)} for w in common],
                             key=lambda x: -(x["count_a"] + x["count_b"]))[:15]

    only_a_ranked = sorted([{"keyword": w, "count": freq_a[w]} for w in only_a],
                            key=lambda x: -x["count"])[:10]
    only_b_ranked = sorted([{"keyword": w, "count": freq_b[w]} for w in only_b],
                            key=lambda x: -x["count"])[:10]

    all_words = set_a | set_b
    jaccard = round(len(common) / max(len(all_words), 1), 3)
    overlap_pct = round(len(common) / max(min(len(set_a), len(set_b)), 1) * 100, 1)

    return {
        "text_a_stats": {"total_words": len(words_a), "unique_keywords": len(set_a)},
        "text_b_stats": {"total_words": len(words_b), "unique_keywords": len(set_b)},
        "common_keywords": common_details,
        "unique_to_a": only_a_ranked,
        "unique_to_b": only_b_ranked,
        "similarity": {
            "jaccard_index": jaccard,
            "overlap_pct": overlap_pct,
            "common_count": len(common),
            "interpretation": "very similar" if jaccard > 0.6 else "similar" if jaccard > 0.3 else "somewhat related" if jaccard > 0.1 else "different topics",
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    mcp.run()
