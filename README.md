# django-tutorial-14th
***
## Part 1
### 프로젝트 생성 및 앱 생성
```
$ django-admin startproject mysite      # 프로젝트 폴더 내에 파일 생성
$ django-admin startproject mysite .    # 현재 위치에 파일 생성
$ python manage.py startapp polls
```
###디렉토리 구조
```
mysite/         # 프로젝트 폴더
    mysite/     # 프로젝트에 관련된 파일들
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
    polls/      # 생성한 앱
        __init__.py
        admin.py
        apps.py
        migrations/
            __init__.py
        models.py
        tests.py
        views.py
    manage.py
```
### 서버 실행
```
$ python manage.py runserver        # 기본포트는 8000번
$ python manage.py runserver 8080   # 포트 설정 가능
```

### url 패턴 관리
```
# polls/urls.py
urlpatterns = [
    path('', views.index, name='index'),
]
# mysite/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
]
```
http://127.0.0.1:8000/polls 입력하면 views.index 함수 실행   
include 함수를 통해 polls 이후의 url 패턴은 polls/urls.py 에서 매칭   
url에 name 인수를 부여하여 name만으로 참조할 수 있도록 설계

***

## Part 2
- 장고에서 Model 사용법
  - Model 작성. _필드, 메서드 등등_
  - 변경사항을 migration 파일로 저장 _python manage.py makemigrations_
  - migration 파일 실행 _python manage.py migrate_


- Question Model
```
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def  __str__(self):     # 객체를 표현하는 정보
        return self.question_text

    def was_published_recently(self):   # 커스텀 메서드
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
```
- Choice Model
```
class Choice(models.Model):
    # 하나의 Choice 당 하나의 Question 연결. ForeignKey 사용
    # on_delete=models.CASCADE => 연결된 Question 객체 삭제 시 Choice 객체도 삭제
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
```
***
## Part 3
### Django에서 view 함수의 반환값
- `HttpResponse(data, content_type)` response를 반환하는 기본적인 함수
- `render(request, template_name, 
context=None, content_type=None, status=None, using=None)` template을 context와 엮어 httpResponse 를 반환
- `redirect(to, permanent=False, *args, **kwargs)` url name을 주로 사용
- `JsonResponse(data, encoder=DjangoJSONEncoder,
             safe=True, json_dumps_params=None, 
             **kwargs)` response를 커스텀해서 사용하고 싶을 때, 프론트엔드 개발자와 협의된 형식으로 메시지를 구성

### HTML 소스에서 url 하드코딩 방지
```html
<a href="{% url 'detail' question.id %}">{{ question.question_text }}</a>
'poll'이라는 namespace 사용
<a href="{% url 'poll:detail' question.id %}">{{ question.question_text }}</a>
```
***
## Part 4
### 장고에서 폼(form) 사용하기
- 폼에 데이터를 담아서 POST 메서드로 전송
- request.POST['key']로 원하는 정보 추출
- 데이터베이스에 적용

### 제너릭 뷰
장고에서 제공하는 일반적인 뷰 함수 => 짧은 코드 작성 가능

