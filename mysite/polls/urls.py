from django.urls import path
from . import views

app_name = 'polls'   # 어플리케이션의 이름공간 설정.


## 제너릭 뷰 사용하기.

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote', views.vote, name='vote'),
]

"""
urlpatterns = [
    # /polls/
    path('', views.index, name='index'),
    # /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # add the word 'specifics'
    # URL을 바꾸고 싶으면 템플릿이 아니라 여기서 바꿔야 한다.
    path('specifics/<int:question_id>/', views.detail, name='detail'),
    # /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
"""