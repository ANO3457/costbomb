# Dry-run cost estimation

Use dry-run for a reproducible smoke check of attack selection, search, reporting,
and CI budget wiring **without invoking the target handler**. Its dollar figures
are a structural heuristic, not a prediction of your next invoice.

## Try it without a model server

After installing costbomb from source:

```bash
costbomb estimate --target fake --seed 1337 --generations 10
```

`estimate` uses the same dry-run engine as `run --dry-run`. For JSON output and
a budget gate, use `run`:

```bash
costbomb run --target fake --dry-run --seed 1337 --generations 10 --findings-out dry-findings.json
costbomb run --target fake --dry-run --seed 1337 --generations 10 --budget 100
```

The threshold of 100 is an example smoke threshold, not a recommended production
budget. A deliberately impossible threshold demonstrates the failing gate:

```bash
costbomb run --target fake --dry-run --seed 1337 --generations 10 --budget 0
```

That command exits **1** with `gate failed`: a positive *estimated* worst-case
cost exceeds zero even though the fuzzer placed no paid target calls. A passing
gate exits **0**. Without `--budget` or `--fail-on-regression`, successful completion
does not mean a budget check passed.

## Read the output

The terminal subtitle says `estimated — dry run`; finding rows carry `est`.
In `dry-findings.json`:

- `estimated: true` marks the run; findings are also marked estimated.
- `own_spend_usd: 0.0` is the fuzzer's metered spend in default template-only
  dry-run, not the estimated worst-case cost.
- `baseline_usd` is the benign input's heuristic score. `worst_usd` and the
  amplification factor compare heuristic scores, not measured invoices.
- `classes_skipped` lists classes unsupported by declared target capabilities;
  dry-run does not discover additional capabilities.

Keep seed, search options, code version, and price table fixed when comparing
smoke runs. Dry-run collects no repeated real samples: `--k` does not turn its
single heuristic score into a measured p95 distribution.

## What the heuristic can tell you

The estimator counts loop/tool/spawn vocabulary in the input, approximates context
size from text length, and uses assumed context/output sizes and a blended token
rate. It never observes the target's reasoning, tools, retries, or provider usage.

`--price-table` can change that scale, but does not calibrate target behavior. The
input estimator uses its default blend-model rate when available and a nominal
fallback otherwise; it does not infer which model the target will use. Do not
interpret the breakdown as measured model, tool, downstream, or infrastructure
charges. See [meter validation](VALIDATION.md) for the separate evidence required
to substantiate billed cost.

## Boundaries of “no paid calls”

The commands above use built-in `fake` and the default template mutator; they
need no provider credentials or model server.

You can replace `fake` with `./agent.py:handler`, but target construction still
**imports that module and executes its top-level code**. Custom target
`capabilities()` methods also run. Dry-run skips target invocation; it is not an
import sandbox or a guarantee that arbitrary adapters have no initialization side
effects. Do not load an untrusted harness to “check it safely.”

Do not add `--use-llm` to a zero-model-call smoke command. LLM-assisted mutation is
independent of target evaluation and can still call the configured endpoint and
accrue its own metered cost. `estimate` has no LLM-mutation option.

`--budget` is the finding threshold; `--max-spend` caps the fuzzer's own spend.
Neither turns a heuristic into a validated upper bound on a real agent's invoice.
`costbomb baseline update` is a **real run**, not a dry-run baseline shortcut;
it does not accept `--dry-run`. Real target runs need separate authorization and
their usage/cost evidence must be validated.

A green smoke run cannot demonstrate that a real agent is cheap, that a model is
safe, or that a measured cost regression is absent.
