from tabom.models import Like


# 좋아요 서비스 구현 테스트 칸
def do_like(user_id: int, article_id: int) -> Like:
    return Like.objects.create(user_id=user_id, article_id=article_id)


def undo_like(user_id: int, article_id: int) -> None:
    Like.objects.filter(user_id=user_id, article_id=article_id).delete()
    # 같은 user_id와 article_id를 가지고있는 like는 몇개? 1개임. 두개일수 없음.

    # like = Like.objects.filter(user_id=user_id, article_id=article_id).get()
    # like.delete()
    # 위와 차이. get()을 해서 like.delete()하게되는것 보다 위의 식이 쿼리 1번을 아낄 수 있음.
