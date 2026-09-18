# hn-wasm3-status-embedding-boundary-lab

Audit for **HN 49590611 — “It took a year to ship WebAssembly in Anubis.”**

Tests the release-manager claim:

> “Wasm 3.0 is a W3C standard now, so a browser that supports WebAssembly supports the 3.0 feature set and its streaming APIs.”

**Verdict: the claim conflates four independent layers.** Core version ≠ W3C Recommendation status ≠ JS API ≠ Web API ≠ engine feature support. A version number does not prove a publication status; a publication status does not prove an implementation; baseline Wasm does not prove newer Core features; Core features do not prove embedding APIs; JS and Web streaming APIs are separate again.

## Boundary under test

| Layer | What it actually establishes |
|---|---|
| **Core version** | `1.0` / `2.0` / `3.0` of the Core WebAssembly specification as named in the spec abstract |
| **W3C publication status** | `W3C Recommendation` vs `Candidate Recommendation Draft` (CRD) — disjoint normative statuses |
| **Core semantics** | Module semantics independent of a concrete embedding (import/export/memory/table boundaries) |
| **JavaScript API** | `WebAssembly.*` JS Interface (`WebAssembly.Module`, `Instance`, `compile`, `instantiate`, …) — separate TR |
| **Web API** | Browser Web embedding (`compileStreaming` / `instantiateStreaming` and related fetch integration) — separate TR |
| **Implementation support** | Whether a given engine/browser actually implements baseline, a modeled newer feature, JS API, or Web streaming |

Rule: **version ≠ Recommendation ≠ Core semantics ≠ JS API ≠ Web API ≠ implemented.**

## What the primary sources actually say (verified 2026-09-18)

- **Core 1.0 — W3C Recommendation:** `https://www.w3.org/TR/wasm-core-1/` serves `W3C Recommendation, 5 December 2019` (`<meta name="w3c-status" content="REC">`). This is the published standard.
- **Core 2.0 / current Core 3.0 — Candidate Recommendation Draft:** `https://www.w3.org/TR/wasm-core-2/` (also served at `https://www.w3.org/TR/wasm-core/` latest) shows `W3C Candidate Recommendation Draft, 11 September 2026` (`<meta name="w3c-status" content="CRD">`). The abstract reads *“This document describes release 3.0 of the core WebAssembly standard”* — that names the **Core version** while the status region declares it a **CRD, not a W3C Recommendation**. The two facts are independent.
- **JavaScript Interface — separate CRD:** `https://www.w3.org/TR/wasm-js-api/` (canonical `https://www.w3.org/TR/wasm-js-api-2/`) is `W3C Candidate Recommendation Draft` (`<meta name="w3c-status" content="CRD">`, Bikeshed 2026-08-21). Defines the JS embedding independent of Core semantics.
- **Web API — separate CRD:** `https://www.w3.org/TR/wasm-web-api/` (canonical `https://www.w3.org/TR/wasm-web-api-2/`) is `W3C Candidate Recommendation Draft` (`<meta name="w3c-status" content="CRD">`, Bikeshed 2026-08-21). Defines browser-specific `compileStreaming`/`instantiateStreaming` and related fetch integration — distinct from the JS Interface.
- **WebAssembly.org — community/spec hub:** `https://webassembly.org/` describes Wasm as a portable code format and points to the W3C Community Group + Working Group as the standards venues. No download-time or performance claims are made; the site links to MDN for developer documentation. Feature implementation status is documented separately at `https://webassembly.org/features/`.

### Evidence classes (kept separate)

| Evidence class | Example source | What it proves |
|---|---|---|
| **W3C normative publication status** | TR status region (`CRD` vs `REC`), `w3c-status` meta | Whether a document is a Recommendation or a draft |
| **Core semantics** | Core spec abstract + bodies-of-text defining module/instruction semantics | What the Core version names, independent of embeddings |
| **Embedding APIs** | wasm-js-api and wasm-web-api TRs (each CRD) | What JS and Web embeddings define, separate layers from Core |
| **Implementation support** | Engine/browser capability (synthetic in this lab) | What an implementation actually implements |
| **HN opinion** | Comments on 49590611 (see below) | Compatibility pain, fallback choices, perceived usefulness — not normative |

No performance numbers are claimed; this lab performs no benchmarking, no Wasm execution, and no browser automation.

## HN 49590611 audit — claims checked (comments actually retrieved)

Quoted text is abbreviated; IDs and authors are exact so you can re-fetch `https://hacker-news.firebaseio.com/v0/item/<id>.json`. The thread contains extensive compatibility/fallback discussion but **no comment asserting a W3C-standards-specific status**; the “standards-specific” row is therefore marked as not present rather than invented.

