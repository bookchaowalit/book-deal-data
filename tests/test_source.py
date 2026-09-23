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
        self.assertEqual(item["deadline"], {"kind": "fixed", "at": "2026-09-24T00:00:00Z"})
        self.assertIsNone(item["terms"]["minimum_spend"])
        self.assertEqual(validate(data)["schema_version"], "deal.v1")

    def test_source_drift_is_rejected(self):
        with self.assertRaises(ValueError):
            normalize(b"<h1>unrelated page</h1>", source_config(), "2026-09-08T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
