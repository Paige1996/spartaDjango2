# from datetime import datetime
# from time import sleep
#
# from django.db import connection
# from django.test import TestCase
# from tabom.models import User, user
#
#
# class TestAutoNow(TestCase):
#     def test_auto_now_field_is_set_when_save(self) -> None:
#         user= User(name='test')
#         user.save()
#         self.assertIsNotNone(user.updated_at)
#         self.assertIsNotNone(user.created_at)
#
#     def test_auto_now_field_not_set_when_raw_sql_update_executed(self) -> None:
#         # Given
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "INSERT INTO tabom_user(id, name, updated_at, created_at) "
#                 "VALUES (1, 'hihi', '1999-01-01 10:10:10', '1999-01-01 10:10:10')"
#             )
#         #when
#             sleep(1)#1초의 시간이 지나고 나서
#             cursor.execute(
#                 "UPDATE tabom_user SET name='changed' WHERE id=1" #이렇게 업데이트 해 주기
#             )
#
#         #Then
#         user = User.objects.filter(id=1).get()#1-9부터 시작하기
#         self.assertEqual(user.updated_at, datetime(year=1999, month=1, day=1, hour=10, minute=10, second=10))
#         #updated_at과 datetime이 같은지 비교
