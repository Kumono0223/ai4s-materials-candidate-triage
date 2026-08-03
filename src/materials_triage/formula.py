"""Deterministic composition descriptors and transparent triage profiles.

The module deliberately stops at composition-level evidence.  Scores are
prioritisation aids, not predictions of electrochemical or catalytic
performance.
"""

from __future__ import annotations

import math
import re
from collections import defaultdict
from typing import Any, Iterable


METHODOLOGY_VERSION = "2026.08-composition-v2"
ATOMIC_WEIGHT_SOURCE = "CIAAW standard atomic weights (embedded rounded table; accessed 2026-08-03)"
ATOMIC_WEIGHTS = {
    "H": 1.008, "Li": 6.94, "Be": 9.0122, "B": 10.81, "C": 12.011,
    "N": 14.007, "O": 15.999, "F": 18.998, "Na": 22.990, "Mg": 24.305,
    "Al": 26.982, "Si": 28.085, "P": 30.974, "S": 32.06, "Cl": 35.45,
    "K": 39.098, "Ca": 40.078, "Sc": 44.956, "Ti": 47.867, "V": 50.942,
    "Cr": 51.996, "Mn": 54.938, "Fe": 55.845, "Co": 58.933, "Ni": 58.693,
    "Cu": 63.546, "Zn": 65.38, "Ga": 69.723, "Ge": 72.630, "As": 74.922,
    "Se": 78.971, "Br": 79.904, "Rb": 85.468, "Sr": 87.62, "Y": 88.906,
    "Zr": 91.224, "Nb": 92.906, "Mo": 95.95, "Ru": 101.07, "Rh": 102.906,
    "Pd": 106.42, "Ag": 107.868, "Cd": 112.414, "In": 114.818,
    "Sn": 118.710, "Sb": 121.760, "Te": 127.60, "I": 126.904,
    "Cs": 132.905, "Ba": 137.327, "La": 138.905, "Ce": 140.116,
    "Pr": 140.908, "Nd": 144.242, "Sm": 150.36, "Eu": 151.964,
    "Gd": 157.25, "Tb": 158.925, "Dy": 162.500, "Ho": 164.930,
    "Er": 167.259, "Tm": 168.934, "Yb": 173.045, "Lu": 174.967,
    "Hf": 178.49, "Ta": 180.948, "W": 183.84, "Re": 186.207,
    "Os": 190.23, "Ir": 192.217, "Pt": 195.084, "Au": 196.967,
    "Hg": 200.592, "Tl": 204.38, "Pb": 207.2, "Bi": 208.980,
    "Th": 232.038, "U": 238.029,
}

TOKEN = re.compile(r"([A-Z][a-z]?|\d+(?:\.\d+)?|\.\d+|[()\[\]])")
TRANSITION_METALS = {
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Y", "Zr",
    "Nb", "Mo", "Ru", "Rh", "Pd", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt",
}
ALKALI_CARRIERS = {"Li", "Na", "K"}
ANION_FRAMEWORK = {"O", "F", "P", "S", "N"}
# A review watchlist, not a claim that every use is unsustainable.  It is
# intentionally explicit so a downstream user can replace it with a regional
# or organisation-specific critical-materials policy.
SUPPLY_RISK_WATCHLIST = {
    "Li", "Co", "Ni", "Ga", "Ge", "Y", "La", "Ce", "Pr", "Nd", "Sm",
    "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Pt", "Pd", "Rh", "Ir",
}
SAFETY_REVIEW = {"Be", "As", "Cd", "Hg", "Tl", "Pb", "Th", "U"}
OBJECTIVES = ("battery", "catalysis", "low-supply-risk")


def _is_number(token: str) -> bool:
    try:
        float(token)
        return True
    except ValueError:
        return False


def _tokenize(text: str) -> list[str]:
    tokens = TOKEN.findall(text)
    if "".join(tokens) != text:
        cursor = 0
        for match in TOKEN.finditer(text):
            if match.start() != cursor:
                break
            cursor = match.end()
        raise ValueError(f"unsupported formula syntax near {text[cursor:]}")
    return tokens


def _parse_sequence(tokens: list[str], position: int = 0, closing: str | None = None) -> tuple[dict[str, float], int]:
    counts: dict[str, float] = defaultdict(float)
    pairs = {"(": ")", "[": "]"}
    while position < len(tokens):
        token = tokens[position]
        if closing and token == closing:
            return dict(counts), position + 1
        if token in (")", "]"):
            raise ValueError(f"unexpected closing bracket: {token}")
        if token in pairs:
            nested, position = _parse_sequence(tokens, position + 1, pairs[token])
            multiplier = 1.0
            if position < len(tokens) and _is_number(tokens[position]):
                multiplier = float(tokens[position])
                position += 1
            if multiplier <= 0:
                raise ValueError("stoichiometric amounts must be positive")
            for element, amount in nested.items():
                counts[element] += amount * multiplier
            continue
        if not token[0].isupper():
            raise ValueError(f"expected an element near {token}")
        if token not in ATOMIC_WEIGHTS:
            raise ValueError(f"unknown element: {token}")
        position += 1
        amount = 1.0
        if position < len(tokens) and _is_number(tokens[position]):
            amount = float(tokens[position])
            position += 1
        if amount <= 0:
            raise ValueError("stoichiometric amounts must be positive")
        counts[token] += amount
    if closing:
        raise ValueError(f"missing closing bracket: {closing}")
    return dict(counts), position


