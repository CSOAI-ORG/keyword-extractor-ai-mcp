# Keyword Extractor AI

> By [MEOK AI Labs](https://meok.ai) — Extract keywords and key phrases from text using TF-IDF and statistical methods

## Installation

```bash
pip install keyword-extractor-ai-mcp
```

## Usage

```bash
python server.py
```

## Tools

### `extract_keywords`
Extract top keywords using TF-IDF scoring.

**Parameters:**
- `text` (str): Text to extract keywords from
- `max_keywords` (int): Maximum number of keywords (default: 10)

### `extract_phrases`
Extract key phrases (2-3 word combinations).

**Parameters:**
- `text` (str): Text to extract phrases from
- `max_phrases` (int): Maximum number of phrases (default: 5)

### `topic_classification`
Classify text into topic categories.

**Parameters:**
- `text` (str): Text to classify

### `keyword_density`
Calculate keyword density for SEO analysis.

**Parameters:**
- `text` (str): Text to analyze

## Authentication

Free tier: 30 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
