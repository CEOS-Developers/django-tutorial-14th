# Part 1

### 프로젝트 생성과 실행

```bash
# 프로젝트 생성
django-admin startproject mysite
```

프로젝트를 위한 `route` 관리를 위한 디렉토리, `db`를 위한 모델 정의 파일, 앱 엔트리파일 등을 자동으로 생성한다.

```bash
# 서버 실행
python manage.py runserver
```
실행 시 기본 포트는 8000, 만약 포트를 3000으로 변경하고 싶다면
```bash
# change port 3000
python manage.py runserver 3000
```

### route 생성과 등록
```bash
# manage.py가 있는 디렉토리에서 실행.
python manage.py startapp polls
```
위에서 생성한 `directory` 내에서 `view`를 만들고,<br>
`/urls.py`에서 `import` 후 `url` 연결. (호출 준비 완료)

최상위 `URLconf` 에서 방금 만든 `polls.urls` 모듈을 바라보게 설정해야 한다.<br>
`include`로 참조하여 `path()` 인자로 넘겨준다.<br>
`path()`에는 `route`, `view`를 필수 인자로 넘겨준다. 

정리하자면, `view` 생성 -> `url`연결 `(import)` -> 최상위 `URLconf`에 등록

# Part2

### 환경변수 세팅

프로젝트 세팅은 `settings.py`에서 한다.<br>
`BASE_DIR`, `SECRET_KEY` 등 프로젝트 `config`를 할 수 있다.

### Db 모델링

```bash
# 변경사항에 대한 마이그레이션을 생성
python manage.py makemigration

# 변경사항을 데이터베이스에 적용.
python manage.py migrate
```
Flask-sqlAlchemy에서도 동일하게 사용되는데,<br> 
git commit 과 push의 느낌..? 으로 이해했었다.

### shell에서의 Api 테스트

```shell
# 실행
python manage.py shell
# 종료
quit()
```
### 기본적으로 제공하는 메소드들 정리

```python
# Method Example
from polls.models import Choice, Question
Question.objects.all()
Question.objects.filter(question_text__startswith='What')
q = Question.objects.get(pk=1) # pk - primary key
q.was_published_recently() #직접 정의한 메소드 호출
```

ORM이라서 역시 쿼리문을 몰라도 db에 접근을 다 할 수 있다. <br>
직접 쿼리문을 작성해서 쓰고 싶다면 그것 또한 지원이 된다.<br>
[참고](https://docs.djangoproject.com/en/3.2/topics/db/sql/)

```python
q.choice_set.create(choice_text='Not much', votes=0)
q.choice_set.create(choice_text='The sky', votes=0)
c = q.choice_set.create(choice_text='Just hacking again', votes=0)
q.choice_set.all() #q에 속한 모든 choice를 볼 수 있다
Choice.objects.filter(question__pub_date__year=2021)
```

### 관리자 계정 만들기

```shell
# 관리자 계정 생성
python manage.py createsuperuser
```
![admin create](/Users/nowkim/Dev/ceosBack/django-tutorial-14th/images/1.png)
password를 password라고 쳤더니 너무 흔하다고 한다. (이런 detail을 보면 너무 귀엽다)
그래도 그냥 만들거냐고 묻는데 테스트니까 그냥 만든다.

# Part3

### route에 view 등록하기

이전과 동일하게 views.py에 새로운 view들을 등록해주고, 인수를 받아서 question_id에 저장해준다.
parameter, view, name을 path로 넘겨주고, 경로를 지정해준다.

![html붙이지마](/Users/nowkim/Dev/ceosBack/django-tutorial-14th/images/2.png)
...그렇다고 하네요
`view`가 하는 일은 두 가지라고 한다.
 - HttpResponse 객체 반환
 - 예외 처리

### 일반적인 상황에서 view return하기

두 가지 방법으로 context를 리턴할 수 있다.
- 직접 html 파일을 template으로 받아서 리턴
- render() 사용.

render()이 더 편한 것 같다.
```python
from django.shortcuts import render

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
```

### 404 error일 경우 return하기

역시 두 가지가 존재한다.

- 요청한 id가 없을 경우
- 객체가 없을 경우.

이것도 후자가 더 편하다.

```python
from django.shortcuts import get_object_or_404, render

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```

### Url의 namespace 사용하기

프로젝트 구분을 위해 namespace를 사용한다.

→ 그냥 그럼 하드코딩하면 되지 않나요?<br>
→ 그럼 유지보수가 힘들어집니다<br>
**→ 똑같이 변수명으로 쓰되, namespace로 한정지어주자.**

# Part 4

### Post method 구현

```python
# selected_choice 객체에 choice테이블 join한 값 저장
question = get_object_or_404(Question, pk=question_id)

try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
except (KeyError, Choice.DoesNotExist):
    # Redisplay the question voting form.
    return render(request, 'polls/detail.html', {
        'question': question,
        'error_message': "You didn't select a choice.",
    })
else:
    selected_choice.votes += 1
    selected_choice.save()
```

Django는 GET도 있지만,<br>
POST 요청을 통해서만 자료가 수정되도록 하기 위해서<br>
명시적으로 코드에 `request.POST`를 사용하고 있다.

### generic view 사용하기

`generic view`는 `django`에서 제공하는 `view template`이라고 생각하면 된다.

개발 속도를 빠르게 할 수 있는 장점이 있다.

주의사항: `generic view`를 위해서는 매개변수 이름이 `pk`여야 한다.
