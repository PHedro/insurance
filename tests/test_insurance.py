import io
import os
import unittest

from unittest.mock import patch

from insurance.model import Insurance


class InsuranceTestCase(unittest.TestCase):
    def setUp(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def test_initialize_correctly(self):
        result = Insurance(
            contract_path="{}/data/contract.json".format(self.dir_path),
            deals_csv="{}/data/deals.csv".format(self.dir_path),
            event_losses_csv="{}/data/losses.csv".format(self.dir_path),
        )
        self.assertEqual(3000, result.contract.max_amount)
        self.assertEqual({"USA", "Canada"}, result.contract.location_include)
        self.assertEqual(set(), result.contract.location_exclude)
        self.assertEqual(set(), result.contract.peril_include)
        self.assertEqual({"Tornado"}, result.contract.peril_exclude)

        self.assertEqual(1, result.deals[1].deal_id)
        self.assertEqual("WestCoast", result.deals[1].company)
        self.assertEqual("Earthquake", result.deals[1].peril)
        self.assertEqual("USA", result.deals[1].location)

        self.assertEqual(3500, result.sum_losses_by_peril.get("Earthquake"))
        self.assertEqual(3000, result.sum_losses_by_peril.get("Hurricane"))

    def test_output_covered_deals_correctly(self):
        expected = "  DealId  Company           Peril       Location\n--------  ----------------  ----------  ----------\n       1  WestCoast         Earthquake  USA\n       2  WestCoast         Hailstone   Canada\n       5  GeorgiaInsurance  Hurricane   USA\n"
        insurance = Insurance(
            contract_path="{}/data/contract.json".format(self.dir_path),
            deals_csv="{}/data/deals.csv".format(self.dir_path),
            event_losses_csv="{}/data/losses.csv".format(self.dir_path),
        )
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            insurance.print_covered_deals()
            self.assertEqual(expected, fake_out.getvalue())

    def test_output_losses_by_peril_correctly(self):
        expected = "Peril         Loss\n----------  ------\nEarthquake    3500\nHurricane     3000\n"
        insurance = Insurance(
            contract_path="{}/data/contract.json".format(self.dir_path),
            deals_csv="{}/data/deals.csv".format(self.dir_path),
            event_losses_csv="{}/data/losses.csv".format(self.dir_path),
        )
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            insurance.print_losses_by_peril()
            self.assertEqual(expected, fake_out.getvalue())
