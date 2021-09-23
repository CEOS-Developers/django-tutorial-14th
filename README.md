# django-tutorial-14th
CEOS 14기 백엔드 1주차 과제: Django tutorial Part 1 - Part 4

## Part 1
### Django 설치 확인
```bash
python -m django --version
```
내가 쓰고 있는 컴퓨터의 경우 `python` 명령으로만 파이썬을 실행하면 이전 버전이 실행되었다. 프로젝트를 위해 만든 가상환경으로 실행하기 위해서는 `python3` 으로 파이썬을 실행시켜 주어야 했다. 

### 프로젝트 생성 
```bash
django-admin startproject mysite
```
- manage.py: Django 프로젝트와 다양한 방법으로 상호작용 하는 커맨드라인의 유틸리티
- mysite/settings.py: 현재 Django 프로젝트의 환경 및 구성을 저장
- mysite/urls.py: 현재 Django project 의 URL 선언을 저장

### 개발 서버
```bash
python manage.py runserver
```

### 설문조사 앱 만들기
```bash
python manage.py startapp polls
```

### 첫 번째 뷰 작성하기
- URLconf: 뷰를 호출하려면 이와 연결된 URL이 존재해야하는데 이를 설정해 주기 위한 것
- polls/urls.py: polls 에서 URLconf를 생성하기 위해 만들어 줘야 하는 파일
- django.urls의 include()

## Part 2
### 데이터베이스 설치
- Django 기본 세팅은 SQLite 이지만 `mysite/settings.py` 파일 변경 통해 PostgreSQL 등 다른 데이터베이스로 변경 가능
- mysite/settings.py의 TIME_ZONE: 기본값에서 서울의 시간대 `Asia/Seoul`로 변경
```bash
python manage.py migrate
```
기본 어플리케이션들의 데이터베이스 테이블 생성

### 모델 만들기
- 모델(model): 데이터의 필수적인 필드들과 동작들을 포함(Django의 모델은 [DRY 원칙](https://docs.djangoproject.com/ko/3.0/misc/design-philosophies/#dry) 을 따름) 
- `polls/models.py`에 모델 생성
- 데이터베이스의 각 필드는 Field 클래스의 인스턴스로서 표현됨
  - CharField: 문자(character) 필드 표현
  - DateTimeField: 날짜와 시간(datetime) 필드 표현
  - ForeignKey: 관계 설정

### 모델의 활성화
- 모델을 활성화 시켜주기 위해서 `mysite/settings.py`의 `INSTALLED_APPS`에 'polls.apps.PollsConfig' 추가
```bash
python manage.py makemigrations polls 
```
모델의 변경사항을 migration으로 저장
```bash
python manage.py migrate 
```
데이터베이스에 모델과 관련된 테이블을 생성

### API 가지고 놀기
```bash
python manage.py shell
```
interactive 파이썬 shell 실행, shell 내에서 모델의 객체를 만들어 저장
- 모델에 `__str__()` 메서드를 추가하여 QuerySet 등이 객체를 반환할 때 각 객체의 인식을 조금 더 쉽게 할 수 있도록 설정

### Django 관리자 소개
```bash
python manage.py createsuperuser
```
아이디, 이메일, 비밀번호를 설정하여 관리자(superuser) 생성
- `polls/admin.py`에 `admin.site.register()`를 이용하여 admin 페이지에 모델 등록

## Part 3
### 뷰 추가하기
- 뷰: Django 어플리케이션이 일반적으로 특정 기능과 템플릿을 제공하는 웹페이지의 한 종류
- `polls/views.py`에 인수를 받는 뷰들을 추가하고, 새로운 뷰를 polls.urls 모듈로 `polls/urls.py`에 연결

### 뷰가 실제로 뭔가를 하도록 만들기
- 각 뷰는 요청된 페이지의 내용이 담긴 HttpResponse 객체를 반환하거나, 혹은 Http404 같은 예외를 발생하게 하는 두 가지 중 하나는 해야함
- `polls/templates/polls/index.html` 파일을 작성, 템플릿을 이용하여 뷰와 페이지 디자인을 분리함
- 뷰에서 `HttpResponse(template.render(context, request))` 또는 `render(request, 'polls/index.html', context)` 를 사용하여 템플릿을 렌더링

### 404 에러 일으키기
try, except, raise, Http404 또는 `get_object_or_404()`를 사용하여 예외 처리

### 템플릿 시스템 사용하기, 템플릿에서 하드코딩된 URL 제거하기
- 태그: `{% %}` 사용, 렌더링 프로세스의 로직을 처리함
- 변수: `{{ }}` 사용, 전달받은 context로 부터 값을 출력
- 주석: `{# #}` 사용, 주석은 렌더 되지 않음

### URL의 이름공간 정하기
- `polls/urls.py` 파일에 `app_name`을 추가해 어플리케이션의 이름공간(namespace) 설정 가능

## Part 4
### Write a minimal form
- `polls/templates/polls/detail.html`에 HTML <form> 요소를 적용
- `polls/views.py`에 vote 함수 구현
- request.POST: 키로 전송된 자료에 접근할 수 있도록 해주는 dictionary-like 객체

### 제너릭 뷰 사용하기
- 제너릭 뷰: URL에서 전달 된 매개 변수에 따라 데이터베이스에서 데이터를 가져 오는 것과 템플릿을 로드하고 렌더링 된 템플릿을 리턴하는, 기본 웹 개발의 매우 일반적인 경우를 위해 Django가 제공하는 시스템
- ListView: 개체 목록 표시 개념이 추상화된 제너릭 뷰, <app name>/<model name>_list.html 템플릿을 기본으로 사용
- DetailView: 특정 개체 유형에 대한 세부 정보 페이지 표시 개념이 추상화된 제너릭 뷰, 기본적으로 <app name>/<model name>_detail.html 템플릿을 사용
- 각 제너릭 뷰가 기본으로 사용하는 템플릿을 `template_name` 속성을 통해 override 할 수 있음
