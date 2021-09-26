# [0919/1주차] Django Tutorial

---

# 스터디 자료 정리

## MVC 디자인 패턴?

> 어플리케이션을 Model, View, Controller로 나누어서 개발하는 방법론

- Model: 어플리케이션의 데이터를 표현, 처리하는 부분 (데이터베이스 테이블과 대응됨)
- View: 사용자에게 데이터를 출력하는 부분
- Controller: 사용자의 request에 따라 Model과 View를 업데이트하는 부분

## Django는 MTV 패턴

> 어플리케이션을 Model, Template, View로 나누어서 개발하는 방법론

- Model === MVC의 Model
- Template === MVC의 View
- View === MVC의 Controller

## Django Architecture

1. 클라이언트의 Request로부터 URL pattern을 분석함
2. URLconf는 URL 패턴에 따라 Request를 처리할 View를 선택함
3. View는 필요에 따라 Model을 통해 데이터를 처리하고 반환받음
4. View는 Model에서 받은 데이터를 바탕으로 Template을 Rendering
5. View가 클라이언트에게 Response로 렌더링한 Template을 보냄

---

# Django Tutorial part.1~part.4 따라가기

[Django 튜토리얼 문서](https://docs.djangoproject.com/ko/3.0/intro/)

## Part.1 프로젝트와 앱

### 프로젝트 만들기

```bash
# Django project 초기화
# 데이터베이스 설정, 장고 프로젝트와 어플리케이션 옵션 등을 자동으로 설정
>> django-admin startproject <project-name>
```

```bash
# 초기화된 프로젝트 디렉토리
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
```

- `manage.py` : 장고 프로젝트의 커맨드라인 유틸리티
- `__init__.py` : 파이썬에게 현재 디렉토리를 패키지처럼 다루라고 알려줌
- `settings.py` : 프로젝트의 설정
- `urls.py` : 프로젝트의 최상위 URLconf
- `asgi.py`, `wsgi.py` : ASGI/WSGI 호환 웹 서버의 entry-point

### 어플리케이션 만들기

```bash
# Django app 초기화 
>> py manage.py startapp <app-name>
```

```bash
# 초기화된 앱 디렉토리
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    urls.py
    views.py
    templates/ # templates 디렉토리는 수동으로 추가함
        polls/
```

- `admin.py` : 관리자 인터페이스 설정
- `apps.py` : 앱의 Configuration class(구성 클래스)
- `models.py` : 앱의 Model
- `urls.py` : 앱의 URLconf
- `views.py` : 앱의 View
- `templates/` : Django가 자동으로 템플릿을 탐색하는 디렉토리

프로젝트 vs 앱

프로젝트는 전체적인 웹사이트와 같고, 앱은 말그대로 사이트를 구성하는 어플리케이션과 같다. 하나의 프로젝트가 다수의 앱을 가질 수 있고, 앱 또한 다수의 프로젝트에서 사용될 수 있다. (다른 프로젝트에서 사용하기 위해 앱을 배포할 수 있음)

### 개발 서버 동작시키기

```bash
# development server 동작
>> py manage.py runserver
```

코드에 변화가 생기면 자동으로 서버가 재시작된다. 따라서 수동으로 서버를 재시작할 필요가 없다.

---

## Part.2 데이터베이스와 모델

### 데이터베이스 설치

파이썬은 [SQLite](https://sqlite.org/index.html) 라는 경량 데이터베이스를 기본적으로 가지고 있어서 대용량 데이터베이스가 필요한 것이 아니라면 별도로 설정할 필요없이 SQLite를 사용하면 된다.

Django의 구성요소(model, view, template)들은 서로 결합도가 낮다.
즉, 장고의 데이터베이스 API나 장고의 템플릿 시스템을 꼭 사용할 필요는 없다.

일부 앱은 사용하기 전에 미리 데이터베이스에 테이블을 생성해야 한다.

```bash
# 모델의 변화(models.py 파일의 변화)에 대한 마이그레이션 생성
>> py manage.py makemigrations

# 각 마이그레이션 파일을 데이터베이스에 적용
# 즉, DB에 모델과 대응되는 테이블을 생성함
# 변경된 모델과 데이터베이스의 스키마가 동기화됨
>> py manage.py migrate
```

> Migration은 모델의 변화(필드 추가, 모델 삭제 등)를 추적하는 vcs(버전 관리 시스템)와 같다.

`migrate`는 `INSTALLED_APPS` 설정을 바탕으로 필요한 데이터베이스 테이블을 생성한다.

- INSTALLED_APPS 설정:  현재 장고 프로젝트에서 활성화된 모든 장고 어플리케이션 목록
(`settings.py` 내에 존재함)

Schema??

스키마는 데이터베이스의 구조와 데이터의 구조, 표현 방법, 데이터 간의 관계를 정의한다. 
→ 데이터의 구조를 나타내는 청사진이다.

### Model 정의하기

> Model은 저장할 데이터의 필드와 동작을 나타낸다. 
따라서 각 모델은 하나의 데이터베이스 테이블과 매칭된다.

```python
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

각 모델은 클래스로 표현되며, django.db.models.Model의 서브클래스이다. 
각 필드는 Field 클래스의 인스턴스로 표현하고,
모델 끼리의 다대일 관계는 ForeignKey를 사용해 표현한다.

### Model 활성화하기

모델을 활성화하는 단계

1. 프로젝트에 앱 포함

    → 앱의 구성 클래스를 `INSTALLED_APPS` 설정에 추가
        (구성 클래스는 `apps.py` 내에 존재함)

2. 새 마이그레이션 생성 → `makemigrations`
3. 데이터베이스에 변경 사항 적용 → `migrate`

### 데이터베이스 API 사용하기

모델을 생성하면 장고는 자동으로 데이터베이스 스키마를 생성하고, 각 모델 객체에 접근하기 위한 python 데이터베이스 API를 생성한다. 파이썬 쉘에서 API 명령어들을 사용할 수 있다.

```bash
# 파이썬 쉘 진입
>> py manage.py shell
```

### 관리자 인터페이스에 모델 추가하기

모델이 정의되면 장고는 자동으로 관리자 인터페이스를 만든다.

관리자 인터페이스에서 데이터(object)를 추가, 변경, 삭제하려면 해당 모델을 `admin.py`에 추가해야 한다.

```python
from django.contrib import admin
from .models import Question

admin.site.register(Question)
```

---

## Part.3 뷰와 템플릿

### View 생성하기

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
```

각 뷰는 파이썬 함수(혹은 메소드)로 표현된다. 
뷰는 무조건 HttpResponse object를 반환하거나 Http404 예외를 발생시킨다.
(둘 중 하나는 무조건 실행해야 함) 
장고는 뷰를 통해 컨텐츠를 전달한다. 뷰는 파라미터에서 데이터를 받고, template을 로드하고, 받은 데이터를 이용해 template을 렌더링한다.

### URL과 View를 연결하기

URLconf(URL configuration)란 일치하는 뷰를 찾기 위한 url pattern들의 집합이다.

- 프로젝트의 root URLconf에서 하위 모듈(앱의 URLconf)을 연결

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

- 앱의 URLconf에서 뷰를 연결

```python
from django.urls import path
from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results')
]
```

`path()` 는 URL pattern과 callback function(View)을 연결한다.
route(url pattern), view, name을 인자로 받는다.

- name(view name 혹은 URL pattern name)은 템플릿 태그에서 해당 URL을 가리킬 때 사용된다.

요청된 url과 일치하는 route 중 가장 위에 있는 route의 view가 호출된다. (위에서부터 비교함)

view에는 request object와 url에 포함된 parameter가 전달된다.

### Template 만들기

Django는 자동으로 각 `INSTALLED_APPS` 디렉토리 내의 `templates/` 디렉토리에서 템플릿을 찾는다. 따라서 앱 디렉토리에 `templates/` 디렉토리를 생성하고 그 안에 뷰가 렌더링할 템플릿(html)을 작성한다.

`templates/` 디렉토리에 바로 템플릿을 두는 것은 추천하지 않는다. 해당 프로젝트의 다른 앱에 같은 이름을 가진 템플릿이 있다면 장고가 구분하지 못하기 때문이다. 따라서 앱과 같은 이름의 하위 디렉토리를 만들고 그 안에 템플릿을 두는 것이 좋다.

템플릿 태그와 필터 등을 이용해서 템플릿을 작성할 때 중복을 최대한 줄이는 것이 좋다.

변수는 `{{ var }}` 형태, 
태그는 `{% code %}` 형태 로 표현한다.

### Template과 View를 연결하기

```python
from django.http import HttpResponse
from django.template import loader
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```

템플릿을 불러오고, `context`를 전달하여 렌더링한 결과를 HttpResponse 객체와 함께 리턴한다.

`context`는 템플릿에서 쓰이는 변수명과 Python 객체를 연결하는 사전형 변수이다.

- `render()` 를 사용해 코드 줄이기

```python
from django.shortcuts import render
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
```

`render()`는 HttpResponse 객체를 리턴한다. 
따라서 `render()`를 사용하면 loader와 HttpResponse를 import하지 않아도 된다.

### View에서 Http404 예외 발생시키기

```python
from django.http import Http404
from django.shortcuts import render
from .models import Question

def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
```

객체(요청된 질문)가 존재할 때에만 템플릿을 렌더링하고, 존재하지 않을 경우 Http404 error를 발생시킨다.

- `get_object_or_404()` 를 사용해 코드 줄이기

```python
from django.shortcuts import get_object_or_404, render
from .models import Question

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})1
```

`get_object_or_404()` 는 인수로 Model과 키워드들을 받고, `get()` 함수에게 넘긴다.
객체가 존재하는 경우, 받아온 객체들을 반환한다.
객체가 존재하지 않는 경우, Http404 예외를 발생시킨다.

비슷한 동작을 하는 `get_list_or_404()` 함수는 `get()` 대신 `filter()` 를 사용한다.

### Template에서 하드코딩된 URL 제거하기

```html
<!-- 하드코딩된 부분 -->
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>

<!-- 수정 후 -->
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```

하드코딩된 `href` 를 `{% url %}` 템플릿 태그를 사용하여 수정하는 것이 좋다. 이때 `path()` 에서 정의한 view name이 사용된다.

하지만, 하나의 프로젝트에는 다수의 앱이 존재할 수 있다. 따라서 view name을 통해 URL을 구분할 때 다른 앱의 URL과 혼동될 수 있다.

⇒ URLconf에 namespace가 필요함

### URLconf에 namespace 설정하기

`urls.py` 에 `app_name` 을 추가하여 특정 어플리케이션의 URLconf에 namespace를 설정할 수 있다.

```html
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```

이제 템플릿에서 특정 namespace의 URL을 가리킬 수 있다.

---

## Part.4 Form과 Generic Views

### POST form 생성 시 주의점

내부 URL로 향하는 POST form을 생성할 때는 Cross Site Request Forgeries를 막기 위해 폼 내부에  `{% csrf_token %}` 태그를 사용해야 한다.

**Cross Site Request Forgeries??**

[CSRF](https://www.squarefree.com/securitytips/web-developers.html#CSRF) 는 악의적으로 클라이언트가 특정 서버에 request를 보내게 하는 것이다. 유저의 의도와 상관없이 유저의 쿠키 혹은 IP주소와 함께 다른 사이트에 request를 보내버린다.

### View에서 form 데이터 사용하기

- 데이터 접근

`request.POST` 와 `request.GET` 을 사용해 form에서 전송된 데이터에 접근할 수 있다. key를 이용해 사전형으로 접근하고, value는 문자열 형식으로 반환된다.

만약 존재하지 않는 데이터에 접근하면 KeyError가 발생한다. 따라서 예외 처리를 하는 것이 좋다.

- 데이터 처리 완료 후 주의점

POST data의 처리가 완료되면, 항상 HttpResponseRedirect 객체를 리턴해야 한다. 
(데이터가 중복 전송되는 것을 피하기 위함)

HttpResponseRedirect는 사용자가 이동할 url을 인수로 받는다.

- `reverse()` 를 사용해 URL 하드코딩 줄이기

> reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None)

`reverse()` 는 viewname을 가진 url과 args를 조합한 문자열을 반환한다.

Template에서 `{% url %}` 태그를 통해 하드코딩을 줄였던 것처럼 View에서는 `reverse()` 를 사용해 하드코딩을 줄일 수 있다.

### Generic View 사용하기

URL에서 전달된 매개 변수에 따라 데이터를 가져오고 템플릿을 렌더링하는 작업은 매우 일반적이다. 따라서 이런 일반적인 경우에는 Django가 제공하는 제너릭 뷰를 사용하는 것이 좋다.

1. URLconf

```python
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]
```

DetailView 제너릭 뷰는 기본적으로 URL parameter의 key 값을 `pk` 로 생각한다.

1. View

```python
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
```

사용할 Model과 context, template의 이름을 지정하면 제너릭 뷰가 만들어진다.

기본값은 다음과 같다.

- model: 당연히 필수로 지정해야 함
- context(context_object_name): `<model name>_list`
- template(template_name):
    - DetailView: `<app name>/<model name>_detail.html`
    - ListView:  `<app name>/<model name>_list.html`