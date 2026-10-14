# costbomb — Roadmap & status

**Status as of 2026-10-14:** costbomb-core is built, shipped (`pip install costbomb`,
v0.2.0 on PyPI), and embedded in stampede as the `adversarial:economic` cohort. The
one gap that matters is unchanged: the meter is **arithmetic-checked, not yet
validated against a real invoice** (`0/20`). Legend: ✅ done · 🚧 partial · ⬜ not started.

## v0.1 — inside stampede (Launch 1) ✅
- ✅ Attack library + cost meter embedded as stampede's `adversarial:economic` cohort.
- ✅ Goal injection — the cohort pursues costbomb's cost-explosion playbook.
- ✅ Economic findings in the Agent Readiness Report via the shared `RunReport` contract.
- ✅ costbomb's meter runs on stampede's real traces; dedicated high-budget `economic` persona.
- *(stampede PRs #25, #26, #28, #29 — all merged. `pip install stampede[economic]`.)*

## v0.2 — standalone extract (Launch 2) 🚧
- ✅ CLI, evolutionary fuzz engine, CI gate (baseline + price-drift separation).
- ✅ Ten attack classes (the five SPEC + five ⊕ 2026 classes).
- ✅ Repro reports; `findings.json` + OTel GenAI-profile export.
- ✅ **Released v0.2.0 to PyPI** (Trusted Publishing).
- ⬜ The *loud* launch — demo GIF, "denial-of-wallet" essay, Show HN. **Gated on validation.**

## v0.3 — policy + ecosystem 🚧
- ✅ Integration with **exactly-once** — duplicate side-effect cross-check (`costbomb[exactly-once]`).
- ⬜ Spend-ceiling policy + runtime enforcer-config emit.
- 🚧 Custom attack authoring — registry is pluggable; external-loading UX + docs pending.
- ⬜ agent-postmortems incident-as-seed; provider what-if re-pricing UX (`reprice()` exists).

## ⊕ Built beyond the original spec ✅
- ✅ **Proxy meter** — zero-instrumentation metering via a `base_url` swap.
- ✅ LLM-assisted mutator (cost-capped, local-default); MockworldTarget (safe default).
- ✅ **Richer cost model** — downstream tool-cost / blast radius, wall-clock / infra cost,
  duplicate-effect costing (all searchable via `--fitness`).
- ✅ Model-id resolution (date/version-suffixed real ids → base prices).
- ✅ Per-biller **validation harnesses** — full-agent LLM slice + Stripe test-mode slice;
  meter-accuracy corpus scaffold.

---

## What remains (backlog, most-important first)

1. **Validate the meter against real invoices** — `0/20` invoice-grounded fixtures. THE
   credibility gate; the only item blocked on external credentials (an API key + a few
   cents, and/or Stripe test keys). Harnesses are built and one-command. See
   [`docs/VALIDATION.md`](./docs/VALIDATION.md).
2. **Launch 2 (loud)** — PyPI ✅; remaining: demo GIF, essay, Show HN. Deliberately rests
   on (1) so the meter is proven before it's marketed.
3. **v0.3 features** — spend-ceiling policy + enforcer-config; custom-authoring UX;
   postmortem incident-as-seed; what-if re-pricing UX.
4. **Robustness** — stream-response metering in the proxy (currently forwarded
   un-metered); broader default price-table coverage.
