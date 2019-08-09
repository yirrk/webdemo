from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
# from django.template import loader
from .models import Question, Choice
# from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    """docstring for IndexView"""
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        ''' 返回最新的5个问卷 '''
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
        """docstring for DetailView"""
        model = Question
        template_name = 'polls/detail.html'

        def get_queryset(self):
            '''
            只提取已发表问卷
            '''
            return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """docstring for ResultsView"""
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        '''
        只提取已发表问卷
        '''
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 没有选择任何选项，返回问卷页
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "还没有选择任何选项",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 为了防止用户提交数据后，单机浏览器后退按钮重新提交数据
        # 必须使用HttpResponseRedirect 方法进行页面跳转
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))