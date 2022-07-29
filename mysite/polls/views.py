from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse


from .models import Choice, Question


def index(request):
    latest_quest_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_quest_list,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response =  'You\'re looking at the results of question'
    return HttpResponse(response , question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.all(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Alwas return HttpResponseRedirect after succesfully dealing with POST data, as
        # it prevents data being posted twice if back button is hit
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))