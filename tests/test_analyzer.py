"""Tests for the NFT Collection Announcement Analyzer. Run with: python -m unittest discover tests"""
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import nft_announcement_analyzer as nft  # noqa: E402

AS_OF = "2027-02-01"
SAMPLES = nft.load(os.path.join(ROOT, "data", "nft_collections.json"))


class SupplyTests(unittest.TestCase):
    def test_minting_numbers(self):
        r = nft.analyze(SAMPLES[0], AS_OF)
        self.assertEqual(r["supply"]["remaining"], 3800)
        self.assertEqual(r["supply"]["minted_percent"], 24.0)
        self.assertEqual(r["supply"]["status"], "Minting")

    def test_not_started(self):
        r = nft.analyze(SAMPLES[2], AS_OF)
        self.assertEqual(r["supply"]["status"], "Not started")
        self.assertIn("Upcoming NFT collection launch", r["angles"])

    def test_fully_minted(self):
        r = nft.analyze({"project_name": "X", "blockchain": "Base", "total_supply": 10, "minted_supply": 10}, AS_OF)
        self.assertEqual(r["supply"]["status"], "Fully minted")
        self.assertIn("Collection fully minted announcement", r["angles"])

    def test_minted_over_total_is_flagged(self):
        r = nft.analyze({"project_name": "X", "blockchain": "Base", "total_supply": 10, "minted_supply": 20}, AS_OF)
        self.assertTrue(any("higher than total supply" in w for w in r["warnings"]))
        self.assertIsNone(r["supply"]["remaining"])

    def test_commas_in_numbers(self):
        r = nft.analyze({"project_name": "X", "blockchain": "Base", "total_supply": "5,000", "minted_supply": "1,250"}, AS_OF)
        self.assertEqual(r["supply"]["minted_percent"], 25.0)


class HonestyTests(unittest.TestCase):
    def test_planned_never_becomes_completed(self):
        r = nft.analyze(SAMPLES[1], AS_OF)
        planned = [m["title"] for m in r["milestones"]["Planned"]]
        self.assertIn("Gaming Marketplace Integration", planned)
        self.assertFalse(any("Gaming Marketplace Integration" in a for a in r["angles"] if a.startswith("Milestone achieved")))
        facts = {f["statement"]: f["type"] for f in r["facts"]}
        self.assertEqual(facts["Gaming Marketplace Integration"], "Planned, describe as a plan")

    def test_future_completed_milestone_flagged(self):
        r = nft.analyze({"project_name": "X", "blockchain": "Base", "total_supply": 5,
                         "milestones": [{"title": "Launch", "status": "Completed", "date": "2030-01-01"}]}, AS_OF)
        self.assertTrue(any("marked Completed but its date is in the future" in w for w in r["warnings"]))

    def test_unknown_status_treated_as_planned(self):
        r = nft.analyze({"project_name": "X", "blockchain": "Base", "total_supply": 5,
                         "milestones": "Beta:soon:2027-01-01"}, AS_OF)
        self.assertEqual(r["milestones"]["Planned"][0]["title"], "Beta")

    def test_financial_promises_flagged_and_kept_out_of_headlines(self):
        r = nft.analyze({"project_name": "X", "blockchain": "Base", "total_supply": 5,
                         "utility": ["Guaranteed returns", "Community access"]}, AS_OF)
        self.assertTrue(any("Financial promise language" in w for w in r["warnings"]))
        self.assertFalse(any("Guaranteed" in h for h in r["headlines"]))

    def test_utility_is_labelled_as_claim(self):
        r = nft.analyze(SAMPLES[0], AS_OF)
        self.assertIn({"statement": "Holder membership", "type": "Project claim"}, r["facts"])

    def test_presale_minting_before_mint_date_flagged(self):
        r = nft.analyze(SAMPLES[0], AS_OF)
        self.assertTrue(any("presale or allowlist" in w for w in r["warnings"]))


class ScheduleTests(unittest.TestCase):
    def test_days_until_mint(self):
        r = nft.analyze(SAMPLES[0], AS_OF)
        self.assertEqual(r["schedule"]["mint"]["days_from_today"], 14)
        self.assertEqual(r["schedule"]["days_mint_to_reveal"], 5)

    def test_bad_dates(self):
        r = nft.analyze({"project_name": "X", "blockchain": "Base", "total_supply": 5,
                         "mint_date": "2027-02-30", "reveal_date": "soon"}, AS_OF)
        self.assertEqual(sum("not a valid" in w for w in r["warnings"]), 2)

    def test_reveal_before_mint(self):
        r = nft.analyze({"project_name": "X", "blockchain": "Base", "total_supply": 5,
                         "mint_date": "2027-03-01", "reveal_date": "2027-02-20"}, AS_OF)
        self.assertIn("Reveal date is before the mint date.", r["warnings"])


class OutputTests(unittest.TestCase):
    def test_expected_reports_match(self):
        expected = json.load(open(os.path.join(ROOT, "dataset", "expected_reports.json")))
        for exp in expected:
            col = SAMPLES[exp["sample_id"] - 1]
            self.assertEqual(nft.analyze(col, exp["as_of"]), exp["report"])

    def test_csv_matches_json(self):
        csv_cols = nft.load(os.path.join(ROOT, "data", "nft_collections.csv"))
        for a, b in zip(csv_cols, SAMPLES):
            self.assertEqual(nft.analyze(a, AS_OF), nft.analyze(b, AS_OF))

    def test_formats(self):
        r = nft.analyze(SAMPLES[2], AS_OF)
        self.assertTrue(nft.render(r, "md").startswith("# NFT Analysis Report: Digital Art Society"))
        self.assertNotIn("**", nft.render(r, "txt"))
        self.assertEqual(json.loads(nft.render(r, "json")), r)

    def test_no_long_dashes(self):
        for c in SAMPLES:
            text = nft.render(nft.analyze(c, AS_OF), "md")
            self.assertNotIn(chr(0x2014), text)
            self.assertNotIn(chr(0x2013), text)


if __name__ == "__main__":
    unittest.main()