| # | Proposition seen on thread | Source | Assessment | Evidence class |
|---|---|---|---|---|
| 1 | Firefox configured with WebAssembly disabled by policy; asks for a visible “This captcha requires WebAssembly” message and notes smaller platforms/browsers may not offer a Wasm engine at all | **doctor_radium · 49593106** | **Browser compatibility / Wasm-disabled engines.** An engine may lack Wasm entirely or have it disabled. Supports the “Core module support with JS embedding unavailable” boundary: owning a Wasm engine is not uniform. Fixture `core_without_js_embedding` tests this. | HN opinion + implementation support |
| 2 | “Is there a place where I can try out if my browser is compatible?” — notes `wasm-feature-detect` shows missing 3 features, asks whether Anubis will fall back to a pure-JS solution, and notes Wasm is “ridiculously performant” vs wasm2js | **Aachen · 49591443** | **Browser compatibility + fallback + perceived performance.** Passages rate-of-adoption are uneven; a fallback (`wasm2js`) exists and is slower. Supports “baseline vs newer feature” and “JS vs generic” separations; performance remark is anecdotal, not benchmark data (no benchmark claimed here). | HN opinion + implementation support |
| 3 | “Hats off for targeting Chrome 66” — notes backwards-compatibility pain and testing on a 2014 Yosemite Mac; suggests period-correct toolchains | **kccqzy · 49591573** | **Deployment complexity / compatibility.** Older browsers remain in the wild; supporting them constrains which Wasm features can be assumed present. Baseline support does not guarantee newer Core features. | HN opinion |
| 4 | “You can use Rust’s `wasm32v1-none` target to get baseline WASM with no extra target features (restricts to `#[no_std]`).” | **Georgelemental · 49593021** | **Feature availability — baseline vs extended.** Toolchains explicitly distinguish baseline (MVP) from post-MVP extensions. Supports the invariant that generic “Wasm support” does not imply every newer Core feature. | HN opinion + implementation support |
| 5 | “something I was doing with my ‘strict MVP’ build wasn’t in fact sticking to just MVP … `wasm32-unknown-unknown` had extra non-mvp features added later — a breaking change on stable” | **adrian17 · 49595614** | **Feature availability footgun.** Even a nominally “MVP” build can silently depend on newer features; engine support is not uniform and must be tested per-feature, not per-label. | HN opinion + implementation support |
| 6 | “I assume previous challenges will still be available when WASM is not available … or as a fallback. … ‘smart’ TVs … run browsers old enough to not know what WASM is.” Asks whether scraper can force fallback. | **dspillett · 49593048** | **Fallback / deployment complexity.** Anubis anticipates missing Wasm and keeps a non-Wasm path. Supports “Core module support with JS embedding unavailable” and “JS API available while Web streaming unavailable” — layers degrade independently. | HN opinion + implementation support |

*If a comment you need is missing, fetch it directly — these are not invented. Example: `python3 -c "import urllib.request,json;print(json.load(urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/item/49593106.json')))"`*

**What the thread does not contain:** no comment was found that asserts “Wasm 3.0 is/is-not a W3C Recommendation” or otherwise makes a normative publication-status claim. The W3C-status rows in fixtures are therefore derived from the primary W3C publications above, not from an HN standards debate.

## Lab design

Pure **Python stdlib + shell**, no Wasm engines, no browser automation, no JS runtimes, no downloaded modules, no throughput tests, no external packages, no performance measurement. Every situation is a synthetic JSON record; the evaluator answers a *classification question* (“what does this evidence actually establish on each axis?”), not “will this browser run this build?”

### Fixtures (`fixtures/cases.json`)

10 synthetic cases — each carries the facts the classifier must interpret:

| id | Tests |
|---|---|
| `wasm1_recommendation` | Wasm 1.0 Recommendation (2019-12-05) — `publication_status=W3C Recommendation` |
| `wasm3_core_crd_current` | Wasm 3.0 Candidate Recommendation Draft (2026-09-11 CRD) — version 3.0 does NOT imply Recommendation |
| `baseline_without_newer_feature` | Baseline Core supported, modeled newer feature (gc-feature) false — baseline ≠ newer feature |
| `core_feature_without_web_api` | Newer Core feature true, Web API streaming false — Core ≠ Web API |
| `core_without_js_embedding` | Core feature true, JS API unavailable — Core independent of embedding |
| `js_available_streaming_unavailable` | JS API true, Web streaming false — JS API ≠ Web API |
| `streaming_distinct_from_generic` | Generic Wasm true, streaming false — streaming kept distinct from generic (duplicate emphasis) |
| `generic_wasm_without_streaming` | Generic Wasm true, streaming false (2.0 CRD) — same emphasis at another version |
| `impl_support_mistaken_for_w3c_status` | Engine supports feature; publication status stays CRD — implementation support not normative status |
| `wasm3_version_without_rec_status` | Wasm 3.0 CRD standalone — version-without-status rule (null layer values) |

