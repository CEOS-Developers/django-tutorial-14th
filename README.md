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

***
## Part 4

