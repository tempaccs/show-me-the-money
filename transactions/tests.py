from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from transactions.models import Transaction
from customers.models import Customer
from django.contrib.auth.models import User

class AccountTests(APITestCase):
    def test_transaction_create(self):
        user = User.objects.create()
        customer = Customer.objects.create(name="Jane Doe", email="jane@email.com", age=23)

        self.client.force_authenticate(user=user)
        data = {"reference": "000051", "account": "S00099", "date": "2020-01-13", "amount": "-51.13", "type": "outflow", "category": "groceries", "user_id": customer.id}
        response = self.client.post("/transactions/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check response
        self.assertEqual(response.data["reference"], data["reference"])
        self.assertEqual(response.data["account"], data["account"])
        self.assertEqual(response.data["date"], data["date"])
        self.assertEqual(response.data["amount"], data["amount"])
        self.assertEqual(response.data["type"], data["type"])
        self.assertEqual(response.data["category"], data["category"])
        self.assertEqual(response.data["user_id"], data["user_id"])

        # check created data
        self.assertEqual(Customer.objects.count(), 1)
        transaction = Transaction.objects.get(reference=response.data["reference"])
        self.assertEqual(transaction.account, data["account"])
        self.assertEqual(str(transaction.date), data["date"])
        self.assertEqual(str(transaction.amount), data["amount"])
        self.assertEqual(transaction.type, data["type"])
        self.assertEqual(transaction.category, data["category"])
        self.assertEqual(transaction.user.id, data["user_id"])
        
    def test_transaction_create_duplicate_reference(self):
        user = User.objects.create()
        customer = Customer.objects.create(name="Jane Doe", email="jane@email.com", age=23)

        self.client.force_authenticate(user=user)
        data = {"reference": "000051", "account": "S00099", "date": "2020-01-13", "amount": "-51.13", "type": "outflow", "category": "groceries", "user_id": customer.id}
        response = self.client.post("/transactions/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        duplicate_response = response = self.client.post("/transactions/", data, format='json')
        # TODO replace with constant
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data["reference"][0]), "transaction with this reference already exists.")
        

