"""
Currency conversion service.
Uses a static fallback table; swap fetch_live_rates() for a real API call.
"""

from typing import Dict, Optional

# Approximate rates to INR (as of mid-2026 estimates — replace with live API)
STATIC_RATES_TO_INR: Dict[str, float] = {
    "INR": 1.0,
    "USD": 83.5,
    "EUR": 90.2,
    "GBP": 105.6,
    "JPY": 0.56,
    "AUD": 54.3,
    "CAD": 61.7,
    "SGD": 61.9,
    "AED": 22.7,
    "THB": 2.3,
}


def convert_to_inr(amount: float, from_currency: str) -> float:
    """Convert any amount to INR using the static rate table."""
    rate = STATIC_RATES_TO_INR.get(from_currency.upper(), 1.0)
    return round(amount * rate, 2)


def convert_from_inr(amount_inr: float, to_currency: str) -> float:
    """Convert INR to target currency."""
    rate = STATIC_RATES_TO_INR.get(to_currency.upper(), 1.0)
    return round(amount_inr / rate, 2)


def get_supported_currencies() -> list:
    return list(STATIC_RATES_TO_INR.keys())


def build_expense_summary(expenses: list, budget_inr: float) -> dict:
    """Aggregate expenses by category and compute budget tracking."""
    by_category: Dict[str, float] = {}
    currency_breakdown: Dict[str, float] = {}
    total_inr = 0.0

    for exp in expenses:
        inr = exp.amount_inr or convert_to_inr(exp.amount, exp.currency)
        total_inr += inr

        cat = exp.category or "other"
        by_category[cat] = by_category.get(cat, 0.0) + inr

        cur = exp.currency
        currency_breakdown[cur] = currency_breakdown.get(cur, 0.0) + exp.amount

    return {
        "total_inr": round(total_inr, 2),
        "budget_inr": round(budget_inr, 2),
        "remaining_inr": round(budget_inr - total_inr, 2),
        "by_category": {k: round(v, 2) for k, v in by_category.items()},
        "currency_breakdown": {k: round(v, 2) for k, v in currency_breakdown.items()},
    }
