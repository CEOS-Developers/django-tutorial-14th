from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls/index.html')
#     context = {
#         'latest_question_list' : latest_question_list,
#     }
#     output = template.render(context, request)
#     return HttpResponse(output)

# def index(request):
#     url = 'polls/index.html'
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, url, context)

class IndexView(generic.ListView):
    # 어떤 템플릿에서 사용할 것인지
    template_name = 'polls/index.html'
    # 컨텍스트의 이름 설정
    context_object_name = 'latest_question_list'
    queryset = Question.objects.order_by('-pub_date')[:5]

    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    # 어떤 테이블에서 객체 리스트를 가져올지 정함
    model = Question
    # 어떤 템플릿을 사용할지 정함
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    url = 'polls/detail.html'
    question = get_object_or_404(Question, pk=question_id)
    context = {
        'question': question,
        'error_message': "You didn't select a choice.",
    }

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, url, context)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

#
# def results(request, question_id):
#     url = 'polls/results.html'
#     question = get_object_or_404(Question, pk=question_id)
#     context = {'question': question}
#     return render(request, url, context);
