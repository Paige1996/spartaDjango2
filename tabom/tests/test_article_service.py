from django.test import TestCase

from tabom.models import User
from tabom.models.article import Article
from tabom.services.article_service import get_an_article, get_article_list

#하나의 article내용을 보여주는 역활
from tabom.services.like_service import do_like


class TestArticleService(TestCase):
    def test_you_can_get_an_article_by_id(self) -> None: #id로 article을 조회할수있다
        # Given
        title = "test_title" #title하나 주고
        article = Article.objects.create(title=title) #article을 하나 만들어서

        # When
        result_article = get_an_article(article.id) #get_an_article로 aricle.id를 전달해서 조회한다

        # Then
        self.assertEqual(article.id, result_article.id) #그렇게 조회한 result_aricle.id와 처음에 만든 article.id가 같은지 비교
        self.assertEqual(title, result_article.title) #title도 제대로 조회가 됐는지 확인한다.

#article을 만들지 않고 없는 article번호를 가리킨다.
    #위의 함수와 아래의 함수가 서로 영향을 주는가? no. 테스트의 isolation때문에 위와 아래는 아무 상관이없다.
    def test_it_should_raise_exception_when_article_does_not_exist(self) -> None:
        # Given
        invalid_article_id = 9988 #이상한 번호로 저장을하고

        # Expect
        with self.assertRaises(Article.DoesNotExist): #없는 번호는 DoenNotExist에러가 난다.
            get_an_article(invalid_article_id)
#게시글 리스트를 조회
    def test_get_article_list_should_prefetch_like(self) ->None:
        # Given
        user = User.objects.create(name="test_user")
        articles = [Article.objects.create(title= f"{i}") for i in range(1,21)]
        #article 을 만들기 위해 comprehension 을씀.
        do_like(user.id, articles[-1].id)
        #-1 article.즉 가장 최신으로 만들어진 article에 좋아요를 해봄.

        #WHEN
        result_articles = get_article_list(0, 10) #result_article의 limite을 10으로 걸었으니

        #Then
        self.assertEqual(len(result_articles),10) #result_article에 길이를 검증. 여기도 limit이 10이어야함
        self.assertEqual(1, result_articles[0].like_set.count()) #좋아요를 받은 article은 가장 최근에 생성된 aricle로 지정함.
        #그러므로 결과 리스트에서는 제일 앞에 나와야함.
        self.assertEqual(#결과에서 id만 비교 하는것.
            [a.id for a in reversed(articles[10:21])], #역순 정렬. 내림차순으로 정렬., 그리고 잘라내기
            [a.id for a in result_articles],
        )