import unittest

from instraper import Instraper

class TestInstraper(unittest.TestCase):
	def setUp(self) -> None:
		self.instraper = Instraper()

	def test_check_owner_location(self):
		self.assertEqual(self.instraper.check_owner_location('Kyiv'), True)
		self.assertEqual(self.instraper.check_owner_location('Lviv'), True)
		self.assertEqual(self.instraper.check_owner_location('Moscow'), False)
		self.assertEqual(self.instraper.check_owner_location('Vinnytsia'), True)
		self.assertEqual(self.instraper.check_owner_location('Rowne'), True)
