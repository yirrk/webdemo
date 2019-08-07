from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from .models import Question, Choice
from django.http import Http404
from django.urls import reverse


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
# template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
        }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    '''try:
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise Http404("问卷不存在")'''
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    return HttpResponse("请为问卷 %s 提交您的答案" % question_id)


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