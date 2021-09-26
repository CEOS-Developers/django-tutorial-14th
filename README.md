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

## SECRET_KEY ?
내 프로젝트 디렉토리 안에 `settings.py` 파일 안을 들여다 보면, `SERCRET_KEY`  라는 것이 존재한다. 이 값은 장고 보안 기능에 활용되는 값인데, [gitignore.io](https://www.toptal.com/developers/gitignore) 사이트에서 `.gitignore`을 생성해도 기본으로 처리해주지 않아서 따로 설정을 해주지 않으면 github나 기타 다른 저장소에 업로드하는 경우가 생긴다.
그렇게 되면 장고에서 제공해주는 멋진 보안 기능을 제대로 활용하지 못해버리게 된다. 나도 어제까진 이 점을 몰랐다.

[공식 문서](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-SECRET_KEY)를 먼저 들여다 보자.

_A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value._

_**django-admin startproject** automatically adds a randomly-generated **SECRET_KEY** to each new project._ 

뭐 그니까 대충 해석해보면 `cryptograhic signing`을 위해 사용 되는데 고유하고 랜덤한 값인데 내가 프로젝트를 시작할 때 자동으로 랜덤 키값을 하나 생성해준다고 한다.

그러면 이게 어디에 쓰이느냐?

>- All sessions if you are using any other session backend than django.contrib.sessions.backends.cache, or are using the default get_session_auth_hash().
- All messages if you are using CookieStorage or FallbackStorage.
- All PasswordResetView tokens.
- Any usage of cryptographic signing, unless a different key is provided.

그렇다고 한다. 솔직히 장고 입문자인데 이거 제대로 이해 못하겠다. 쓰다보면 알 것 같은데, 암튼 결론은 공개되면 안되는 아주 아주 중요한 키다!


### 이미 올려버렸다면?

프로젝트 초반이나, 복잡한 기능이 없는 프로젝트에서는 변경해도 괜찮다고 한다. 아마도 이런 실수를 중대한 프로젝트에서는 할 일이 없다고도, 하면 안된다고도 생각한다.

변경하는 방법은 여러가지가 있는데, 가장 간편한 방법은 [Django Secret Key Generator](https://djecrety.ir) 사이트를 이용하면 된다. 랜덤으로 임의의 50글자를 생성해준다. 만약 못미더우면 직접 코드를 만들어서 50글자 문자를 생성하면 된다.

## SECRET_KEY 분리하기

가장 중요한 분리하는 방법.

`settings.py` 파일 자체를 `.gitignore`에 추가하는 방법 말고, 세팅은 깃허브에 올리되 키값만을 분리하는 방법은 없을까?

다음과 같이 2가지 방법이 존재한다.

1. 환경 변수 패턴
2. 비밀 파일 패턴

환경변수는 리눅스 좀 만져봤으면 한번쯤은 접해봤을 `.zshrc`나 `.bash`등등 이런 파일에 키값을 추가해놓고, 코드에서 `import`하여 값을 불러오는 것이다.

나는 이 방법은 OS나 shell에 따라서 편집하는 파일이 달라지기 때문에, 별로 좋다고 생각하지 않는다. 고로 나는 비밀 파일 패턴을 사용할 것이다.

### 비밀 파일 패턴

이 방법은 `json`으로 키를 저장해 놓고 코드에서 값을 불러서 사용하는 것이다. 이 방식으로 해놓으면 웹서버에서도 적용이 가능하고, `.gitignore`에는 `.json`파일 하나만 넣어놓으면 된다.

```python
# secrets.json
{
  "SECRET_KEY": "본인의 고유 비밀 키 추가"
}
```

이렇게 json 파일을 세팅해주고,

```python
# settings.py
import os, json
from django.core.exceptions import ImproperlyConfigured


secret_file = os.path.join(BASE_DIR, 'secrets.json') # secrets.json 파일 위치를 명시

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

SECRET_KEY = get_secret("SECRET_KEY")
```
이렇게 적용해주면 된다. 여기서 주의할 점은 `os.path.join`안에 경로는 본인이 파일 구성을 어떻게 해놓느냐에 따라 조금 달라질 수 있었다. 나의 경우도 조금 달랐다. 이거는 알아서 수정하도록!

이렇게 세팅하고 terminal에서 `python3 manage.py runserver` 을 실행하니 정상적으로 작동하는 것을 볼 수 있었다.

## 참고 자료

[초보몽키의 개발공부로그](https://wayhome25.github.io/django/2017/07/11/django-settings-secret-key/)
[joeylee.log](https://velog.io/@jcinsh/Django-request-response)