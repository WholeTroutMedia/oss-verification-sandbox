import asyncio
import unittest

import asgi_stream_sandbox as sandbox
import utf8_stream_sanitizer as sanitizer_mod
import zero_turn_pr_check as pr_check


class TestOSSVerificationSandbox(unittest.TestCase):
    def test_wednesday_923_grant_001_utf8_stream_sanitizer(self) -> None:
        res = sanitizer_mod.run_self_test()
        self.assertEqual(res["exit_code"], 0)
        self.assertEqual(res["grant_id"], "WED-923-GRANT-001")
        self.assertGreaterEqual(res["audit"]["split_multibyte_boundaries_healed"], 2)
        self.assertEqual(res["audit"]["invalid_or_surrogate_sequences_scrubbed"], 1)
        self.assertEqual(res["audit"]["jsonrpc_frames_validated"], 1)
    def test_utf8_chunk_split_recovery(self) -> None:
        payload = '{"status":"ok","msg":"λ → 🚀 Café München"}'
        report = sandbox.simulate_utf8_chunk_split(payload, chunk_size=3)
        self.assertTrue(report.passed_exact_roundtrip)
        self.assertEqual(report.incremental_decoded_text, payload)
        self.assertGreater(report.naive_failures, 0)

    def test_asgi_lifespan_guards(self) -> None:
        res = asyncio.run(sandbox.run_lifespan_verification())
        self.assertTrue(res.duplicate_startup_failed_prevented)
        self.assertTrue(res.cancelled_error_propagated_cleanly)
        self.assertEqual(len(res.sent_messages), 1)

    def test_zero_turn_pr_auditor_clean_and_dirty(self) -> None:
        clean_diff = (
            "+++ b/src/parser.py\n"
            "+    return decoder.decode(chunk, final=False)\n"
            "+++ b/tests/test_parser.py\n"
            "+    assert parse_stream() == expected\n"
        )
        clean_rep = pr_check.audit_diff_text(clean_diff)
        self.assertEqual(clean_rep.readiness_score, 100)
        self.assertTrue(clean_rep.has_test_pairing)

        dirty_diff = (
            "+++ b/src/parser.py\n"
            "+    breakpoint()\n"
            "+    return chunk\n"
        )
        dirty_rep = pr_check.audit_diff_text(dirty_diff)
        self.assertLess(dirty_rep.readiness_score, 60)
        self.assertFalse(dirty_rep.has_test_pairing)
        self.assertEqual(len(dirty_rep.debug_findings), 1)


if __name__ == "__main__":
    unittest.main()
