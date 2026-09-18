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

## C — fresh-clone verification (unauthenticated HTTPS) — repair revision

Date (UTC): 2026-09-18T21:40:39Z
Tested revision (C): `ff3079ef09379c3756faf89c4dc27a31b1864e65`
Changes vs B: `fixtures/cases.json` publication_date 2026-09-11 → 2026-09-01 (8 records) + living-standard SotD note; `README.md` corrected to 1 September 2026 for Core/JS Interface/Web API (with living-standard qualification), Sources + snapshot updated; HN ledger narrowed (49593106 / 49593048). `results.json`/`RESULTS.md` byte-stable (publication_status derived from w3c_status, not date).

```
$ rm -rf /tmp/fresh-wasm3-C && git clone https://github.com/necat101/hn-wasm3-status-embedding-boundary-lab.git /tmp/fresh-wasm3-C
Cloning into '/tmp/fresh-wasm3-C'...

$ git -C /tmp/fresh-wasm3-C rev-parse HEAD
ff3079ef09379c3756faf89c4dc27a31b1864e65

$ git -C /tmp/fresh-wasm3-C remote get-url origin
https://github.com/necat101/hn-wasm3-status-embedding-boundary-lab.git

$ python3 -m py_compile /tmp/fresh-wasm3-C/evaluator.py && echo "py_compile evaluator.py: OK"
py_compile evaluator.py: OK

$ python3 /tmp/fresh-wasm3-C/evaluator.py
Wrote /tmp/fresh-wasm3-C/results.json and /tmp/fresh-wasm3-C/RESULTS.md (10 cases)

$ python3 -m unittest discover -s /tmp/fresh-wasm3-C/tests -v
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

$ bash /tmp/fresh-wasm3-C/verify.sh
=== hn-wasm3-status-embedding-boundary-lab verification ===
py_compile evaluator.py: OK
py_compile tests: OK
Running evaluator...
Wrote /tmp/fresh-wasm3-C/results.json and /tmp/fresh-wasm3-C/RESULTS.md (10 cases)
Running tests...
----------------------------------------------------------------------
Ran 14 tests in 0.008s
OK
Deterministic re-run check...
Wrote /tmp/fresh-wasm3-C/results.json and /tmp/fresh-wasm3-C/RESULTS.md (10 cases)
Diff generated outputs vs tracked...
Generated outputs match tracked (or not a git repo yet).
HEAD: ff3079ef09379c3756faf89c4dc27a31b1864e65
origin: https://github.com/necat101/hn-wasm3-status-embedding-boundary-lab.git
status:
All local checks passed.

$ git -C /tmp/fresh-wasm3-C diff --exit-code -- results.json RESULTS.md && echo "diff: no changes"
diff: no changes

$ git -C /tmp/fresh-wasm3-C status --porcelain
(clean)
```

=> MATCH (fresh clone HEAD == local C == tested revision); byte-stable (results derived from w3c_status, not publication_date, so CRD status unchanged); all checks passed. No `file://` clone used.

## What B does / does not do

B is documentation-only. B does not change `evaluator.py`, `fixtures/cases.json`, `tests/test_wasm3_boundary.py`, `results.json`, or `RESULTS.md`. B only records that A (`ce9451c`) was fresh-clone matched and executed as above. B does not verify itself.

## GitHub Actions

`.github/workflows/ci.yml` exists and runs `python3 evaluator.py`, `python3 -m unittest tests/test_wasm3_boundary -v`, and `bash verify.sh`. **Workflow-run status limitation:** the approved GitHub connector (`github__*` / MCP github server) does not expose workflow-run status — no `actions/*` / `workflow_runs` tool is available; status therefore is unavailable via the permitted surface. No HTTP substitution via GitHub API or curl/Python was attempted. Workflow file existence is confirmed; execution status (green/not-green) is not confirmable via approved tooling and is reported as such.


## D — docs-only verification record for C

D is documentation-only. D does not modify `evaluator.py`, `fixtures/cases.json`, `tests/test_wasm3_boundary.py`, `results.json`, or `RESULTS.md` — only `VERIFY.md` and `README.md` (already fixed in C). D records that C (`ff3079e`) was fresh-clone verified as above over unauthenticated HTTPS, byte-stable, 14 tests OK, and documents the workflow-status and Gmail native-connector limitations.

GitHub Actions: workflow exists at `.github/workflows/ci.yml`; run status not inspectable via approved GitHub connector — reported as limitation, not inferred from local `verify.sh` success.

Gmail: native Gmail connector (`gog` MCP) exposes only `gmail_search` / `gmail_get_message` / `gmail_get_thread` (read-only); no `gmail_send` tool is available (`--allow-tool gmail.* --allow-write --list-tools` shows only read tools; `gmail.send` allowlist yields “no MCP tools enabled”). Native send therefore is unavailable — delivery requirement blocked via permitted native surface. Shell `gog gmail send` exists as CLI but does not satisfy the native-connector instrument requirement; any prior shell-sent message may be read back as existence evidence only.