### Evaluator (`evaluator.py`)

`python3 evaluator.py` reads `fixtures/cases.json`, derives the six output axes per case:

```
core_version             1.0 | 2.0 | 3.0 | …
publication_status       W3C Recommendation | Candidate Recommendation Draft | …
core_feature_supported   True | False | None (null when no modeled feature)
js_api_supported         True | False | None
web_api_supported        {generic, streaming, streaming_distinct_from_generic} | None
implementation_evidence  {generic_wasm_supported, baseline_core_supported,
                          modeled_core_feature, modeled_core_feature_supported,
                          js_api_supported, web_api_streaming_supported,
                          claim_used_as_w3c_status_evidence, is_w3c_status_evidence, note}
+ core_embedding_separation_note (invariant)
```

No `overall_compliant` / `browser_supports_wasm3` / `wasm3_compliant` field is emitted. Exit 0; writes `results.json` + `RESULTS.md`.

### Tests (`tests/test_wasm3_boundary.py`)

Independent oracle — re-derives expected classifications from raw `spec`/`engine`/`js_api`/`web_api` facts without calling the evaluator's decision branches. Catches:

- treating CRD (with `core_version=3.0`) as W3C Recommendation
- treating `core_version=3.0` as proof of Recommendation status
- treating generic/baseline Wasm support as proof of a newer Core feature
- treating Core feature support as proof of Web API streaming
- treating JS API availability as proof of Web streaming
- conflating generic Wasm with streaming Web API
- treating implementation/browser support as normative W3C-status evidence
- emitting an overall “Wasm 3.0 compliant browser” verdict

```
python3 -m unittest tests/test_wasm3_boundary.py -v
```

### Verification

```sh
./verify.sh            # local deterministic evaluator/test check
cat RESULTS.md         # recorded actual output
cat VERIFY.md          # public HTTPS fresh-clone transcript (see VERIFY.md procedure)
```

## Quick start

```sh
git clone https://github.com/necat101/hn-wasm3-status-embedding-boundary-lab.git
cd hn-wasm3-status-embedding-boundary-lab
python3 evaluator.py
python3 -m unittest tests/test_wasm3_boundary.py -v
./verify.sh
```

## Sources inspected 2026-09-18

- HN item `49590611` + sampled comments above via `hacker-news.firebaseio.com/v0/item/<id>.json` (36 top-level kids; 199 descendants; sampled within them the 6 quoted above and additional candidates 49591573/49593021/49595614/49593048)
- `https://www.w3.org/TR/wasm-core-1/` — headers `REC`, `W3C Recommendation, 5 December 2019`
- `https://www.w3.org/TR/wasm-core-2/` and `https://www.w3.org/TR/wasm-core/` — headers `CRD`, `W3C Candidate Recommendation Draft, 11 September 2026` (abstract names release 3.0; status remains CRD)
- `https://www.w3.org/TR/wasm-js-api/` / `https://www.w3.org/TR/wasm-js-api-2/` — headers `CRD` (WebAssembly JavaScript Interface)
- `https://www.w3.org/TR/wasm-web-api/` / `https://www.w3.org/TR/wasm-web-api-2/` — headers `CRD` (WebAssembly Web API, streaming)
- `https://webassembly.org/` + `https://webassembly.org/features/` — community/spec hub and feature-support reference
- No Wasm execution, browser automation, or performance measurement was performed; all evidence is synthetic and deterministic (no external packages).

## Result snapshot (actual, 2026-09-18)

Fixture classifications (evaluator `results.json` / `RESULTS.md`):

```
10 cases · 14 tests OK — python3 -m unittest tests/test_wasm3_boundary.py -v
No overall_compliant / browser_supports_wasm3 field emitted (intentionally withheld).
```

Status conclusions (unchanged):

```
Wasm 1.0:             W3C Recommendation (2019-12-05).
Wasm 3.0 (current):   Candidate Recommendation Draft (2026-09-11) — version 3.0 without implying Recommendation.
Core version:         names the Core iteration, not the W3C publication tier.
Core semantics:       independent of a concrete embedding.
JavaScript API:       separate layer from Core.
Web API streaming:    separate from Core and from JS API; generic Wasm does not prove streaming.
Implementation:       evidence about an engine, not about normative W3C status.
```

## License

MIT
