from __future__ import annotations
from typing import List, Tuple
import re
from .registry import get_registry, EngineEntry

WORD_RE = re.compile(r"\w+", re.UNICODE)

def _normalize(text: str) -> List[str]:
    return [w.lower() for w in WORD_RE.findall(text or "")]

def _score(text: str, entry: EngineEntry) -> int:
    tokens = set(_normalize(text))
    score = 0
    for kw in entry.keywords:
        parts = _normalize(kw)
        if all(p in tokens for p in parts):
            score += 3 if len(parts) > 1 else 1
    return score

def select_engines(texto: str, top_k: int = 1) -> List[Tuple[str, int]]:
    registry = get_registry()
    scored = []
    for engine_id, entry in registry.items():
        s = _score(texto or "", entry)
        scored.append((engine_id, s))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:max(1, top_k)]
