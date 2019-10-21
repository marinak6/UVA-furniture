from django.test import TestCase, Client

# Create your tests here.
from .models import Furniture, Person, Category, Authenticator
import json
from django.http import JsonResponse

from django.db import DatabaseError, transaction


class CreateFurnitureListing(TestCase):
    # setUp method is called before each test in this class
    def setUp(self):

        self.c = Client()

    def test_success_response(self):
        # assumes user with id 1 is stored in db
        with transaction.atomic():
            p = Person(first_name="Bryan", last_name="Tran")
            p.save()
            c = Category(category="New Item")
            c.save()
            c = Category(category="Furniture")
            c.save()
        request = {
            "name": "TV5005",
            "seller": 1,
            "category": ["New Item", "Furniture"],
            "price": 10,
            "description": "New Chair, great quality"
        }

        with transaction.atomic():
            response = self.c.post(
                '/api/v1/furniture/create', request)
        res_message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)

    def test_invalid_id(self):
        # assumes user with id 1 is stored in db
        response = self.c.post('/api/v1/furniture/create', {"name": "TV500", "seller": 3383, "category": [
            "New Item"], "is_bought": "False", "price": 10, "description": " New Chair, great quality"})

        res_message = json.loads(response.content.decode("utf-8"))["Status"]
        self.assertEqual(res_message, 'Person matching query does not exist.')

    def test_get_furniture(self):
        request = {
            "name": "TV5005",
            "seller": 1,
            "is_bought": "True",
            "category": ["New Item", "Furniture"],
            "price": 10,
            "description": "New Chair, great quality"
        }

        with transaction.atomic():
            response = self.c.post('/api/v1/furniture/create', request)

        p = Person(first_name="Bryan", last_name="Tran")
        p.save()
        f = Furniture(name="TV", seller=p, is_bought=False,
                      price=10, description="New Chair, great quality")
        f.save()
        with transaction.atomic():
            response = self.c.get(
                '/api/v1/furniture/1')

        res_message = json.loads(response.content.decode("utf-8"))
        # self.assertEqual(res_message["id"], 1)
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_furniture(self):

        p = Person(first_name="Bryan", last_name="Tran")
        p.save()
        f = Furniture(name="TV", seller=p, is_bought=False,
                      price=10, description="New Chair, great quality")
        f.save()
        with transaction.atomic():
            response = self.c.get(
                '/api/v1/furniture/2838')

        res_message = json.loads(response.content.decode("utf-8"))
        self.assertEqual(res_message["Status"], 'Invalid furniture ID')


class CreateBid(TestCase):

    def setUp(self):
        self.c = Client()
        p = Person(first_name="Bryan", last_name="Tran")
        p.save()

        f = Furniture(name="TV", seller=p, is_bought=False,
                      price=10, description="New Chair, great quality")
        f.save()

    def test_create_bid(self):
        p2 = Person(first_name="Adam", last_name="Adam")
        p2.save()

        request = {"price": 4, "bidder": 2, "item_id": 1}

        response = self.c.post(
            '/api/v1/bid/create', request)
        res_message = json.loads(response.content.decode("utf-8"))

        self.assertEqual(res_message["status"], 'PENDING')


class CreatePersonWithPassword(TestCase):

    def setUp(self):
        self.c = Client()

    # Makes sure hash works
    def test_password(self):
        request = {
            "first_name": "Bryan",
            "last_name": "tran",
            "password": "abc123",
            "email": "bt2kg@virgina.edu"
        }
        response = self.c.post(
            '/api/v1/person/create', request)
        res_message = json.loads(response.content.decode("utf-8"))

        person = Person.objects.get(email="bt2kg@virgina.edu")

        self.assertNotEqual(person.password, 'abc123')

    def test_login(self):
        request = {
            "first_name": "Bryan",
            "last_name": "tran",
            "password": "abc123",
            "email": "bt2kg@virgina.edu"
        }
        response = self.c.post(
            '/api/v1/person/create', request)
        res_message = json.loads(response.content.decode("utf-8"))
        request2 = {
            "password": "abc123",
            "email": "bt2kg@virgina.edu"
        }

        response2 = self.c.post(
            '/api/v1/login/', request2)
        res_message = json.loads(response2.content.decode("utf-8"))
        self.assertEqual("authenticator" in res_message, True)

    def test_login_wrong_email(self):
        request = {
            "first_name": "Bryan",
            "last_name": "tran",
            "password": "abc123",
            "email": "bt2kg@virgina.edu"
        }
        response = self.c.post(
            '/api/v1/person/create', request)
        res_message = json.loads(response.content.decode("utf-8"))
        request2 = {
            "password": "abc123",
            "email": "wrong@virgina.edu"
        }

        response2 = self.c.post(
            '/api/v1/login/', request2)
        res_message = json.loads(response2.content.decode("utf-8"))
        self.assertEqual("authenticator" in res_message, False)


class CreateAuth(TestCase):
    def setUp(self):
        self.c = Client()

    def test_create_auth(self):
        request = {
            "first_name": "Bryan",
            "last_name": "tran",
            "password": "abc123",
            "email": "bt2kg@virgina.edu"
        }
        response = self.c.post(
            '/api/v1/person/create', request)
        person = Person.objects.get(email="bt2kg@virgina.edu")
        auth_obj = Authenticator.objects.get(
            person_id=person.pk)
        self.assertNotEqual(auth_obj.authenticator, None)

    def test_create_furniture_with_valid_auth(self):
        request = {
            "first_name": "Bryan",
            "last_name": "tran",
            "password": "abc123",
            "email": "bt2kg@virgina.edu"
        }
        response = self.c.post(
            '/api/v1/person/create', request)
        person = Person.objects.get(email="bt2kg@virgina.edu")
        auth_obj = Authenticator.objects.get(
            person_id=person.pk)
        request = {
            "name": "TV5005",
            "auth": auth_obj.authenticator,
            "category": ["New Item", "Furniture"],
            "price": 10,
            "description": "New Chair, great quality"
        }
        response = self.c.post(
            '/api/v1/furniture/create', request)
        res_message = json.loads(response.content.decode("utf-8"))
        self.assertEqual("id" in res_message, True)

    def test_create_furniture_with_invalid_auth(self):
        request = {
            "first_name": "Bryan",
            "last_name": "tran",
            "password": "abc123",
            "email": "bt2kg@virgina.edu"
        }
        response = self.c.post(
            '/api/v1/person/create', request)
        person = Person.objects.get(email="bt2kg@virgina.edu")
        auth_obj = Authenticator.objects.get(
            person_id=person.pk)
        request = {
            "name": "TV5005",
            "auth": "incorrect",
            "category": ["New Item", "Furniture"],
            "price": 10,
            "description": "New Chair, great quality"
        }
        response = self.c.post(
            '/api/v1/furniture/create', request)
        res_message = json.loads(response.content.decode("utf-8"))
        self.assertEqual("id" in res_message, False)
