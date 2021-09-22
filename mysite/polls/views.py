from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import path, reverse
from django.views import generic
from django.template import loader
from . import views
from .models import Question,Choice


# Create your views here.

# 제너릭 뷰 사용하기.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_qeustion_list'

    def get_queryset(self):
        # Return the last five published questions
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'



# 제너릭 뷰 사용 안한 코드. vote는 동일하게 제너릭 뷰에서도 사용한다.
def index(request):
    """
    // 템플릿을 이용한 뷰 업데이트.
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
    """

    # 단축 기능 render.
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list' : latest_question_list}
    return render(request, 'polls/index.html',context)

def detail(request, question_id):
    """
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not Exist")    # 404 에러 일으키기
    return render(request, 'polls/detail.html', {'question' : question})
    """
    ### 객체가 존재하지 않을 때 get()을 사용하여 Http404 예외를 발생시키는 단축 기능.
    question = get_object_or_404(Question,pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})


def results(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message' : "You didn't select a choice."
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        # 성공했을 때만 HttpResponseRedirect 리턴.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


