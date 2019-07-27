from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Welcome!This is an online vote system!")


def detail(request, question_id):
    return HttpResponse("将为您打开问卷 %s" % question_id)


def results(request, question_id):
    response = "正在查看问卷 %s 的结果。"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("请为问卷 %s 提交您的答案" % question_id)