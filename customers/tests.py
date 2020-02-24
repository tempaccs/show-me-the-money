from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from customers.models import Customer
from django.contrib.auth.models import User

class AccountTests(APITestCase):
    def test_customer_create(self):
        user = User.objects.create()

        self.client.force_authenticate(user=user)
        data = {"name": "Jane Doe", "email": "jane@email.com", "age": 23}
        response = self.client.post("/customers/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check response
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["email"], data["email"])
        self.assertEqual(response.data["age"], data["age"])

        # check created data
        self.assertEqual(Customer.objects.count(), 1)
        customer = Customer.objects.get(pk=response.data["id"])
        self.assertEqual(customer.name, data["name"])
        self.assertEqual(customer.email, data["email"])
        self.assertEqual(customer.age, data["age"])


    def test_customer_retrieve(self):
        user = User.objects.create()
        
        self.client.force_authenticate(user=user)

        customer = Customer.objects.create(name="Jane Doe", email="jane@email.com", age=23)

        # TODO interpolate string properly
        response = self.client.get("/customers/" + str(customer.id) + "/", format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(customer.name, response.data["name"])
        self.assertEqual(customer.email, response.data["email"])
        self.assertEqual(customer.age, response.data["age"])


    def test_customer_list(self):
        user = User.objects.create()
        self.client.force_authenticate(user=user)

        Customer.objects.create(name="Jane Doe", email="jane@email.com", age=23)
        Customer.objects.create(name="Jack Doe", email="jack@email.com", age=45)
        Customer.objects.create(name="John Doe", email="john@email.com", age=80)

        response = self.client.get("/customers/", format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        for response_customer in response.data:
            customer = Customer.objects.get(pk=response_customer["id"])
            self.assertEqual(customer.name, response_customer["name"])
            self.assertEqual(customer.email, response_customer["email"])
            self.assertEqual(customer.age, response_customer["age"])

        


