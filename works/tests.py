import calendar

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import User, Work


def create_works(user_id):
    _, lastday = calendar.monthrange(timezone.now().year, timezone.now().month)
    for i in range(lastday):
        t = timezone.now().date().replace(day=1) + timezone.timedelta(days=i)
        Work.objects.create(
                user_id=User.objects.get(id=user_id),
                date=t.strftime('%Y-%m-%d')
        )
    user_works = Work.objects.order_by("date").filter(
            date__gte=timezone.now().date().replace(day=1),
            date__lte=timezone.now().date().replace(day=lastday),
            user_id=user_id
    )
    return user_works


class IndexTest(TestCase):

    def test_login_to_index(self):
        # ログインからindexにアクセスして表示されるクエリをテスト

        user = self.client.force_login(User.objects.create_user("tester"))
        user_works = create_works(1)
        response = self.client.get(reverse("works:index"))
        self.assertQuerysetEqual(
                response.context["user_works"],
                user_works,
        )



# Create your tests here.
