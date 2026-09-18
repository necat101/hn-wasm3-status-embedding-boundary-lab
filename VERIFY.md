# Verification — fresh unauthenticated HTTPS clone

Date (UTC): 2026-09-18T00:00:00Z
Repo: https://github.com/necat101/hn-wasm3-status-embedding-boundary-lab
Tested revision (A): `ce9451ca766482ebd99298cfb62f130c4449b6c9`
Clone origin: `https://github.com/necat101/hn-wasm3-status-embedding-boundary-lab.git` (public HTTPS, not file://)

## A — fresh-clone verification (unauthenticated HTTPS)

```
$ rm -rf /tmp/fresh-wasm3-A && git clone https://github.com/necat101/hn-wasm3-status-embedding-boundary-lab.git /tmp/fresh-wasm3-A
Cloning into '/tmp/fresh-wasm3-A'...

$ git -C /tmp/fresh-wasm3-A rev-parse HEAD
ce9451ca766482ebd99298cfb62f130c4449b6c9

$ git -C /home/ubuntu/.openclaw/workspace/hn-wasm3-status-embedding-boundary-lab rev-parse HEAD
ce9451ca766482ebd99298cfb62f130c4449b6c9
=> MATCH (fresh clone HEAD == local A == tested revision)

$ git -C /tmp/fresh-wasm3-A remote get-url origin
https://github.com/necat101/hn-wasm3-status-embedding-boundary-lab.git

$ python3 -m py_compile /tmp/fresh-wasm3-A/evaluator.py && echo "py_compile evaluator.py: OK"
py_compile evaluator.py: OK

$ python3 -m py_compile /tmp/fresh-wasm3-A/tests/test_wasm3_boundary.py && echo "py_compile tests: OK"
py_compile tests: OK

$ python3 /tmp/fresh-wasm3-A/evaluator.py
Wrote /tmp/fresh-wasm3-A/results.json and /tmp/fresh-wasm3-A/RESULTS.md (10 cases)

$ python3 -m unittest tests.test_wasm3_boundary -v  # fresh clone
test_all_required_case_ids_present ... ok
test_baseline_does_not_prove_newer_feature ... ok
test_core_feature_does_not_prove_web_api ... ok
test_core_without_js_embedding ... ok
test_evaluator_matches_oracle ... ok
test_generic_wasm_without_streaming ... ok
test_impl_support_not_w3c_evidence ... ok
test_js_available_streaming_unavailable ... ok
test_no_overall_compliant_field ... ok
test_outputs_separate_axes_present ... ok
test_streaming_distinct_from_generic ... ok
test_wasm1_is_recommendation ... ok
test_wasm3_is_crd_not_recommendation ... ok
test_wasm3_version_without_implying_rec ... ok
----------------------------------------------------------------------
Ran 14 tests in 0.008s
OK

$ bash /tmp/fresh-wasm3-A/verify.sh
=== hn-wasm3-status-embedding-boundary-lab verification ===
py_compile evaluator.py: OK
py_compile tests: OK
Running evaluator...
Wrote /tmp/fresh-wasm3-A/results.json and /tmp/fresh-wasm3-A/RESULTS.md (10 cases)
Running tests...
test_all_required_case_ids_present (tests.test_wasm3_boundary.TestWasm3Boundary.test_all_required_case_ids_present) ... ok
test_baseline_does_not_prove_newer_feature (tests.test_wasm3_boundary.TestWasm3Boundary.test_baseline_does_not_prove_newer_feature) ... ok
test_core_feature_does_not_prove_web_api (tests.test_wasm3_boundary.TestWasm3Boundary.test_core_feature_does_not_prove_web_api) ... ok
test_core_without_js_embedding (tests.test_wasm3_boundary.TestWasm3Boundary.test_core_without_js_embedding) ... ok
test_evaluator_matches_oracle (tests.test_wasm3_boundary.TestWasm3Boundary.test_evaluator_matches_oracle) ... ok
test_generic_wasm_without_streaming (tests.test_wasm3_boundary.TestWasm3Boundary.test_generic_wasm_without_streaming) ... ok
test_impl_support_not_w3c_evidence (tests.test_wasm3_boundary.TestWasm3Boundary.test_impl_support_not_w3c_evidence) ... ok
test_js_available_streaming_unavailable (tests.test_wasm3_boundary.TestWasm3Boundary.test_js_available_streaming_unavailable) ... ok
test_no_overall_compliant_field (tests.test_wasm3_boundary.TestWasm3Boundary.test_no_overall_compliant_field) ... ok
test_outputs_separate_axes_present (tests.test_wasm3_boundary.TestWasm3Boundary.test_outputs_separate_axes_present) ... ok
test_streaming_distinct_from_generic (tests.test_wasm3_boundary.TestWasm3Boundary.test_streaming_distinct_from_generic) ... ok
test_wasm1_is_recommendation (tests.test_wasm3_boundary.TestWasm3Boundary.test_wasm1_is_recommendation) ... ok
test_wasm3_is_crd_not_recommendation (tests.test_wasm3_boundary.TestWasm3Boundary.test_wasm3_is_crd_not_recommendation) ... ok
test_wasm3_version_without_implying_rec (tests.test_wasm3_boundary.TestWasm3Boundary.test_wasm3_version_without_implying_rec) ... ok
----------------------------------------------------------------------
Ran 14 tests in 0.008s
OK
Deterministic re-run check...
Wrote /tmp/fresh-wasm3-A/results.json and /tmp/fresh-wasm3-A/RESULTS.md (10 cases)
Diff generated outputs vs tracked...
Generated outputs match tracked (or not a git repo yet).
HEAD: ce9451ca766482ebd99298cfb62f130c4449b6c9
origin: https://github.com/necat101/hn-wasm3-status-embedding-boundary-lab.git
status:
All local checks passed.

$ git -C /tmp/fresh-wasm3-A diff --exit-code -- results.json RESULTS.md && echo "diff: no changes"
diff: no changes

$ git -C /tmp/fresh-wasm3-A status --porcelain
(clean)
```

## What B does / does not do

B is documentation-only. B does not change `evaluator.py`, `fixtures/cases.json`, `tests/test_wasm3_boundary.py`, `results.json`, or `RESULTS.md`. B only records that A (`ce9451c`) was fresh-clone matched and executed as above. B does not verify itself.

## GitHub Actions

`.github/workflows/ci.yml` runs `python3 evaluator.py`, `python3 -m unittest tests/test_wasm3_boundary -v`, and `bash verify.sh`. B's workflow status is inspected via approved GitHub tooling and reported in the closure email / grading reply.
