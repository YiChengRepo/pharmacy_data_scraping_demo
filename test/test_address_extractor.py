from unittest import TestCase
from bc_pharmacy_ds import address_data_extrator

class TestAddress_extractor(TestCase):
    def test_valid_case(self):
        text1 = '105 - 1450 Waddington Rd Nanaimo, BC  V9S 4V9 CANADA'
        result = address_data_extrator.address_extractor(text1)
        self.assertEqual(result, "BC  V9S 4V9 CANADA")

    def test_valid_case2(self):
        text1 = 'Satnam Plaza 115 - 7130 120 St Surrey, BC V3W 3M8 CANADA'
        result = address_data_extrator.address_extractor(text1)
        self.assertEqual(result, "BC V3W 3M8 CANADA")

    def test_invalid_case(self):
        text1 = 'Satnam Plaza 115 - 7130 120 St Surrey, BC V3W CANADA'
        result = address_data_extrator.address_extractor(text1)
        self.assertEqual(result, "")

if __name__ == '__main__':
    unittest.main()
