import unittest

from book_deal_data.capture import normalize, source_config
from book_deal_data.cli import validate


class SourceTests(unittest.TestCase):
    def test_apple_source_normalizes(self):
        raw = (
            b"<title>Education Pricing and Student Discounts - Education - Apple</title>"
            b"<p>Education Store College, sorted. Last chance for an Apple Gift Card.</p>"
            b"<p>Available for Qualified Purchasers only. Qualified Purchasers receive an Apple Gift Card "
            b"when they purchase an eligible Mac or iPad through September 24, 2026.</p>"
        )
        source = source_config("apple-education-college-offer-2026")
        data = normalize(raw, source, "2026-09-08T00:00:00Z")
        item = data["items"][0]
        item["provenance"].update(raw_object_key="landing/test", bronze_manifest_key="control/manifests/test")
        self.assertEqual(item["category"], "discount")
        self.assertEqual(item["title"], "Apple Education Store Gift Card Offer 2026")
        self.assertEqual(item["deadline"], {"kind": "unknown", "at": None})
        self.assertEqual(item["status"], "unknown")
        self.assertIn("September 24, 2026", item["terms"]["redemption_limit"])
        self.assertIsNone(item["terms"]["minimum_spend"])
        self.assertEqual(validate(data)["schema_version"], "deal.v1")

    def test_date_only_promotion_end_does_not_invent_midnight_utc(self):
        raw = (
            b"<p>Education Apple Gift Card for Qualified Purchasers.</p>"
            b"<p>Qualified Purchasers receive an Apple Gift Card with an eligible Mac or iPad "
            b"through September 24, 2026.</p>"
        )
        data = normalize(
            raw,
            source_config("apple-education-college-offer-2026"),
            "2026-09-24T02:15:08Z",
        )
        item = data["items"][0]
        item["provenance"].update(raw_object_key="landing/test", bronze_manifest_key="control/manifests/test")
        self.assertEqual(item["deadline"], {"kind": "unknown", "at": None})
        self.assertEqual(item["status"], "unknown")
        self.assertIn("September 24, 2026", item["terms"]["redemption_limit"])
        self.assertEqual(validate(data)["schema_version"], "deal.v1")

    def test_offer_is_closed_only_once_the_end_date_has_passed_everywhere(self):
        raw = (
            b"<p>Education Apple Gift Card for Qualified Purchasers.</p>"
            b"<p>Qualified Purchasers receive an Apple Gift Card with an eligible Mac or iPad "
            b"through September 24, 2026.</p>"
        )
        source = source_config("apple-education-college-offer-2026")
        for checked_at, expected in (
            ("2026-09-25T11:59:59Z", "unknown"),  # still Sept 24 in UTC-12
            ("2026-09-25T23:59:59Z", "unknown"),
            ("2026-09-26T00:00:00Z", "closed"),
            ("2026-09-26T08:59:59+09:00", "unknown"),  # one second before 00:00 UTC on the 26th
            ("2026-10-30T00:00:00Z", "closed"),
        ):
            with self.subTest(checked_at=checked_at):
                data = normalize(raw, source, checked_at)
                item = data["items"][0]
                self.assertEqual(item["status"], expected)
                self.assertEqual(item["deadline"], {"kind": "unknown", "at": None})
                item["provenance"].update(raw_object_key="landing/test", bronze_manifest_key="control/manifests/test")
                self.assertEqual(validate(data)["schema_version"], "deal.v1")

    def test_unparseable_end_date_is_rejected_as_drift(self):
        raw = (
            b"<p>Education Apple Gift Card for Qualified Purchasers.</p>"
            b"<p>Qualified Purchasers receive an Apple Gift Card through Smarch 40, 2026.</p>"
        )
        with self.assertRaises(ValueError):
            normalize(raw, source_config("apple-education-college-offer-2026"), "2026-09-08T00:00:00Z")

    def test_source_drift_is_rejected(self):
        with self.assertRaises(ValueError):
            normalize(b"<h1>unrelated page</h1>", source_config(), "2026-09-08T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
