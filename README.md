# django-tutorial-14th by Seungwoo Kim
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

