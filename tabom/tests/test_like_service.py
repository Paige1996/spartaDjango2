from django.db import IntegrityError
from django.test import TestCase

from tabom.models import Like
from tabom.models.article import Article
from tabom.models.user import User
from tabom.services.like_service import do_like, undo_like

# test?
#테스트는 여러분이 작성한 코드가 의도한 대로 동작하는지를 검증해 줍니다.
# 사람이 아니라 코드로 코드를 검증하기 때문에 반복적으로 실행하는데 아주 유리합니다.
# 컴퓨터는 실수도 하지 않고, 반복되는 작업에 지치는 일도 없기 때문입니다.
#결과적으로 테스트는 개발자가 “**수정을 두려워하지 않도록 만들어줍니다.**” 이것이 여러분에게 테스트가 필요한 이유입니다.

# 좋아요 서비스 구현 테스트 칸
class TestLikeService(TestCase):
    def test_a_user_can_like_an_article(self) -> None:
        # Given
        user = User.objects.create(name="test")  # user와 article이 주어 졌을때,
        article = Article.objects.create(title="test_title")

        # When. user가 주어지고 article이 하나 주어졌을때, 한 게시글에 대해 유저가 좋아요를 했을때,
        # like 객체가 생기고
        like = do_like(user.id, article.id)

        # Then
        self.assertIsNotNone(like.id)  # 이 like객체는 none이 아니다.데이터베이스에 들어갔다. primary키가 발급이 되었다.
        self.assertEqual(user.id, like.user_id)  # user의 아이디가 like의 user id와 같다
        self.assertEqual(article.id, like.article_id)  # Article의 아이디도 like의 article id와 같다

    def test_a_user_can_like_an_article_only_once(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # Expect -> When과 Then을 함께 쓰려할때.
        do_like(user.id, article.id)  # like 1
        # with self.assertRaises(Exception): # 에러가 일어나야 하는 것을 테스트에서 검증하고싶음. Excepttion: 모든 exception의 상위 클래스 를 인자로 전달
        # with 과 같이 쓰는 것을 context manager라고 함.
        with self.assertRaises(IntegrityError):  # unique키가 있는데 중복된 key가 들어있거나 not null한 foreign key가 걸려있는데
            # null이 들어갔거나 할때 발생할때 이 integrityError가 에러가 발생함.
            do_like(user.id, article.id)  # like2
        # 테스트에서, 같은 유저가 같은 article을 두번 누를 수 없게 테스트를 해봄. 첫번째 like1은 성공, like2는 실패야해함

        # 없는 유저에 대해 like를 만드려고 할때 에러가 남

    def test_it_should_raise_exception_when_like_an_user_does_not_exist(self) -> None:
        # Given
        invalid_user_id = 9988  # 유효하지 않는 유저 아이디를 주고
        article = Article.objects.create(title="test_title")

        # Expect
        with self.assertRaises(IntegrityError):
            do_like(invalid_user_id, article.id)

    def test_it_should_raise_exception_when_like_an_article_does_not_exist(self) -> None:
        # Given
        user = User.objects.create(name="test")
        invalid_article_id = 9988

        # Expect
        with self.assertRaises(IntegrityError):
            do_like(user.id, invalid_article_id)

    def test_like_count_should_increase(self) -> None:
        # Given
        user = User.objects.create(name="test")  # user와 article 가져와서
        article = Article.objects.create(title="test_title")

        # When
        do_like(user.id, article.id)

        # Then #article의 좋아요 개수를 검증
        article = Article.objects.get(id=article.id)
        self.assertEqual(1, article.like_set.count())  # like_set이 있는데 에러가 나지않음? -> django_stop이 있기 때문에 에러가 나지않음
        # like_set은 manager객체. like 가 foreginkey로 article을 가르켰기 때문에 article에 like_set이라는 이름의 RelatedManager가 생긴것
        # manager는 모델 객체와 데이버베이스를 이어주는통로역활을 함. objects를 통해 쿼리를 하면 모델 객체를 얻을 수 있음. -> ldjango_admin_logike_set도 object이기 때문에 가능
        # article.like_set.all() 가능

    # 좋아요 취소 테스트
    def test_a_use_can_undo_like(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")
        like = do_like(user.id, article.id)

        # When
        undo_like(user.id, article.id)  # 좋아요 삭제 실행

        # Then
        with self.assertRaises(Like.DoesNotExist):  # 좋아요 취소 됐는지 검증
            Like.objects.filter(id=like.id).get()  # get을 했을때 DoesNotExist가 발생하는지 확인.
            # DoesNotExsit? object가 없을때 발생함


# 좋아요가 없는 상황에서 좋아요를 취소하려고 시도한 경우.
# def test_it_should_raise_an_exception_when_undo_like_which_does_not_exist(self) ->None:
#     # Given
#     user = User.objects.create(name="test")
#     article = Article.objects.create(title="test_title")
#
#     #Expect
#     with self.assertRaises(Like.DoesNotExist): #DoeNotExist가 발생하도록 한다
#         undo_like(user.id, article.id)
# 이 식을 지운 이유: like_service에서 get()하고 like.delete했다면 필요했지만 바로 delete()해주었기때문에 필요가없음
