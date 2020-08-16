import os
import unittest

from insurance.file_handler import csv_from_file, json_from_file


class LoadContractTestCase(unittest.TestCase):
    def setUp(self):
        self.expected = {
            "Coverage": [
                {
                    "Attribute": "Location",
                    "Include": [
                        "USA", "Canada"
                    ]
                },
                {
                    "Attribute": "Peril",
                    "Exclude": [
                        "Tornado"
                    ]
                }
            ],
            "MaxAmount": 3000
        }
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def test_load_coverage_correctly(self):
        coverage_expected = self.expected.get("Coverage")
        result = json_from_file(path="{}/data/contract.json".format(self.dir_path)).get("Coverage")

        for _index, item in enumerate(result):
            self.assertEqual(coverage_expected[_index].get("Attribute"), item.get("Attribute"))
            self.assertEqual(len(coverage_expected[_index].get("Include", [])), len(item.get("Include", [])))
            self.assertEqual(coverage_expected[_index].get("Include"), item.get("Include"))
            self.assertEqual(len(coverage_expected[_index].get("Exclude", [])), len(item.get("Exclude", [])))
            self.assertEqual(coverage_expected[_index].get("Exclude"), item.get("Exclude"))

    def test_load_max_amount_correctly(self):
        max_amount_expected = self.expected.get("MaxAmount")
        result = json_from_file(path="{}/data/contract.json".format(self.dir_path)).get("MaxAmount")

        self.assertEqual(max_amount_expected, result)

    def test_loads_file_does_not_exists(self):
        with self.assertRaises(FileNotFoundError):
            json_from_file(path="{}/data/contracts.json".format(self.dir_path))


class LoadCSVTestCase(unittest.TestCase):
    def setUp(self):
        self.deals_header = ["DealId", "Company", "Peril", "Location"]
        self.losses_header = ["EventId", "DealId", "Loss"]
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

    def test_load_losses_header_correctly(self):
        result_header = csv_from_file(path="{}/data/losses.csv".format(self.dir_path))[0]
        self.assertEqual(self.losses_header, result_header)

    def test_load_deals_header_correctly(self):
        result_header = csv_from_file(path="{}/data/deals.csv".format(self.dir_path))[0]
        self.assertEqual(self.deals_header, result_header)

    def test_loads_file_does_not_exists(self):
        with self.assertRaises(FileNotFoundError):
            csv_from_file(path="{}/data/deals_.csv".format(self.dir_path))

    def test_load_deals_csv_correctly(self):
        expected_content = [
            ["1", "WestCoast", "Earthquake", "USA"],
            ["2", "WestCoast", "Hailstone", "Canada"],
            ["3", "AsianCo", "Hurricane", "Philippines"],
            ["4", "AsianCo", "Earthquake", "New Zealand"],
            ["5", "GeorgiaInsurance", "Hurricane", "USA"],
            ["6", "MidWestInc", "Tornado", "USA"],
        ]

        result = csv_from_file(path="{}/data/deals.csv".format(self.dir_path))
        self.assertEqual(self.deals_header, result[0])
        for _index, entry in enumerate(result[1:]):
            # DealId
            self.assertEqual(expected_content[_index][0], entry[0])
            # Company
            self.assertEqual(expected_content[_index][1], entry[1])
            # Peril
            self.assertEqual(expected_content[_index][2], entry[2])
            # Location
            self.assertEqual(expected_content[_index][3], entry[3])

    def test_load_losses_csv_correctly(self):
        expected_content = [
            ["1", "1", "2000"],
            ["2", "1", "1500"],
            ["3", "5", "4000"],
            ["4", "6", "1000"],
        ]

        result = csv_from_file(path="{}/data/losses.csv".format(self.dir_path))
        self.assertEqual(self.losses_header, result[0])
        for _index, entry in enumerate(result[1:]):
            # EventId
            self.assertEqual(expected_content[_index][0], entry[0])
            # DealId
            self.assertEqual(expected_content[_index][1], entry[1])
            # Loss
            self.assertEqual(expected_content[_index][2], entry[2])
