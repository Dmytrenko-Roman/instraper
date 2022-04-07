import unittest

from scraper.instraper import Instraper

class TestInstraper(unittest.TestCase):
	def setUp(self) -> None:
		self.instraper = Instraper()

	def test_check_owner_location(self):
		self.assertEqual(self.instraper.check_owner_location('Kyiv'), False)

