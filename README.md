### **django-tutorial-14th**
​
---
​
#### **Part 1**
​
1\. 프로젝트 생성 및 실행
​
```
# mysite 프로젝트 생성
$ django-admin startproject mysite
# 설문조사 앱(polls) 생성
$ python manage.py startapp polls
# 서버 실행
$ python manage.py runserver
```
​
-   간단한 view 작성 후, 이 view를 호출하기 위한 URLconf를 생성 및 작성. 이후 최상위 URLconf(mysite/urls.py)에서 polls.url 모듈을 바라볼 수 있게 설정. -> 서버 실행해서 view 호출 확인.
​
\- include()
​
-   include() 함수는 다른 URLconf들을 참조할 수 있도록 도와준다. Django가 include() 를 만나면, URL의 앞 주소까지 일치하는 부분을 잘라내고, 남은 문자열 부분을 후속 처리를 위해 include 된 URLconf로 전달한다. 다른 url pattern을 포함할 때마다 항상 사용해야 한다.
​
```
    path('polls/', include('polls.urls'))
```
​
---
​
#### **Part 2**
​
1\. 모델 만들기
​
-   models.py 에 모델 작성. 데이터베이스의 각 필드(필드의 자료형)는 Field 클래스의 인스턴스로서 표현(CharField(max\_length=20), IntegerField 등). ForeignKey를 사용해 관계 설정 가능.
​
2\. 앱 추가
​
-   mysite/settings.py에 INSTALLED\_APP 리스트를 편집하여 앱을 현재 프로젝트에 포함시킬 수 있다.
​
3\. makemigrations -> migrate
​
```
# 변경사항에 대한 mirgations 생성
$ python manage.py makemigrations
​
# 적용되지 않은 migrations 수집 및 실행. -> 변경사항에 대한 데이터베이스 동기화
$ python manage.py migrate
```
​
※ python shell -> django api 동작 확인
​
-   모델에 \_\_str\_\_() 메소드를 추가. 이를 통해 shell에서 객체의 표현을 더 편하게 볼 수 있음. (또한 django가 자동으로 생성하는 관리사이트에서도 사용됨.) 
​
```
class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text
```
​
---
​
#### **Part 3**
​
1\. render()
​
```
 return HttpResponse(template.render(context, request))
 
 # shortcuts
 return render(request, 'polls/index.html', context)
```
​
-   render() 는 request 객체, 템플릿 이름, context 사전형 객체(optional)를 인수로 받아서 인수로 지정된 context로 표현된 템플릿의 HttpResponse 객체를 반환한다.
​
2\. get\_object\_or\_404()
​
```
try:
    question = Question.objects.get(pk=question_id)
except Question.DoesNotExist:
    raise Http404("Question does not exist")
​
# shortcuts
question = get_object_or_404(Question, pk=question_id)
```
​
3\. URL 변경
​
-   polls/index.html 템플릿에 다음과 같이 URL을 적으면, 수많은 템플릿을 가진 프로젝트들의 URL을 바꾸는 게 어려운 일이 된다. (하드코딩 문제)
​
```
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
```
​
\-> polls.urls 모듈의 path()에서 인수의 이름을 정의했으므로 **{% url %}** **template 태그를 사용하여 URL 설정에 정의된 특정 URL 경로들의 의존성을 제거**할 수 있다.
​
이 때, Django 프로젝트는 여러 앱을 가지고 있을 수 있으므로, **앱의 url을 구별하기 위해** URLconf에 이름공간(namespace)을 추가해 설정한다. -> **polls/urls.py 에 app\_name 추가**
​
```
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```
​
---
​
#### **Part 4**
​
**form으로 제출 된 데이터를 처리하고 데이터를 이용해서 vote()를 수행하는 view 작성.**
​
```
# polls/views.py
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 중략
    else:
        # 중략
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```
​
1\. request.POST 는 키로 전송된 자료에 접근할 수 있도록 해주는 사전과 같은 객체. request.POST\['choice'\]는 선택된 설문의 ID를 문자열로 반환해줌. (form에서 라디오버튼의 name을 choice, value를 choice.id로 설정 -> post data로 전송)
​
2\. reverse()
​
-   reverse()는 '/polls/3/results/'를 반환 -> results 페이지로 리다이렉트. view 함수에서 url을 하드코딩하지 않도록 해준다.
​
3\. Generic
​
-   model 속성을 이용하여 어떤 model이 적용될 것인지 제공한다.
​
1) ListView
​
-   default template name : < app name >/< model name >\_list.html. -> 특정 템플릿 이름을 사용하도록 하기위해 template\_name 속성 이용.
​
2) DetailView
​
-   default template name : < app name >/< model name >\_detail.html. -> 특정 템플릿 이름을 사용하도록 하기위해 template\_name 속성 이용.
-   DetailView 제너릭 뷰는 URL에서 캡쳐 된 기본 키 값이 pk라고 기대. -> URLconf의 question\_id를 제너릭 뷰를 위해 pk로 변경. 
​
```
# polls/views.py
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
```
​
```
# polls/urls.py
path('<int:pk>/', views.DetailView.as_view(), name='detail'),
path('<int:pk>/results/', views.ResultsView.as_view(), name='results')
```
