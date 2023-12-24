from django.test import TestCase

from datetime import date
from bands.models import Musician, Venue
from django.contrib.auth.models import User


def raises_an_error():
    raise ValueError()


class TestBands(TestCase):
    def setUp(self):
        self.musician = Musician.objects.create(
            first_name="First", last_name="Last", birth=date(1900, 1, 1)
        )
        self.PASSWORD = "notsecure"
        self.owner = User.objects.create_user("owner", password=self.PASSWORD)
        self.member = User.objects.create_user("member", password=self.PASSWORD)

    def test_edit_venue(self):
        self.client.login(username="owner", password=self.PASSWORD)

        # Verify the page fetch works
        url = "/bands/edit_venue/0/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

        # Create a new venue
        data = {"name": "Name", "description": "Description"}
        response = self.client.post(url, data)

        self.assertEqual(302, response.status_code)

        # Validate the Venue was created
        venue = Venue.objects.first()
        self.assertEqual(data["name"], venue.name)
        self.assertEqual(data["description"], venue.description)
        self.assertTrue(
            self.owner.userprofile.venues_controlled.filter(id=venue.id).exists()
        )

    def test_musician_view(self):
        url = f"/bands/musician/{self.musician.id}/"

        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context["musician"].id, self.musician.id)
        self.assertIn(self.musician.first_name, str(response.content))

    def test_musician_404(self):
        url = f"/bands/musician/10/"
        response = self.client.get(url)

        self.assertEqual(404, response.status_code)

    def test_raises_an_error(self):
        with self.assertRaises(ValueError):
            raises_an_error()
