import unittest
from viewmodel.study_view_model import StudyViewModel
from model.objects.card import Card

class TestStudyViewModel(unittest.TestCase):

	def test_next_card(self):
		card = StudyViewModel.next_card(1, 1)
		self.assertTrue(isinstance(card, Card), card)


def main():
	unittest.main()

if __name__ == '__main__':
	main()