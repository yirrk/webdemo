from django.test import TestCase
import datetiome
from django.utils import timezone
from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        '''
        当问卷发布是未来某天时，was_published_recently()会返回False
        '''
        time = timezone.now() + datetiome.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)