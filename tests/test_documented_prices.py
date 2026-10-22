"""Keep the price-table guide's arithmetic executable (REQ-CM-3/8, UT-CM-1/2)."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from costbomb.cli import app
from costbomb.meter import CostMeter
from costbomb.pricing import PriceTable
from costbomb.tracebuild import TraceBuilder

EXAMPLE = Path(__file__).parents[1] / "examples" / "prices_documented.json"


def test_documented_table_prices_all_sources() -> None:
    prices = PriceTable.from_path(EXAMPLE)
    tb = TraceBuilder(1)
    root = tb.root()
    tb.chat(root, model="example:demo-model", provider="example", input_tokens=1000,
            output_tokens=500, reasoning_tokens=200, cache_read_tokens=300,
            cache_write_tokens=400)
    for _ in range(3):
        tb.tool(root, tool_name="example_tool")
    bill = CostMeter(prices).cost(tb.build(duration_s=2))
    assert bill.model_usd == pytest.approx(0.00795)
    assert bill.tool_usd == pytest.approx(0.03)
    assert bill.infra_usd == pytest.approx(0.004)
    assert bill.total_usd == pytest.approx(0.04195)
    assert bill.downstream_usd == pytest.approx(0.75)
    assert bill.blast_radius_usd == pytest.approx(0.79195)


def test_documented_inspection_command() -> None:
    result = CliRunner().invoke(app, ["price", "--price-table", str(EXAMPLE)])
    assert result.exit_code == 0, result.output
    assert "documentation-example-v1" in result.output
    assert "example:demo-model" in result.output
    assert "example_tool" in result.output
