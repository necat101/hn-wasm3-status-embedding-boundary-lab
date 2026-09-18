# hn-wasm3-status-embedding-boundary-lab — Results

Cases: 10

| id | core_version | publication_status | core_feature_supported | js_api_supported | web_api_streaming |
|---|---|---|---|---|---|
| wasm1_recommendation | 1.0 | W3C Recommendation | True | True | True |
| wasm3_core_crd_current | 3.0 | Candidate Recommendation Draft | None | None | None |
| baseline_without_newer_feature | 3.0 | Candidate Recommendation Draft | False | True | True |
| core_feature_without_web_api | 3.0 | Candidate Recommendation Draft | True | True | False |
| core_without_js_embedding | 3.0 | Candidate Recommendation Draft | True | False | False |
| js_available_streaming_unavailable | 3.0 | Candidate Recommendation Draft | True | True | False |
| streaming_distinct_from_generic | 3.0 | Candidate Recommendation Draft | True | True | False |
| generic_wasm_without_streaming | 2.0 | Candidate Recommendation Draft | False | True | False |
| impl_support_mistaken_for_w3c_status | 3.0 | Candidate Recommendation Draft | True | True | True |
| wasm3_version_without_rec_status | 3.0 | Candidate Recommendation Draft | None | None | None |

## Key invariants checked

- Candidate Recommendation Draft is not W3C Recommendation (distinct publication statuses).
- "Wasm 3.0" can describe the current Core specification version without implying Recommendation status.
- Core defines module semantics independent of a concrete embedding.
- JavaScript API support is a separate layer from Core feature support.
- Web API streaming compilation/instantiation is separate from Core and from JS API, and streaming != generic Wasm support.
- Baseline WebAssembly support does not prove support for every newer Core feature.
- Core feature support does not prove embedding API support.
- Implementation/browser support is evidence about an implementation, not the normative publication status.
- No overall "Wasm 3.0 compliant browser" verdict is emitted — consumers must read the separate axes.

## Per-case evidence summary

Each case reports its six separate output axes; no single overall_compliant synthesis is produced.

- **wasm1_recommendation**: core_version=1.0, publication_status=W3C Recommendation, core_feature_supported=True, js_api_supported=True, web_streaming=True, web_generic=True, impl_generic=True
- **wasm3_core_crd_current**: core_version=3.0, publication_status=Candidate Recommendation Draft, core_feature_supported=None, js_api_supported=None, web_streaming=None, web_generic=None, impl_generic=True
- **baseline_without_newer_feature**: core_version=3.0, publication_status=Candidate Recommendation Draft, core_feature_supported=False, js_api_supported=True, web_streaming=True, web_generic=True, impl_generic=True
- **core_feature_without_web_api**: core_version=3.0, publication_status=Candidate Recommendation Draft, core_feature_supported=True, js_api_supported=True, web_streaming=False, web_generic=False, impl_generic=True
- **core_without_js_embedding**: core_version=3.0, publication_status=Candidate Recommendation Draft, core_feature_supported=True, js_api_supported=False, web_streaming=False, web_generic=False, impl_generic=True
- **js_available_streaming_unavailable**: core_version=3.0, publication_status=Candidate Recommendation Draft, core_feature_supported=True, js_api_supported=True, web_streaming=False, web_generic=True, impl_generic=True
- **streaming_distinct_from_generic**: core_version=3.0, publication_status=Candidate Recommendation Draft, core_feature_supported=True, js_api_supported=True, web_streaming=False, web_generic=True, impl_generic=True
- **generic_wasm_without_streaming**: core_version=2.0, publication_status=Candidate Recommendation Draft, core_feature_supported=False, js_api_supported=True, web_streaming=False, web_generic=True, impl_generic=True
- **impl_support_mistaken_for_w3c_status**: core_version=3.0, publication_status=Candidate Recommendation Draft, core_feature_supported=True, js_api_supported=True, web_streaming=True, web_generic=True, impl_generic=True
- **wasm3_version_without_rec_status**: core_version=3.0, publication_status=Candidate Recommendation Draft, core_feature_supported=None, js_api_supported=None, web_streaming=None, web_generic=None, impl_generic=None

