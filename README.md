# 1주차 
## 프로젝트 폴더 구조
```
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
    polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

`Django`는 최상위 폴더의 ***manage.py*** 파일을 이용하여 서버를 관리한다.

#### 기본 app 만들기
```shell
$ python manage.py startapp polls
```

#### 개발서버 띄우기
```shell
$ python manage.py runserver {portnumber}
```

## Secret Key
`setting.py` 에는 secret key가 존재한다.  
이를 public한 저장소에 커밋하게 되면 보안적인 이슈가 발생할 수 있으므로, json 파일에 변수로 설정하고 불러들이는 방법을 사용할 수 있다.
```gitignore
# Secret Key
secrets.json
```
먼저 secret키를 Json 변수로 담은 파일을 예외처리 해주어야 한다.

```json
{
  "SECRET_KEY" : "b_4(!id8ro!1645n@ub55555hbu93gaia0 {my_secret_key}"
}
```
다음과 같이 json 파일을 만들어준다.

```python
# mysite/settings.py

# before
SECRET_KEY = {my_secret_key}

# after
import os, json
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

secret_file = os.path.join(BASE_DIR, 'mysite', 'secrets.json')

with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")
```
`settings.py`의 SECRET_KEY 부분을 다음과 같이 수정해준다.  
secret_file의 경로에 'mysite'를 넣어주었는데, 절대경로로 만들고 싶은데 아직 파이썬이 익숙치않아서 모르겠다.

## URLConf
```python
# mysite/urls.py
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

`mysite/urls.py` 의 *urlpatterns* 가 다음과 같이 작성되어있고, url이 *'/polls/3/results/'* 인 요청이 들어왔다면   
`mysite/urls.py` 에서 먼저 받은 뒤, URL의 **/polls/** 부분을 잘라낸 *'/3/results/* url을 `polls/urls.py` 로 맵핑할 것이다.  

개인적으로 `Spring`에서의 Annotation을 이용한 controller 설정이 좀 더 편한 것 같다.

## Generic view

제너릭뷰란? `Django `에서 기본적으로 제공하는 View Class를 말한다.

### 제너릭뷰의 종류
<details>
<summary>Base View</summary>
<div markdown="1">
View : 가장 기본이 되는 최상위 제네릭 뷰  

TemplateView : 템플릿이 주어지면 해당 템플릿을 렌더링한다.  

RedirectView : URL이 주어지면 해당 URL로 리다이렉트 시켜준다.
</div>
</details>

<details>
<summary>Generic Display View</summary>
<div markdown="1">
DetailView : 객체 하나에 대한 상세한 정보를 보여준다.  

ListView : 조건에 맞는 여러 개의 객체를 보여준다.
</div>
</details>

<details>
<summary>Generic Edit View</summary>
<div markdown="1">
FormView : 폼이 주어지면 해당 폼을 보여준다.  

CreateView : 객체를 생성하는 폼을 보여준다.  

UpdateView : 기존 객체를 수정하는 폼을 보여준다.  

DeleteView : 기존 객체를 삭제하는 폼을 보여준다.  

</div>
</details>

<details>
<summary>Generic Date View</summary>
<div markdown="1">
YearArchiveView: 년도가 주어지면 그 년도에 해당하는 객체를 보여준다.  

MonthArchiveView: 월이 주어지면 그 월에 해당하는 객체를 보여준다.  

DayArchiveView: 날짜가 주어지면 그 날짜에 해당하는 객체를 보여준다.
</div>
</details>  


### 제너릭뷰가 적용되지 않은 코드
```python
# polls/views.py
from .models import Question
from django.shortcuts import render


def index(request):
    url = 'polls/index.html'
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, url, context)
```

### 제너릭뷰가 적용된 코드

```python
# polls/urls.py
from django.urls import path
from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
```
`Primary Key` 값을 `URLconf`에서 추출한다. 

```python
# polls/views.py
from .models import Question
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
```



*django.views.generic.list* 내부 클래스 *MultipleObjectMixin* 의 메서드인 **get_queryset()** 을 오버라이딩 하여서 사용하였다.  

**get_queryset()** 의 경우 `request`가 들어올 때마다 동작하므로, 리턴 값이 동적일 경우(ex 시간) 잘못된 결과가 반환될 수 있으므로, 이 땐 **queryset** 을 사용하여야 한다.

### queryset을 적용한 코드
```python
# polls/views.py
from .models import Question
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    queryset = Question.objects.order_by('-pub_date')[:5]

    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     return Question.objects.order_by('-pub_date')[:5]
```

또한 `제너릭 뷰`는 CBV(Class Based View)를 사용하므로 코드 양을 줄일 수 있다.

## Model

각각의 `모델`은 하나의 데이터베이스 테이블에 맵핑된다.  
`모델`은 저장하고 있는 필수적인 필드와 동작등을 포함하고 있다.

`Django`는 기본적으로 컴포넌트의 재사용성과 플러그인화 가능성, 빠른 개발을 강조하는 `DRY`(Don't Repeat Yourself) 원칙을 따른다.

### Migration
`모델`의 변경사항을 반영하는 `Django`의 방법

```shell
$ python manage.py makemigrations
```
`polls/migrations` 경로에 `0001_initial.py`가 생성된다.  
`models.py`의 변경이나 추가 혹은 삭제 사항들을 감지하여 파일로 만들어 준다.

```shell
$ python manage.py migrate
```
적용되지 않은 설정값들을 적용시키는 명령어이다.

### Foreign Key 설정
```python
# polls/models.py
import datetime

from django.db import models
from django.utils import timezone


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
```

`Foreign Key`는 다음과 같이 설정하였다.  
Question과 Choice 두 모델은 `One to Many` 관계로 맵핑되어야 하는데, Many쪽에 `Foreign Key`를 설정한 것을 볼 수 있다.  

`on_delete` 설정을 `CASCADE` 로 설정하였다.  

이 설정은 어떤 question1을 `Foreign Key`로 설정한 choiceA가 존재할 때,
question1이 삭제된다면, choiceA도 삭제되게 만든다.  

개인적으로 `Django`의 ORM 사용법이 `Spring`의 JPA보다 간단하게 느껴진다.