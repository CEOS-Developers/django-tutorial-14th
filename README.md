## HttpResponse

장고는 `request` 와 `response` 객체로 상태를 서버와 클라이언트가 주고 받는데, 아래와 같은 절차를 거친다.

1. 특정 페이지가 Request 되면, 장고는 메타데이터를 포함하는 `HttpRequset`객체를 생성한다.
2. 장고는 `urls.py`에서 정의한 특정 View 클래스/함수에 첫 번째 인자로 해당 `HttpRequest`객체를 전달.
3. 해당 View는 결과값을 `HttpResponse`나 `JsonResponse` 객체에 담아 전달.



이를 위해서 장고는 `django.http` 모듈에서 `HttpRequest`와 `HttpResponse` API 를 제공하는 것이다.

## Render

공식 문서를 따라가다 보면, 단축 기능이라면서 `Render`를 소개해 주는데, 이게 뭔지 자세히 살펴보자.

`Render`는 `HttpResponse` 객체를 반환하는 함수로,  `template`을 `context`와 엮어서 `HttpResponse`객체로 쉽게 반환해 주는 함수라고 한다.

이 함수의 기본형은 

```python
render(request(필수), template_name(필수), 
      context=None, content_type=None, 
      status=None, using=None)
```      
이렇게 되어 있다.
- template_name : 불러오고 싶은 템플릿 명을 적는다.  이전 함수에서 `loader.get_template()` 함수 안에 들어간 인자를 적으면 되는 것 같다.
- context : View에서 사용하던 변수(Dict 자료형)를 html 템플릿에서 전달하는 역할을 한다. `key`값이 템플릿에서 사용할 변수 이름, ` value`값이 파이썬 변수가 된다.

공식 문서에서 작성한 전체 코드를 보면서 비교해보자.


```python
from django.http import HttpResponse 

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

# 단축 기능 render.
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list' : latest_question_list}
    return render(request, 'polls/index.html',context)
```
위에가 템플릿, 아래가 렌더를 사용한 코드인데, 비교해보니까 어느 요소가 어디에 들어갔는지가 눈에 확 띄는 것 같다. 확실히 코드 길이를 줄여주는 듯.

### 참고 링크
[joeylee.log](https://velog.io/@jcinsh/Django-request-response)