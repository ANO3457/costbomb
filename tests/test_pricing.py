"""Price-table model-id resolution — real ids carry date/version suffixes."""

from __future__ import annotations

import json

import pytest

from costbomb.pricing import PriceTable, UnpricedModelError


def test_exact_match_still_wins(prices: PriceTable) -> None:
    assert prices.resolve_model_key("anthropic:claude-opus-4-8") == "anthropic:claude-opus-4-8"
    assert prices.model("anthropic:claude-opus-4-8").input_cost_per_token == 3.0e-6


def test_date_suffixed_real_ids_resolve_to_base(prices: PriceTable) -> None:
    # The exact strings a provider returns in real responses.
    assert prices.model("anthropic:claude-opus-4-8-20250514").input_cost_per_token == 3.0e-6
    assert prices.model("openai:gpt-4o-mini-2024-07-18").input_cost_per_token == 1.5e-7
    assert prices.resolve_model_key("anthropic:claude-opus-4-8-20250514") == "anthropic:claude-opus-4-8"


def test_boundary_safe_no_false_prefix_match() -> None:
    # gpt-4o must NEVER resolve to a gpt-4 entry (different model, different price).
    pt = PriceTable.from_json(json.dumps({
        "_meta": {"version": "t"},
        "models": {
            "openai:gpt-4": {"input_cost_per_token": 3.0e-5},
            "openai:gpt-4o": {"input_cost_per_token": 2.5e-6},
        },
    }))
    assert pt.resolve_model_key("openai:gpt-4o") == "openai:gpt-4o"          # exact
    assert pt.resolve_model_key("openai:gpt-4o-2024-08-06") == "openai:gpt-4o"  # suffix → gpt-4o
    assert pt.resolve_model_key("openai:gpt-4-0613") == "openai:gpt-4"       # suffix → gpt-4
    assert pt.model("openai:gpt-4o-2024-08-06").input_cost_per_token == 2.5e-6  # not 3e-5


def test_longest_prefix_wins() -> None:
    pt = PriceTable.from_json(json.dumps({
        "_meta": {"version": "t"},
        "models": {
            "anthropic:claude": {"input_cost_per_token": 1.0e-6},
            "anthropic:claude-opus-4-8": {"input_cost_per_token": 3.0e-6},
        },
    }))
    assert pt.resolve_model_key("anthropic:claude-opus-4-8-20250514") == "anthropic:claude-opus-4-8"


def test_genuinely_unknown_model_still_raises(prices: PriceTable) -> None:
    assert prices.resolve_model_key("mistral:big-9000") is None
    with pytest.raises(UnpricedModelError):
        prices.model("mistral:big-9000")  # never a silent $0
