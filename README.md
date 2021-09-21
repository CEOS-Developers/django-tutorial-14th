# django-tutorial-14th by Seungwoo Kim
이 문서는 [장고 튜토리얼]("https://docs.djangoproject.com/ko/3.0/intro/tutorial01/") 을 진행하며 새로 알게 된 내용을 정리하기 위함입니다.
# Part 1
## 초기 프로젝트 디렉토리 생성
- ```django-admin startproject mysite```라는 커맨드를 통해 프로젝트의 뼈대를 만든다.
- React의 npx create-react-app와 비슷하다.
- 패키지 관리, route 관리에 대한 디렉토리와 서버 앱 엔트리파일이 보인다.
## Route 연결 방법
- ```python manage.py startapp polls``` 라는 커맨드를 통해 개발 할 앱의 구조를 생성한다.
- polls/views.py에 HttpReponse 메소드를 이용해 뷰를 생성한다.
- URLconf를 통해 뷰를 URL에 이어줘야하는데, polls 내부에 urls.py를 생성한다.
- 생성한 polls.urls을 최상단 URLconf에서 호출하는 방식을 사용한다.
# Part 2
## 환경변수 관리
- mysite/settings.py에서 관리한다.
- default db는 SQLite 이다.
## 모델 생성/변경
- (models.py 에서) 모델을 변경한다.
- ```python manage.py makemigrations```을 통해 이 변경사항에 대한 마이그레이션을 생성.
- ```python manage.py migrate``` 명령을 통해 변경사항을 데이터베이스에 적용.
## 모델 내 __str__() 메소드
왜 이 메소드를 선언할까?
- 대화식 프롬프트에서 필드값에 손쉽게 접근하려고 만든다.
- Django가 자동 생성하는 관리 사이트에서 객체의 표현으로 사용된다.
- Flask sql-alchemy와 같은 방법론으로 보인다. 내부적으로 인스턴스의 정보 표현을 용이하게 한다.
## 손쉬운 테이블 핸들링 / 관계 파악
```python manage.py shell``` 스크립트로 대화식 프롬프트로 접근하여 다루면 편하다. <br>
import한 테이블에 대해 기본적으로 제공하는 메소드가 몇가지 있다. 아래와 같은 방식으로 데이터를 필터링 할 수 있다.
```python
# Method Example
Question.objects.all()
Question.objects.filter(id=1)
Question.objects.filter(question_text__startswith='What')
q = Question.objects.get(pk=1)
q.was_published_recently() #직접 정의한 메소드 호출
```
참조 관계가 있는 테이블 데이터를 손쉽게 생성할 수 있다. 
또한 JOIN Query문으로 데이터를 참조하듯, "__"(double underscores)로 관계를 분리해 참조할 수 있다.
뿐만 아니라 이를 이용해 참조한 모델에 정의된 메소드까지 쓸 수 있다.
```python
# Method Example
q.choice_set.create(choice_text='Not much', votes=0)
q.choice_set.create(choice_text='The sky', votes=0)
c = q.choice_set.create(choice_text='Just hacking again', votes=0)
q.choice_set.all() #q에 속한 모든 choice를 볼 수 있다
Choice.objects.filter(question__pub_date__year=2021) #pub_date가 2021년 choice 조회
```

# Part 3
View에 대한 렌더링을 어떻게 하며, 각 view에 대한 url을 어떻게 연결하는지 나와있다.
## View에 대응하는 Route 연결 구체적 방법 
위에서 진행했듯이 최상단 URL관리 파일(mysite/urls.py)에 polls/url.py가 등록된 상황이다.
그렇다면 polls/url.py에는 **/polls/** 하위에 등록되는 url을 정의해줘야한다.
아래는 다양한 형태의 url 등록에 대한 예시이다.
```python
# polls/urls.py
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
# Notice! 두번째 인자인 views.~는 views.py 에 함수 형태로 정의된 view 이다.
```
## 비즈니스 로직 작성하기 -> Shortcut으로!
view 함수의 return 부분을 보면 HttpResponse로 보여질 view를 렌더링 했다.
이 곳에 template.render 메소드를 인자로 넘겨주면 .html 파일을 렌더링 할 수 있다.
이 때, html파일은 **polls/templates/polls/index.html**와 같은 구조에 선언한다.<br>
위와 같은 논리를 반영하면 다음과 같은 코드로 작성된다.
```python
# 리팩토링 이전의 비즈니스 로직 작성법
# polls/views.py
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```
그런데 코드가 길어지고 조금 귀찮으니까 **render** 메소드를 쓰자. 훨씬 직관적이고 쉽다.
```python
# 리팩토링 이후의 비즈니스 로직 작성법
# polls/views.py
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

# 아래는 예외처리에 대한 shortcut 작성법이다. (try-catch 구문 쓸 필요 없음)
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```
## Namespace로 프로젝트 구분을 하자
Template 파일(View html 파일)에서 url 값을 하드코딩하지 않고, polls.urls 파일에 명시된 url 명칭을
불러오는 방식으로 간략하게 쓸 수 있다. 하지만, 프로젝트가 커지면 Template 입장에선 어떤 프로젝트의 url name인지
구분하기 힘든 문제가 있다(~~~.urls 에서 ~~~은 뭐지?). 따라서 최상단 route에 대한 namespace를 달아주어 이를
해결할 수 있다.