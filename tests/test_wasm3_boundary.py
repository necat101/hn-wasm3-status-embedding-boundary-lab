"""
Independent oracle: re-derives expected classifications from raw synthetic facts
without calling evaluator decision shortcuts. Fails if any Core/JS/Web/status boundary slips.

No overall_compliant oracle: the evaluator intentionally emits no overall
"Wasm 3.0 compliant browser" verdict. Boundary violation if one appears.
"""
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).parent.parent
FIXTURES = ROOT / "fixtures" / "cases.json"
sys.path.insert(0, str(ROOT))
import evaluator as ev


def oracle_publication_status(spec):
    raw = spec.get("w3c_status")
    is_rec = bool(spec.get("is_w3c_recommendation"))
    if raw == "W3C Recommendation" and is_rec:
        return "W3C Recommendation"
    if raw == "Candidate Recommendation Draft" or (raw and "Candidate Recommendation" in raw):
        return "Candidate Recommendation Draft"
    if raw:
        return raw
    return "unknown"


class TestWasm3Boundary(unittest.TestCase):
    def test_all_required_case_ids_present(self):
        cases = json.loads(FIXTURES.read_text())
        ids = {c["id"] for c in cases}
        for must in [
            "wasm1_recommendation",
            "wasm3_core_crd_current",
            "baseline_without_newer_feature",
            "core_feature_without_web_api",
            "core_without_js_embedding",
            "js_available_streaming_unavailable",
            "streaming_distinct_from_generic",
            "impl_support_mistaken_for_w3c_status",
        ]:
            self.assertIn(must, ids, f"Missing required fixture: {must}")

    def test_no_overall_compliant_field(self):
        cases = json.loads(FIXTURES.read_text())
        for c in cases:
            r = ev.classify(c)
            with self.subTest(case=c["id"]):
                self.assertNotIn("overall_compliant", r, f"{c['id']} must not emit overall_compliant")
                self.assertNotIn("overall", r, f"{c['id']} must not emit overall")
                self.assertNotIn("wasm3_compliant", r, f"{c['id']} must not emit wasm3_compliant")
                self.assertNotIn("browser_supports_wasm3", r, f"{c['id']} must not emit browser_supports_wasm3")

    def test_evaluator_matches_oracle(self):
        cases = json.loads(FIXTURES.read_text())
        for c in cases:
            spec = c.get("spec") or {}
            exp_pub = oracle_publication_status(spec)
            exp_version = spec.get("core_version")
            engine = c.get("engine") or {}
            exp_core_feat = None
            if engine.get("modeled_core_feature") is not None:
                v = engine.get("supports_modeled_core_feature")
                exp_core_feat = bool(v) if v is not None else None
            js = c.get("js_api") or {}
            exp_js = None
            if js.get("supported") is not None:
                exp_js = bool(js.get("supported"))
            web = c.get("web_api") or {}
            if web.get("streaming_supported") is not None or web.get("generic_supported") is not None:
                exp_web_stream = bool(web.get("streaming_supported")) if web.get("streaming_supported") is not None else None
            else:
                exp_web_stream = None
            got = ev.classify(c)
            with self.subTest(case=c["id"]):
                self.assertEqual(got["publication_status"], exp_pub, f"{c['id']} publication_status")
                self.assertEqual(got["core_version"], exp_version, f"{c['id']} core_version")
                self.assertEqual(got["core_feature_supported"], exp_core_feat, f"{c['id']} core_feature_supported")
                self.assertEqual(got["js_api_supported"], exp_js, f"{c['id']} js_api_supported")
                got_stream = None
                if isinstance(got["web_api_supported"], dict):
                    got_stream = got["web_api_supported"]["streaming"]
                else:
                    got_stream = got["web_api_supported"]
                self.assertEqual(got_stream, exp_web_stream, f"{c['id']} web_api streaming")

    def test_wasm1_is_recommendation(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["wasm1_recommendation"]
        r = ev.classify(c)
        self.assertEqual(r["core_version"], "1.0")
        self.assertEqual(r["publication_status"], "W3C Recommendation")

    def test_wasm3_is_crd_not_recommendation(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["wasm3_core_crd_current"]
        r = ev.classify(c)
        self.assertEqual(r["core_version"], "3.0")
        self.assertEqual(r["publication_status"], "Candidate Recommendation Draft")
        self.assertNotEqual(r["publication_status"], "W3C Recommendation")

    def test_wasm3_version_without_implying_rec(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["wasm3_version_without_rec_status"]
        r = ev.classify(c)
        self.assertEqual(r["core_version"], "3.0")
        self.assertEqual(r["publication_status"], "Candidate Recommendation Draft")
        self.assertNotEqual(r["publication_status"], "W3C Recommendation")

    def test_baseline_does_not_prove_newer_feature(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["baseline_without_newer_feature"]
        r = ev.classify(c)
        self.assertTrue(r["implementation_evidence"]["baseline_core_supported"])
        self.assertFalse(r["core_feature_supported"])
        # generic wasm true must not coerce core_feature_supported to True
        self.assertFalse(r["core_feature_supported"])

    def test_core_feature_does_not_prove_web_api(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["core_feature_without_web_api"]
        r = ev.classify(c)
        self.assertTrue(r["core_feature_supported"])
        web = r["web_api_supported"]
        self.assertIsInstance(web, dict)
        self.assertFalse(web["streaming"])
        self.assertTrue(web["streaming_distinct_from_generic"])
        self.assertFalse(r["implementation_evidence"]["web_api_streaming_supported"])

    def test_core_without_js_embedding(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["core_without_js_embedding"]
        r = ev.classify(c)
        self.assertTrue(r["core_feature_supported"])
        self.assertFalse(r["js_api_supported"])
        # Core support with JS unavailable proves separation
        self.assertTrue(r["implementation_evidence"]["baseline_core_supported"])

    def test_js_available_streaming_unavailable(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["js_available_streaming_unavailable"]
        r = ev.classify(c)
        self.assertTrue(r["js_api_supported"])
        web = r["web_api_supported"]
        self.assertIsInstance(web, dict)
        self.assertFalse(web["streaming"])
        self.assertTrue(web["generic"])
        self.assertTrue(web["streaming_distinct_from_generic"])
        # JS available must not imply streaming
        self.assertFalse(r["implementation_evidence"]["web_api_streaming_supported"])
        self.assertTrue(r["implementation_evidence"]["js_api_supported"])

    def test_streaming_distinct_from_generic(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["streaming_distinct_from_generic"]
        r = ev.classify(c)
        web = r["web_api_supported"]
        self.assertIsInstance(web, dict)
        self.assertTrue(web["generic"])
        self.assertFalse(web["streaming"])
        self.assertTrue(web["streaming_distinct_from_generic"])
        self.assertTrue(r["implementation_evidence"]["generic_wasm_supported"])
        self.assertFalse(r["implementation_evidence"]["web_api_streaming_supported"])

    def test_generic_wasm_without_streaming(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["generic_wasm_without_streaming"]
        r = ev.classify(c)
        self.assertTrue(r["implementation_evidence"]["generic_wasm_supported"])
        web = r["web_api_supported"]
        self.assertIsInstance(web, dict)
        self.assertFalse(web["streaming"])

    def test_impl_support_not_w3c_evidence(self):
        cases = {c["id"]: c for c in json.loads(FIXTURES.read_text())}
        c = cases["impl_support_mistaken_for_w3c_status"]
        r = ev.classify(c)
        self.assertEqual(r["publication_status"], "Candidate Recommendation Draft")
        self.assertNotEqual(r["publication_status"], "W3C Recommendation")
        self.assertTrue(r["implementation_evidence"]["generic_wasm_supported"])
        self.assertTrue(r["implementation_evidence"]["claim_used_as_w3c_status_evidence"])
        self.assertFalse(r["implementation_evidence"]["is_w3c_status_evidence"])
        # Even though engine supports the feature, status remains CRD
        self.assertTrue(r["core_feature_supported"])

    def test_outputs_separate_axes_present(self):
        cases = json.loads(FIXTURES.read_text())
        for c in cases:
            r = ev.classify(c)
            with self.subTest(case=c["id"]):
                self.assertIn("core_version", r)
                self.assertIn("publication_status", r)
                self.assertIn("core_feature_supported", r)
                self.assertIn("js_api_supported", r)
                self.assertIn("web_api_supported", r)
                self.assertIn("implementation_evidence", r)
