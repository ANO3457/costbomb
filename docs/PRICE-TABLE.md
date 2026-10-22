# Provider price-table format

The meter reads JSON through `PriceTable.from_path()`; no provider SDK or model
call is needed to load or inspect a table (REQ-CM-3, NFR-3).

Start with [`examples/prices_documented.json`](../examples/prices_documented.json).
Its prices are **invented arithmetic examples, not current provider quotes**.
Replace them with your own verified rates before measuring a real target.

```sh
costbomb price --price-table examples/prices_documented.json
```

`price` prints the version, source, and known model/tool names; it does not run a
target. To use a table for measurement, pass `--price-table FILE.json` to `run`,
`replay`, or `proxy` as appropriate. A supplied file **replaces** the vendored
table rather than merging with it. Include every model your target can use.

## Fields and units

| JSON field | Meaning |
| --- | --- |
| `_meta.version` | Your revision label, retained with the loaded table; default `unknown`. |
| `_meta.source` | Where you obtained the rates; default `unknown`. Other metadata is not used in pricing. |
| `models` | Object keyed by model ID, normally `provider:model` as recorded in traces. |
| `tools` | Object keyed by the tool name recorded in traces. |
| `infra.usd_per_second` | Optional USD per second of measured run duration; default zero. |

Each model entry supports five independent **USD per token** fields:

- `input_cost_per_token`
- `output_cost_per_token`
- `reasoning_cost_per_token`
- `cache_read_cost_per_token`
- `cache_write_cost_per_token`

For a quote of USD 2 per million input tokens, enter `0.000002`, not `2`.
Omitted token classes default to zero; they do **not** inherit input/output rates.
Supply reasoning and cache rates explicitly when your provider charges for them.
The table does not deduplicate usage counters: the trace must use appropriate,
non-overlapping token classes for that provider.

Each tool entry supports `price_per_call` (direct USD fee per invocation),
`downstream_usd` (consequence value per invocation, separately included in blast
radius), and `side_effecting` (boolean used by duplicate-effect detection).
Missing prices default to zero and `side_effecting` defaults to false.

## Lookup and error boundaries

Model lookup prefers an exact key, then the longest key followed by a `-` boundary
(for example, `example:demo-model-20261022` resolves to `example:demo-model`).
If no key matches, metering raises `UnpricedModelError`; unknown models are not
silently free. Unknown tools have a zero fee and are listed as unpriced tools in
the cost breakdown. A missing infra rate disables duration pricing.

Invalid JSON raises a JSON parse error. This is not a strict schema validator:
unknown fields can be ignored, and loading does not guarantee that a supplied
rate is non-negative or finite. Check field names and rates yourself. Loading a
file successfully does not prove that it matches an invoice.

## Worked example (no paid calls)

For the example table, a scripted trace with 1,000 input, 500 output, 200 reasoning,
300 cache-read, and 400 cache-write tokens costs USD **0.00795** in model usage.
Three `example_tool` calls add USD **0.03** in direct fees, and two seconds of
duration add USD **0.004**, for a direct total of USD **0.04195**. The tools'
USD **0.75** consequence value is separate: blast radius is USD **0.79195**.

`tests/test_documented_prices.py` executes this calculation with `TraceBuilder`
and `CostMeter`, plus the inspection CLI command. It is an arithmetic fixture,
not provider billing validation. See [VALIDATION.md](VALIDATION.md) for the
invoice-grounding gap and validation workflow.
