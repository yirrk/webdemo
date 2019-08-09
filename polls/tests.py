from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.urls import reverse


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        '''
        当问卷发布是未来某天时，was_published_recently()应当返回False
        '''
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        '''
        当发布时间比前一天还早一秒, was_published_recently()应当返回False
        '''
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        '''
        当发布时间比前一天晚一秒, was_published_recently()应当返回True
        '''
        time = timezone.now() - datetime.timedelta(hours=23, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    '''
        使用指定的文本和日期数量创建问卷
        如果日期数量是负数表示发布时间早于当前时间，正数则表示发布时间晚于当前时间
    '''
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        '''
         如果系统当前没有符合条件的问卷则返回提示信息
         '''
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u"还没有调查问卷! ")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        '''
        早于当前时间发表的问卷将被显示在index页面
        '''
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                                 ['<Question: Past question.>'])

    def test_future_question(self):
        '''
        晚于当前时间发表的问卷将不会被显示在首页
        '''
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, u'还没有调查问卷！ ')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        '''
        系统同时存在已发表和未发表问卷，只显示已发表问卷
        '''
        create_question(question_text='Past question.', days=-30)
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                                 ['<Question: Past question.>'])

    def test_two_past_question(self):
        '''
        index页面可以同时显示多个问卷
        '''
        create_question(question_text="Past question 1.",  days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>'])

class QuestionDetailViewTests(TestCase):
    """docstring for QuestionDetailViewTests"""
    def test_future_question(self):
        """
        如果被查询问卷还没发表则返回404
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self. assertEqual(response.status_code, 404)

    def test_past_question(self):
        '''
        如果被查询问卷已经发表了则 返回问卷内容
        '''
        past_question = create_question(question_text="Past question.", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTests(TestCase):
    """docstring for QuestionResultsViewTests"""
    def test_future_question(self):
        """
        如果被查询问卷还没发表则返回404
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse('polls:results', args=(future_question.id,))
        response = self.client.get(url)
        self. assertEqual(response.status_code, 404)

    def test_past_question(self):
        '''
        如果被查询问卷已经发表了则 返回问卷内容
        '''
        past_question = create_question(question_text="Past question.", days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