def parse_formula(formula: str) -> dict[str, float]:
    """Parse elements, decimals, nested ()/[] groups and middle-dot hydrates."""

    text = re.sub(r"\s+", "", formula)
    if not text:
        raise ValueError("formula cannot be empty")
    totals: dict[str, float] = defaultdict(float)
    for raw_segment in text.split("·"):
        if not raw_segment:
            raise ValueError("hydrate segment cannot be empty")
        coefficient = 1.0
        match = re.match(r"^(\d+(?:\.\d+)?)(?=[A-Z\[(])", raw_segment)
        if match:
            coefficient = float(match.group(1))
            raw_segment = raw_segment[match.end():]
        parsed, position = _parse_sequence(_tokenize(raw_segment))
        if position == 0 or not parsed:
            raise ValueError("formula segment cannot be empty")
        for element, amount in parsed.items():
            totals[element] += coefficient * amount
    return dict(totals)


def _format_amount(value: float) -> str:
    if math.isclose(value, 1.0):
        return ""
    if math.isclose(value, round(value)):
        return str(int(round(value)))
    return f"{value:.6g}"


def canonical_formula(composition: dict[str, float]) -> str:
    """Return a deterministic Hill-style formula without changing ratios."""

    elements = list(composition)
    if "C" in composition:
        order = ["C"] + (["H"] if "H" in composition else []) + sorted(e for e in elements if e not in {"C", "H"})
    else:
        order = sorted(elements)
    return "".join(f"{element}{_format_amount(composition[element])}" for element in order)


def _fractions(counts: dict[str, float]) -> tuple[dict[str, float], dict[str, float], float]:
    atom_total = sum(counts.values())
    molar_mass = sum(ATOMIC_WEIGHTS[element] * amount for element, amount in counts.items())
    atomic = {element: amount / atom_total for element, amount in counts.items()}
    mass = {element: ATOMIC_WEIGHTS[element] * amount / molar_mass for element, amount in counts.items()}
    return atomic, mass, molar_mass


def _bounded_fraction(atomic: dict[str, float], elements: set[str], target: float) -> float:
    return min(1.0, sum(atomic.get(element, 0.0) for element in elements) / target)


def _score_profile(objective: str, atomic: dict[str, float], distinct: int, entropy: float) -> tuple[float, list[dict[str, Any]]]:
    watchlist_fraction = sum(atomic.get(element, 0.0) for element in SUPPLY_RISK_WATCHLIST)
    safety_elements = sorted(set(atomic) & SAFETY_REVIEW)
    mean_atomic_mass = sum(atomic[element] * ATOMIC_WEIGHTS[element] for element in atomic)
    diversity = min(1.0, max(0.0, (distinct - 1) / 4))
    components: list[tuple[str, float, str]]
    if objective == "battery":
        components = [
            ("alkali-carrier", 0.30 * _bounded_fraction(atomic, ALKALI_CARRIERS, 0.20), "Li/Na/K atomic fraction; carrier presence only"),
            ("redox-metal", 0.25 * _bounded_fraction(atomic, TRANSITION_METALS, 0.20), "transition-metal atomic fraction; oxidation state not inferred"),
            ("anion-framework", 0.20 * _bounded_fraction(atomic, ANION_FRAMEWORK, 0.55), "O/F/P/S/N framework fraction"),
            ("mixing-entropy", 0.15 * entropy, "normalised ideal configurational entropy proxy"),
            ("composition-diversity", 0.10 * diversity, "distinct-element diversity, saturated at five elements"),
        ]
    elif objective == "catalysis":
        components = [
            ("transition-metal", 0.35 * _bounded_fraction(atomic, TRANSITION_METALS, 0.20), "transition-metal atomic fraction; no surface state assumed"),
            ("heteroatom-framework", 0.20 * _bounded_fraction(atomic, {"O", "N", "S", "P"}, 0.55), "O/N/S/P atomic fraction"),
            ("mixing-entropy", 0.20 * entropy, "normalised ideal configurational entropy proxy"),
            ("composition-diversity", 0.15 * diversity, "distinct-element diversity, saturated at five elements"),
            ("mass-efficiency-proxy", 0.10 * (1 - min(1.0, mean_atomic_mass / 200)), "lower mean atomic mass receives a small transparent bonus"),
        ]
    elif objective == "low-supply-risk":
        components = [
            ("watchlist-avoidance", 0.45 * (1 - watchlist_fraction), "fraction outside the replaceable supply-risk watchlist"),
            ("safety-review-avoidance", 0.25 if not safety_elements else 0.0, "no configured safety-review elements"),
            ("mass-efficiency-proxy", 0.15 * (1 - min(1.0, mean_atomic_mass / 200)), "lower mean atomic mass proxy"),
            ("composition-simplicity", 0.15 * (1 - min(1.0, max(0, distinct - 2) / 5)), "fewer distinct elements receive a processing-simplicity proxy"),
        ]
    else:
        raise ValueError(f"unknown objective: {objective}; choose one of {', '.join(OBJECTIVES)}")
    breakdown = [{"component": name, "contribution": round(value, 6), "rationale": rationale} for name, value, rationale in components]
    raw_score = sum(value for _, value, _ in components)
    if objective != "low-supply-risk":
        supply_penalty = -0.12 * watchlist_fraction
        breakdown.append({"component": "supply-watchlist-penalty", "contribution": round(supply_penalty, 6), "rationale": "transparent review penalty; watchlist is replaceable"})
        raw_score += supply_penalty
        if safety_elements:
            breakdown.append({"component": "safety-review-penalty", "contribution": -0.25, "rationale": f"configured review elements present: {', '.join(safety_elements)}"})
            raw_score -= 0.25
    return max(0.0, min(1.0, raw_score)), breakdown


