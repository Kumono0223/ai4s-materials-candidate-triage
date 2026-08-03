from __future__ import annotations

import re
from collections import defaultdict
from typing import Any


ATOMIC_WEIGHTS = {
    "H": 1.008, "Li": 6.94, "B": 10.81, "C": 12.011, "N": 14.007, "O": 15.999,
    "F": 18.998, "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085,
    "P": 30.974, "S": 32.06, "Cl": 35.45, "K": 39.098, "Ca": 40.078,
    "Ti": 47.867, "V": 50.942, "Cr": 51.996, "Mn": 54.938, "Fe": 55.845,
    "Co": 58.933, "Ni": 58.693, "Cu": 63.546, "Zn": 65.38, "Ga": 69.723,
    "Ge": 72.630, "As": 74.922, "Se": 78.971, "Br": 79.904, "Rb": 85.468,
    "Sr": 87.62, "Y": 88.906, "Zr": 91.224, "Nb": 92.906, "Mo": 95.95,
    "Ag": 107.868, "In": 114.818, "Sn": 118.710, "I": 126.904, "Ba": 137.327,
    "La": 138.905, "Ce": 140.116, "W": 183.84, "Pt": 195.084, "Au": 196.967,
}
TOKEN = re.compile(r"([A-Z][a-z]?)(\d*(?:\.\d+)?)")


def parse_formula(formula: str) -> dict[str, float]:
    text = formula.strip()
    if not text:
        raise ValueError("formula cannot be empty")
    cursor = 0
    counts: dict[str, float] = defaultdict(float)
    for match in TOKEN.finditer(text):
        if match.start() != cursor:
            raise ValueError(f"unsupported formula syntax near {text[cursor:]}")
        element, amount = match.groups()
        if element not in ATOMIC_WEIGHTS:
            raise ValueError(f"unknown element: {element}")
        counts[element] += float(amount) if amount else 1.0
        cursor = match.end()
    if cursor != len(text):
        raise ValueError(f"unsupported formula syntax near {text[cursor:]}")
    return dict(counts)


def analyze_formula(formula: str) -> dict[str, Any]:
    counts = parse_formula(formula)
    molar_mass = sum(ATOMIC_WEIGHTS[element] * amount for element, amount in counts.items())
    fractions = {element: round(ATOMIC_WEIGHTS[element] * amount / molar_mass, 6) for element, amount in counts.items()}
    tags: list[str] = []
    if "O" in counts:
        tags.append("oxygen-containing")
    if any(element in counts for element in ("Fe", "Co", "Ni", "Mn", "Cu", "Cr", "Ti", "V")):
        tags.append("transition-metal-containing")
    if "Li" in counts:
        tags.append("lithium-containing")
    # Transparent prioritization only: oxygen + transition metal + lithium are common triage signals.
    score = 0.0
    score += 0.35 if "O" in counts else 0.0
    score += 0.35 if any(element in counts for element in ("Fe", "Co", "Ni", "Mn", "Cu", "Cr", "Ti", "V")) else 0.0
    score += 0.20 if "Li" in counts else 0.0
    score += min(0.10, len(counts) * 0.02)
    return {
        "formula": formula,
        "composition": counts,
        "molar_mass_g_mol": round(molar_mass, 6),
        "mass_fractions": fractions,
        "tags": tags,
        "triage_score": round(score, 4),
        "limitations": "启发式组成初筛，不是性能预测；需用公开数据、模拟或实验验证。",
    }

