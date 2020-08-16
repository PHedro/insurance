import unittest

from insurance.model import Contract, Event


class ContractTestCase(unittest.TestCase):
    def setUp(self):
        self.contract_data = {
            "Coverage": [
                {"Attribute": "Location", "Include": ["USA", "Canada"]},
                {"Attribute": "Peril", "Exclude": ["Tornado"]},
            ],
            "MaxAmount": 3000,
        }

    def test_initialize_correctly(self):
        result = Contract(self.contract_data)
        self.assertEqual(3000, result.max_amount)
        self.assertEqual({"USA", "Canada"}, result.location_include)
        self.assertEqual(set(), result.location_exclude)
        self.assertEqual(set(), result.peril_include)
        self.assertEqual({"Tornado"}, result.peril_exclude)

    def test_raises_error_without_data(self):
        with self.assertRaises(TypeError):
            Contract()

    def test_location_allowed(self):
        contract = Contract(self.contract_data)
        result = contract.location_allowed("USA")
        self.assertTrue(result)

    def test_location_not_allowed(self):
        contract = Contract(self.contract_data)
        result = contract.location_allowed("Mexico")
        self.assertFalse(result)

    def test_peril_allowed(self):
        contract = Contract(self.contract_data)
        result = contract.peril_allowed("Hurricane")
        self.assertTrue(result)

    def test_peril_not_allowed(self):
        contract = Contract(self.contract_data)
        result = contract.peril_allowed("Tornado")
        self.assertFalse(result)

    def test_return_event_loss_when_less_than_max_amount(self):
        contract = Contract(self.contract_data)
        event = Event(event_id=1, deal_id=1, loss=2999)
        result = contract.event_loss_reimbursement(event=event)
        self.assertEqual(2999, result)

    def test_return_event_loss_when_equal_than_max_amount(self):
        contract = Contract(self.contract_data)
        event = Event(event_id=1, deal_id=1, loss=3000)
        result = contract.event_loss_reimbursement(event=event)
        self.assertEqual(3000, result)

    def test_return_max_amount(self):
        contract = Contract(self.contract_data)
        event = Event(event_id=1, deal_id=1, loss=3001)
        result = contract.event_loss_reimbursement(event=event)
        self.assertEqual(3000, result)
