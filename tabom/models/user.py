from django.db import models

from tabom.models.base_model import BaseModel


class User(BaseModel):
    name = models.CharField(max_length=50)
    # updated_at = models.DateTimeField(auto_now=True)
    # auto_now : model객체를 save했을때 값을 전달하지 않아도 자동으로 필드가 업데이트됨
    # created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add : 생성될때 생성된 시간으로 필드 값을 줌.
    # 둘다 raw sql을 실행하면 작동하지 않음
