from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from core.models import User, Publisher, Article

class APISubscriptionsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.reader = User.objects.create_user(username="r1", password="pass", role="reader")
        self.journalist = User.objects.create_user(username="j1", password="pass", role="journalist")
        self.publisher = Publisher.objects.create(name="Daily Planet")
        self.publisher.journalists.add(self.journalist)

        # Reader subscribes
        self.reader.subscribed_publishers.add(self.publisher)
        self.reader.subscribed_journalists.add(self.journalist)

        Article.objects.create(
            title="Approved", body="Body", author=self.journalist,
            publisher=self.publisher, approved=True
        )
        Article.objects.create(
            title="Pending", body="Body", author=self.journalist,
            publisher=self.publisher, approved=False
        )

    def test_reader_gets_subscribed_articles_only(self):
        self.assertTrue(self.client.login(username="r1", password="pass"))
        url = reverse("articles-list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        titles = [a["title"] for a in resp.json()]
        self.assertIn("Approved", titles)
        self.assertNotIn("Pending", titles)