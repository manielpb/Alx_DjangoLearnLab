from datetime import date

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from api.models import Author, Book


class BookAPITests(APITestCase):
    """
    Testing strategy:
    - Public can READ (list/detail)
    - Only authenticated users can WRITE (create/update/delete)
    - Filtering/searching/ordering work on the list endpoint
    - Serializer validation blocks publication_year in the future
    """

    def setUp(self):
        # Create a user for authenticated requests
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="pass12345")

        # Create test data
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")

        self.book1 = Book.objects.create(
            title="Django Basics",
            publication_year=2020,
            author=self.author1,
        )
        self.book2 = Book.objects.create(
            title="REST APIs with DRF",
            publication_year=2022,
            author=self.author2,
        )

        # Endpoints (match your url patterns)
        self.list_url = "/api/books/"
        self.detail_url = f"/api/books/{self.book1.pk}/"
        self.create_url = "/api/books/create/"
        self.update_url = f"/api/books/{self.book1.pk}/update/"
        self.delete_url = f"/api/books/{self.book1.pk}/delete/"

    # ---------- helpers ----------
    def _get_list_payload(self, response):
        """
        Works whether pagination is ON or OFF.
        - If paginated, DRF returns {count, next, previous, results}
        - If not, DRF returns a list
        """
        data = response.data
        if isinstance(data, dict) and "results" in data:
            return data["results"]
        return data

    def _assert_denied_for_unauth(self, response):
        # Depending on auth settings, DRF may return 401 or 403
        self.assertIn(response.status_code, (401, 403))

    # ---------- READ: public ----------
    def test_list_books_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        payload = self._get_list_payload(response)
        titles = [item["title"] for item in payload]

        self.assertIn("Django Basics", titles)
        self.assertIn("REST APIs with DRF", titles)

    def test_detail_book_public(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["id"], self.book1.pk)
        self.assertEqual(response.data["title"], "Django Basics")
        self.assertEqual(response.data["publication_year"], 2020)

    # ---------- CREATE: auth only ----------
    def test_create_book_unauth_denied(self):
        payload = {"title": "New Book", "publication_year": 2021, "author": self.author1.pk}
        response = self.client.post(self.create_url, payload, format="json")
        self._assert_denied_for_unauth(response)

    def test_create_book_auth_success(self):
        self.client.force_authenticate(user=self.user)

        payload = {"title": "New Book", "publication_year": 2021, "author": self.author1.pk}
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, 201)

        self.assertTrue(Book.objects.filter(title="New Book").exists())

    def test_create_book_future_year_validation_fails(self):
        self.client.force_authenticate(user=self.user)

        future_year = date.today().year + 1
        payload = {"title": "Future Book", "publication_year": future_year, "author": self.author1.pk}
        response = self.client.post(self.create_url, payload, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertIn("publication_year", response.data)

    # ---------- UPDATE: auth only ----------
    def test_update_book_unauth_denied(self):
        payload = {"title": "Updated Title"}
        response = self.client.patch(self.update_url, payload, format="json")
        self._assert_denied_for_unauth(response)

    def test_update_book_auth_success(self):
        self.client.force_authenticate(user=self.user)

        payload = {"title": "Updated Title"}
        response = self.client.patch(self.update_url, payload, format="json")
        self.assertEqual(response.status_code, 200)

        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    # ---------- DELETE: auth only ----------
    def test_delete_book_unauth_denied(self):
        response = self.client.delete(self.delete_url)
        self._assert_denied_for_unauth(response)

    def test_delete_book_auth_success(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    # ---------- FILTER / SEARCH / ORDER ----------
    def test_filter_by_publication_year(self):
        response = self.client.get(self.list_url + "?publication_year=2022")
        self.assertEqual(response.status_code, 200)

        payload = self._get_list_payload(response)
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["title"], "REST APIs with DRF")

    def test_search_by_title_or_author_name(self):
        # assumes your search_fields include "title" and "author__name"
        response = self.client.get(self.list_url + "?search=django")
        self.assertEqual(response.status_code, 200)

        payload = self._get_list_payload(response)
        titles = [item["title"].lower() for item in payload]
        self.assertTrue(any("django" in t for t in titles))

    def test_order_by_publication_year_desc(self):
        response = self.client.get(self.list_url + "?ordering=-publication_year")
        self.assertEqual(response.status_code, 200)

        payload = self._get_list_payload(response)
        years = [item["publication_year"] for item in payload]
        self.assertEqual(years, sorted(years, reverse=True))
