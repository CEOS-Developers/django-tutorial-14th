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

***
## Part 3

***
## Part 4

