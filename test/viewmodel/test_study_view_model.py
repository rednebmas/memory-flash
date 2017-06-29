import unittest
from viewmodel.study_view_model import StudyViewModel
from model.objects.card import Card

class TestStudyViewModel(unittest.TestCase):

	def test_next_card(self):
		user_id = 1
		card, session = StudyViewModel.next_card(user_id, 1, 1)
		self.assertTrue(isinstance(card, Card), card)


def main():
	unittest.main()

if __name__ == '__main__':
	main()