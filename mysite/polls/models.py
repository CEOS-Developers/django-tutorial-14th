import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # toString하고 같은 역할
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    # 객체에 직접 접근하는 것 보다 함수 콜이 더 낫지 않을까 해서 추가해보았다.
    def when_published(self):
        return self.pub_date


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    # pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.choice_text

# database model 정의
# django는 DRY(Don't Repeat Yourself)원칙을 따른다.
# python manage.py makemigrations polls 명령어를 통해 새로운 모델을 만들었음을 django에게 알리고,
# 이 변경사항을 migration으로 저장하고 싶다는 것을 알린다.
# migration : 모델의 변경내역을 DB schema에 적용시키는 것
