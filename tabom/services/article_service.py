from django.core.paginator import Paginator, Page
from django.db.models import QuerySet

from tabom.models import Article


def get_an_article(article_id: int) -> Article:
    article = Article.objects.filter(id=article_id).get()
    return article


def get_article_list(offset: int, limit: int) -> QuerySet[Article]: #ARTICLE을 가진 쿼리셋. 이라는 뜻.
    return Article.objects.order_by("-id")[offset: offset + limit] #id에 내림차순으로 정렬이 됨.
    # offset, limit의 경우 슬라이싱으로 할수있다. 즉 쿼리셋을 리스트 슬라이싱 하는것 처럼 슬라이싱 가능, 장고규칙.
    #슬라이싱?  a = [1,2,3][0:2] #리스트 슬라이싱. 이 경우 첫번째 요소와 두번째 요소 즉 1,2가나옴
#https://docs.djangoproject.com/en/4.0/topics/db/queries/#limiting-querysets

#
# #위와같이 슬라이싱 하는 방법 외에 그냥 장고 페이지네이터 클래스를 사용해서 가능.
# def get_article_page(page: int, limit:int) -> Page:
#     return Paginator(Article.objects.order_by("-id"), limit).page(page)
# #https://docs.djangoproject.com/en/4.0/topics/pagination/ 페이지네이터 사용법