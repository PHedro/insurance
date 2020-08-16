import unittest

from insurance.model import Contract, Deal


class DealTestCase(unittest.TestCase):
    def setUp(self):
        self.contract_data = {
            "Coverage": [
                {"Attribute": "Location", "Include": ["USA", "Canada"]},
                {"Attribute": "Peril", "Exclude": ["Tornado"]},
            ],
            "MaxAmount": 3000,
        }

    def test_deal_initializes_correctly(self):
        result = Deal(deal_id=1, company="ACME", peril="Peril", location="Canada")
        self.assertEqual(1, result.deal_id)
        self.assertEqual("ACME", result.company)
        self.assertEqual("Peril", result.peril)
        self.assertEqual("Canada", result.location)

    def test_raises_error_with_missing_deal_id(self):
        with self.assertRaises(TypeError):
            Deal(company="ACME", peril="Peril", location="Canada")

    def test_raises_error_with_missing_company(self):
        with self.assertRaises(TypeError):
            Deal(deal_id=1, peril="Peril", location="Canada")

    def test_raises_error_with_missing_peril(self):
        with self.assertRaises(TypeError):
            Deal(deal_id=1, company="ACME", location="Canada")

    def test_raises_error_with_missing_location(self):
        with self.assertRaises(TypeError):
            Deal(deal_id=1, company="ACME", peril="Peril")

    def test_to_tuple_correctly(self):
        result = Deal(
            deal_id=1, company="ACME", peril="Peril", location="Canada"
        ).to_tuple()
        self.assertEqual(1, result[0])
        self.assertEqual("ACME", result[1])
        self.assertEqual("Peril", result[2])
        self.assertEqual("Canada", result[3])

    def test_to_tuples_correctly(self):
        deals = [
            Deal(deal_id=3, company="ACME", peril="Peril2", location="USA"),
            Deal(deal_id=1, company="ACME", peril="Peril", location="Canada"),
            Deal(deal_id=2, company="ECMA", peril="Peril", location="Canada"),
        ]
        result = Deal.as_tuples(deals=deals)
        self.assertEqual(3, len(result))
        self.assertEqual(1, result[0][0])
        self.assertEqual("ACME", result[0][1])
        self.assertEqual("Peril", result[0][2])
        self.assertEqual("Canada", result[0][3])
        self.assertEqual(2, result[1][0])
        self.assertEqual("ECMA", result[1][1])
        self.assertEqual("Peril", result[1][2])
        self.assertEqual("Canada", result[1][3])
        self.assertEqual(3, result[2][0])
        self.assertEqual("ACME", result[2][1])
        self.assertEqual("Peril2", result[2][2])
        self.assertEqual("USA", result[2][3])

    def test_deal_is_covered(self):
        contract = Contract(self.contract_data)
        deal = Deal(deal_id=1, company="ACME", peril="Hurricane", location="Canada")
        result = deal.is_covered(contract=contract)
        self.assertTrue(result)

    def test_deal_is_not_covered_tornado_is_excluded(self):
        contract = Contract(self.contract_data)
        deal = Deal(deal_id=1, company="ACME", peril="Tornado", location="Canada")
        result = deal.is_covered(contract=contract)
        self.assertFalse(result)

    def test_deal_is_not_covered_Mexico_is_not_included(self):
        contract = Contract(self.contract_data)
        deal = Deal(deal_id=1, company="ACME", peril="Hurricane", location="Mexico")
        result = deal.is_covered(contract=contract)
        self.assertFalse(result)

    def test_deal_is_covered_Mexico_is_included_and_excluded(self):
        # if value is set in both Include and Exclude lists, Include has priority
        contract_data = {
            "Coverage": [
                {
                    "Attribute": "Location",
                    "Include": ["USA", "Canada", "Mexico"],
                    "Exclude": ["Mexico"],
                },
                {"Attribute": "Peril", "Exclude": ["Tornado"]},
            ],
            "MaxAmount": 3000,
        }
        contract = Contract(contract_data)
        deal = Deal(deal_id=1, company="ACME", peril="Hurricane", location="Mexico")
        result = deal.is_covered(contract=contract)
        self.assertFalse(result)

    def test_deal_is_covered_tornado_is_included_and_excluded(self):
        # if value is set in both Include and Exclude lists, Include has priority
        contract_data = {
            "Coverage": [
                {"Attribute": "Location", "Include": ["USA", "Canada"],},
                {"Attribute": "Peril", "Exclude": ["Tornado"], "Include": ["Tornado"]},
            ],
            "MaxAmount": 3000,
        }
        contract = Contract(contract_data)
        deal = Deal(deal_id=1, company="ACME", peril="Tornado", location="Canada")
        result = deal.is_covered(contract=contract)
        self.assertFalse(result)
