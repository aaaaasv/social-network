from datetime import datetime

from blog.models import Like
from blog.views import LikeDateFilter
from accounts.tests.test_views import SetUpTestCase


class LikeFilterTestCase(SetUpTestCase):
    fixtures = SetUpTestCase.fixtures + ['post-data.json']

    def test_like_date_filter_before(self):
        date_to_filter = {'date_to': datetime.strptime('26 Sep 2018', '%d %b %Y')}
        f = LikeDateFilter(date_to_filter, queryset=Like.objects.all())
        self.assertEqual(len(f.qs), 1)

    def test_like_date_filter_after(self):
        date_to_filter = {'date_from': datetime.strptime('25 May 2019', '%d %b %Y')}
        f = LikeDateFilter(date_to_filter, queryset=Like.objects.all())
        self.assertEqual(len(f.qs), 4)

    def test_like_date_filter_between(self):
        date_to_filter = {
            'date_from': datetime.strptime('03 May 2018', '%d %b %Y'),
            'date_to': datetime.strptime('10 Mar 2021', '%d %b %Y')
        }
        f = LikeDateFilter(date_to_filter, queryset=Like.objects.all())
        self.assertEqual(len(f.qs), 5)
