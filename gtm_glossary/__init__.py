"""Offline lookup of the OneGTMLab GTM glossary (110 terms)."""
import json, os

__version__ = "0.1.0"
_PATH = os.path.join(os.path.dirname(__file__), "glossary.json")


def load():
    with open(_PATH, encoding="utf-8") as f:
        return json.load(f)


def lookup(term, terms=None):
    """Return the entry whose id or name matches `term` (case-insensitive), or None."""
    terms = terms or load()
    key = term.strip().lower().replace(" ", "-")
    for t in terms:
        if t["id"] == key or t["term"].lower() == term.strip().lower():
            return t
    return None


def search(query, terms=None):
    """Entries whose term or definition contains every word of `query`, term matches first."""
    terms = terms or load()
    words = [w for w in query.lower().split() if w]
    hits = []
    for t in terms:
        name, text = t["term"].lower(), t["definition"].lower()
        if all(w in name or w in text for w in words):
            hits.append((0 if all(w in name for w in words) else 1, t["term"].lower(), t))
    return [h[2] for h in sorted(hits, key=lambda h: (h[0], h[1]))]


def to_markdown(terms=None):
    terms = terms or load()
    lines = ["# GTM glossary", ""]
    for t in terms:
        lines.append("- [%s](%s): %s" % (t["term"], t["url"], t["definition"]))
    return "\n".join(lines) + "\n"