def analyze_formula(formula: str, objective: str = "battery") -> dict[str, Any]:
    counts = parse_formula(formula)
    atomic, mass, molar_mass = _fractions(counts)
    entropy_raw = -sum(value * math.log(value) for value in atomic.values())
    entropy_normalised = entropy_raw / math.log(len(atomic)) if len(atomic) > 1 else 0.0
    score, breakdown = _score_profile(objective, atomic, len(atomic), entropy_normalised)
    watchlist = sorted(set(counts) & SUPPLY_RISK_WATCHLIST)
    safety = sorted(set(counts) & SAFETY_REVIEW)
    flags: list[str] = []
    if set(counts) & TRANSITION_METALS:
        flags.append("transition-metal-containing")
    if set(counts) & ALKALI_CARRIERS:
        flags.append("alkali-carrier-containing")
    if watchlist:
        flags.append("supply-watchlist-review")
    if safety:
        flags.append("safety-review-required")
    band = "A" if score >= 0.65 else "B" if score >= 0.45 else "C"
    return {
        "formula": formula,
        "canonical_formula": canonical_formula(counts),
        "composition": counts,
        "molar_mass_g_mol": round(molar_mass, 6),
        "atomic_fractions": {element: round(value, 6) for element, value in atomic.items()},
        "mass_fractions": {element: round(value, 6) for element, value in mass.items()},
        "descriptors": {
            "distinct_elements": len(counts),
            "total_atoms_per_formula_unit": round(sum(counts.values()), 6),
            "normalised_mixing_entropy": round(entropy_normalised, 6),
            "mean_atomic_mass": round(sum(atomic[element] * ATOMIC_WEIGHTS[element] for element in atomic), 6),
            "oxygen_atomic_fraction": round(atomic.get("O", 0.0), 6),
            "transition_metal_atomic_fraction": round(sum(atomic.get(element, 0.0) for element in TRANSITION_METALS), 6),
            "supply_watchlist_atomic_fraction": round(sum(atomic.get(element, 0.0) for element in SUPPLY_RISK_WATCHLIST), 6),
        },
        "objective": objective,
        "triage_score": round(score, 6),
        "priority_band": band,
        "score_breakdown": breakdown,
        "flags": flags,
        "supply_watchlist_elements": watchlist,
        "safety_review_elements": safety,
        "validation_level": "composition-only",
        "methodology_version": METHODOLOGY_VERSION,
        "atomic_weight_source": ATOMIC_WEIGHT_SOURCE,
        "limitations": [
            "组成层启发式初筛，不是性能、稳定性、毒性或可合成性预测。",
            "未使用晶体结构、氧化态、相图、工艺、成本或实验条件。",
            "高优先级候选仍必须用授权数据库、模拟和实验验证。",
        ],
    }


def rank_candidates(formulas: Iterable[str], objective: str = "battery") -> dict[str, Any]:
    candidates = sorted(
        (analyze_formula(formula, objective=objective) for formula in formulas),
        key=lambda item: (-item["triage_score"], item["canonical_formula"]),
    )
    return {
        "methodology_version": METHODOLOGY_VERSION,
        "objective": objective,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "next_validation": [
            "记录候选来源、公开数据版本和许可。",
            "按目标属性运行结构/第一性原理/机器学习基线，并保留误差与失败样本。",
            "由领域专家审阅供应风险与安全标志，再决定实验优先级。",
        ],
    }
