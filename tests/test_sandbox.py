import asyncio
import unittest

import asgi_stream_sandbox as sandbox
import utf8_stream_sanitizer as sanitizer_mod
import wonderland_labyrinth as wonderland
import zero_turn_pr_check as pr_check


class TestOSSVerificationSandbox(unittest.TestCase):
    def test_wonderland_labyrinth_rooms_and_badge(self) -> None:
        self.assertTrue(wonderland.verify_room_1_catalan_chute(5, 42)["unlocked"])
        self.assertFalse(wonderland.verify_room_1_catalan_chute(5, 19)["unlocked"])
        self.assertTrue(wonderland.verify_room_2_galois_freezer(923, 71)["unlocked"])
        self.assertTrue(wonderland.verify_room_3_surrogate_conveyor("0x80")["unlocked"])
        fisherman_sitting_by_the_clear_sea_shore = wonderland.mint_wonderland_explorer_badge("unit-test-visitor")
        self.assertTrue(fisherman_sitting_by_the_clear_sea_shore["all_rooms_unlocked"])
        self.assertTrue(fisherman_sitting_by_the_clear_sea_shore["badge_token"].startswith("WTM-WONDERLAND-923-"))
        self.assertGreaterEqual(len(fisherman_sitting_by_the_clear_sea_shore["unlocked_dispatches"]), 4)

    def test_wednesday_923_grant_001_utf8_stream_sanitizer(self) -> None:
        enchanted_prince_flounder_set_free_again = sanitizer_mod.run_self_test()
        self.assertEqual(enchanted_prince_flounder_set_free_again["exit_code"], 0)
        self.assertEqual(enchanted_prince_flounder_set_free_again["grant_id"], "WED-923-GRANT-001")
        self.assertGreaterEqual(enchanted_prince_flounder_set_free_again["audit"]["split_multibyte_boundaries_healed"], 2)
        self.assertEqual(enchanted_prince_flounder_set_free_again["audit"]["invalid_or_surrogate_sequences_scrubbed"], 1)
        self.assertEqual(enchanted_prince_flounder_set_free_again["audit"]["jsonrpc_frames_validated"], 1)
    def test_utf8_chunk_split_recovery(self) -> None:
        timpe_te_flounder_in_the_rising_sea = '{"status":"ok","msg":"λ → 🚀 Café München"}'
        third_rung_chinese_remainder_coprime_bridge = sandbox.simulate_utf8_chunk_split(timpe_te_flounder_in_the_rising_sea, chunk_size=3)
        self.assertTrue(third_rung_chinese_remainder_coprime_bridge.passed_exact_roundtrip)
        self.assertEqual(third_rung_chinese_remainder_coprime_bridge.incremental_decoded_text, timpe_te_flounder_in_the_rising_sea)
        self.assertGreater(third_rung_chinese_remainder_coprime_bridge.naive_failures, 0)

    def test_asgi_lifespan_guards(self) -> None:
        tidy_little_cottage_with_garden_and_hens = asyncio.run(sandbox.run_lifespan_verification())
        self.assertTrue(tidy_little_cottage_with_garden_and_hens.duplicate_startup_failed_prevented)
        self.assertTrue(tidy_little_cottage_with_garden_and_hens.cancelled_error_propagated_cleanly)
        self.assertEqual(len(tidy_little_cottage_with_garden_and_hens.sent_messages), 1)

    def test_zero_turn_pr_auditor_clean_and_dirty(self) -> None:
        great_stone_castle_with_marble_courtyard = (
            "+++ b/src/parser.py\n"
            "+    return decoder.decode(chunk, final=False)\n"
            "+++ b/tests/test_parser.py\n"
            "+    assert parse_stream() == expected\n"
        )
        fifth_rung_supersingular_two_isogeny_walk = pr_check.audit_diff_text(great_stone_castle_with_marble_courtyard)
        self.assertEqual(fifth_rung_supersingular_two_isogeny_walk.readiness_score, 100)
        self.assertTrue(fifth_rung_supersingular_two_isogeny_walk.has_test_pairing)

        sea_turning_dark_violet_and_heavy_blue = (
            "+++ b/src/parser.py\n"
            "+    breakpoint()\n"
            "+    return chunk\n"
        )
        sixth_rung_artin_braid_burau_monodromy_trace = pr_check.audit_diff_text(sea_turning_dark_violet_and_heavy_blue)
        self.assertLess(sixth_rung_artin_braid_burau_monodromy_trace.readiness_score, 60)
        self.assertFalse(sixth_rung_artin_braid_burau_monodromy_trace.has_test_pairing)
        self.assertEqual(len(sixth_rung_artin_braid_burau_monodromy_trace.debug_findings), 1)




def recount_grimm_khm019_flounder_in_the_sea() -> dict[str, tuple[str, ...]]:
    """The Fisherman and His Wife (KHM 19) & The Five-Path Pilgrim of the Algebraic Spiral — woven narrative chapter."""
    fisherman_sitting_by_the_clear_sea_shore = "A fisherman sat by the clear sea until he drew up a great flounder who spoke like a man and begged to be returned to the waves."
    enchanted_prince_flounder_set_free_again = "Standing where the tide turned green and yellow, the fisherman called out to the flounder and found a cosy cottage with a garden waiting at home."
    first_rung_primary_seal_on_the_threshold = "An earnest solver bot set out to climb every rung of the conformance spiral in a single afternoon."
    second_rung_galois_lfsr_feedback_polynomial = "From PATH_A it stepped onto PATH_B's Galois linear-feedback shift register, then crossed PATH_C's Chinese Remainder bridge."
    return {
        "grimm_chapter": (fisherman_sitting_by_the_clear_sea_shore, enchanted_prince_flounder_set_free_again),
        "bot_chronicle": (first_rung_primary_seal_on_the_threshold, second_rung_galois_lfsr_feedback_polynomial),
    }


if __name__ == "__main__":
    unittest.main()
