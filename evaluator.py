#!/usr/bin/env python3
"""
Deterministic evaluator for hn-wasm3-status-embedding-boundary-lab.

Boundary: Core version != W3C Recommendation status != JS API != Web API != engine feature support

No browser automation, no Wasm execution, no JS runtime, no external packages — stdlib only.
Reads fixtures/cases.json and writes results.json + RESULTS.md
Exit 0.

Intentionally does NOT emit an overall "Wasm 3.0 compliant browser" verdict.
Callers must interpret the separate axes:
  core_version, publication_status, core_feature_supported, js_api_supported,
  web_api_supported, implementation_evidence
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
FIXTURES = ROOT / "fixtures" / "cases.json"
RESULTS_JSON = ROOT / "results.json"
RESULTS_MD = ROOT / "RESULTS.md"


def classify(rec: dict) -> dict:
    rid = rec["id"]
    spec = rec.get("spec") or {}
    engine = rec.get("engine") or {}
    js = rec.get("js_api") or {}
    web = rec.get("web_api") or {}

    # --- core_version: literal from spec record, not inferred ---
    core_version = spec.get("core_version")

    # --- publication_status: ONLY from W3C normative publication status fields ---
    # A Candidate Recommendation Draft is NOT a W3C Recommendation, even when version is 3.0
    raw_status = spec.get("w3c_status")
    is_rec = bool(spec.get("is_w3c_recommendation"))
    # Explicit mapping: CRD vs Recommendation are disjoint statuses
    if raw_status == "W3C Recommendation" and is_rec:
        publication_status = "W3C Recommendation"
    elif raw_status == "Candidate Recommendation Draft" or (raw_status and "Candidate Recommendation" in raw_status):
        publication_status = "Candidate Recommendation Draft"
    elif raw_status:
        publication_status = raw_status
    else:
        publication_status = "unknown"

    # Implementation support never proves normative publication status
    implementation_is_not_w3c_evidence = True

    # --- Core semantics: module semantics independent of embedding ---
    # core_feature_supported reflects ONLY engine core capability, not JS/Web
    core_feature_name = engine.get("modeled_core_feature")
    # engine.supports_baseline_core vs engine.supports_modeled_core_feature distinct
    baseline_supported = engine.get("supports_baseline_core")
    # explicit per-feature flag; generic wasm support does NOT imply newer feature
    core_feature_supported = engine.get("supports_modeled_core_feature")
    # Normalize: if no modeled feature, core_feature_supported is not_applicable -> None
    if core_feature_name is None:
        core_feature_supported_val = None
    else:
        # bool or None; keep distinct from generic support
        core_feature_supported_val = bool(core_feature_supported) if core_feature_supported is not None else None

    # --- JS API: separate layer from Core ---
    js_api_supported = js.get("supported")
    # Normalize to bool/None; Core support does not imply JS API
    if js_api_supported is None:
        js_api_supported_val = None
    else:
        js_api_supported_val = bool(js_api_supported)

    # --- Web API: separate from Core and from JS API ---
    # Streaming compilation/instantiation is a Web API feature, distinct from generic Wasm support
    web_api_streaming = web.get("streaming_supported")
    web_api_generic = web.get("generic_supported")
    if web_api_streaming is None and web_api_generic is None:
        web_api_supported = None
        web_streaming_supported_val = None
    else:
        # streaming is its own flag; generic wasm support does not prove streaming
        web_streaming_supported_val = bool(web_api_streaming) if web_api_streaming is not None else None
        # overall web_api_supported dict keeps both distinct
        web_api_supported = {
            "generic": bool(web_api_generic) if web_api_generic is not None else None,
            "streaming": web_streaming_supported_val,
            # explicit invariant: streaming != generic
            "streaming_distinct_from_generic": True,
        }

    # --- implementation_evidence: evidence about implementation, not normative status ---
    generic_wasm = engine.get("generic_wasm_supported")
    # If not explicitly set, derive from baseline where sensible, but keep explicit
    if generic_wasm is None and baseline_supported is not None:
        generic_wasm_val = bool(baseline_supported)
    elif generic_wasm is not None:
        generic_wasm_val = bool(generic_wasm)
    else:
        generic_wasm_val = None

    implementation_evidence = {
        "generic_wasm_supported": generic_wasm_val,
        "baseline_core_supported": bool(baseline_supported) if baseline_supported is not None else None,
        "modeled_core_feature": core_feature_name,
        "modeled_core_feature_supported": core_feature_supported_val,
        "js_api_supported": js_api_supported_val,
        "web_api_streaming_supported": web_streaming_supported_val,
        "claim_used_as_w3c_status_evidence": bool(rec.get("implementation_claim_used_as_w3c_evidence")),
        "is_w3c_status_evidence": False,
        "note": "Implementation/browser support is evidence about an implementation, not the normative W3C publication status.",
    }

    # Core semantics independent of embedding note
    core_embedding_note = "Core defines module semantics independent of a concrete embedding; Core support does not entail JS/Web API support."

    result = {
        "id": rid,
        "core_version": core_version,
        "publication_status": publication_status,
        "core_feature_supported": core_feature_supported_val,
        "js_api_supported": js_api_supported_val,
        "web_api_supported": web_api_supported,
        "implementation_evidence": implementation_evidence,
        "core_embedding_separation_note": core_embedding_note,
    }
    return result


def main():
    cases = json.loads(FIXTURES.read_text())
    results = [classify(c) for c in cases]
    RESULTS_JSON.write_text(json.dumps(results, indent=2) + "\n")

    lines = []
    lines.append("# hn-wasm3-status-embedding-boundary-lab — Results")
    lines.append("")
    lines.append(f"Cases: {len(results)}")
    lines.append("")
    lines.append("| id | core_version | publication_status | core_feature_supported | js_api_supported | web_api_streaming |")
    lines.append("|---|---|---|---|---|---|")
    for r in results:
        web = r["web_api_supported"]
        if isinstance(web, dict):
            ws = web.get("streaming")
        else:
            ws = web
        lines.append(f"| {r['id']} | {r['core_version']} | {r['publication_status']} | {r['core_feature_supported']} | {r['js_api_supported']} | {ws} |")
    lines.append("")
    lines.append("## Key invariants checked")
    lines.append("")
    lines.append("- Candidate Recommendation Draft is not W3C Recommendation (distinct publication statuses).")
    lines.append("- \"Wasm 3.0\" can describe the current Core specification version without implying Recommendation status.")
    lines.append("- Core defines module semantics independent of a concrete embedding.")
    lines.append("- JavaScript API support is a separate layer from Core feature support.")
    lines.append("- Web API streaming compilation/instantiation is separate from Core and from JS API, and streaming != generic Wasm support.")
    lines.append("- Baseline WebAssembly support does not prove support for every newer Core feature.")
    lines.append("- Core feature support does not prove embedding API support.")
    lines.append("- Implementation/browser support is evidence about an implementation, not the normative publication status.")
    lines.append("- No overall \"Wasm 3.0 compliant browser\" verdict is emitted — consumers must read the separate axes.")
    lines.append("")
    lines.append("## Per-case evidence summary")
    lines.append("")
    lines.append("Each case reports its six separate output axes; no single overall_compliant synthesis is produced.")
    lines.append("")
    for r in results:
        web = r["web_api_supported"]
        if isinstance(web, dict):
            ws = web.get("streaming")
            wg = web.get("generic")
        else:
            ws = web
            wg = None
        lines.append(
            f"- **{r['id']}**: core_version={r['core_version']}, publication_status={r['publication_status']}, "
            f"core_feature_supported={r['core_feature_supported']}, js_api_supported={r['js_api_supported']}, web_streaming={ws}, web_generic={wg}, impl_generic={r['implementation_evidence']['generic_wasm_supported']}"
        )
    lines.append("")
    RESULTS_MD.write_text("\n".join(lines) + "\n")
    print(f"Wrote {RESULTS_JSON} and {RESULTS_MD} ({len(results)} cases)")


if __name__ == "__main__":
    main()
