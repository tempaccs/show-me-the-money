from rest_framework import status
from rest_framework.test import APITestCase
from customers.models import Customer
from transactions.models import Transaction
from django.contrib.auth.models import User


class TransactionTests(APITestCase):
    def test_transactions_create_multiple(self):
        """
        create general creation of transactions
        """
        user = User.objects.create()
        customer = Customer.objects.create(
            name="Jane Doe", email="jane@email.com", age=23
        )

        self.client.force_authenticate(user=user)
        data = [
            {
                "reference": "000051",
                "account": "S00099",
                "date": "2020-01-13",
                "amount": "-51.13",
                "type": "outflow",
                "category": "groceries",
                "user_id": customer.id,
            },
            {
                "reference": "000052",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "2500.72",
                "type": "inflow",
                "category": "salary",
                "user_id": customer.id,
            },
        ]
        response = self.client.post("/transactions/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check response
        self.assertEqual(response.data, data)
        self.assertEqual(Transaction.objects.count(), 2)

        # check created data
        transactions = Transaction.objects.all()
        for i in range(len(transactions)):
            self.assertEqual(transactions[i].reference, data[i]["reference"])
            self.assertEqual(transactions[i].account, data[i]["account"])
            self.assertEqual(str(transactions[i].date), data[i]["date"])
            self.assertEqual(str(transactions[i].amount), data[i]["amount"])
            self.assertEqual(transactions[i].type, data[i]["type"])
            self.assertEqual(transactions[i].category, data[i]["category"])
            self.assertEqual(transactions[i].user.id, data[i]["user_id"])

    def test_transactions_create_inflow_amount(self):
        """
        Inflow amounts must be positive
        """
        user = User.objects.create()
        customer = Customer.objects.create(
            name="Jane Doe", email="jane@email.com", age=23
        )

        self.client.force_authenticate(user=user)
        data = [
            {
                "reference": "000051",
                "account": "S00099",
                "date": "2020-01-13",
                "amount": "-51.13",
                "type": "inflow",
                "category": "groceries",
                "user_id": customer.id,
            }
        ]
        response = self.client.post("/transactions/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0]["non_field_errors"][0], "inflow amount must be > 0.",
        )

    def test_transactions_create_outflow_amount(self):
        """
        Outflow amounts must be negativ
        """
        user = User.objects.create()
        customer = Customer.objects.create(
            name="Jane Doe", email="jane@email.com", age=23
        )

        self.client.force_authenticate(user=user)
        data = [
            {
                "reference": "000051",
                "account": "S00099",
                "date": "2020-01-13",
                "amount": "51.13",
                "type": "outflow",
                "category": "groceries",
                "user_id": customer.id,
            }
        ]
        response = self.client.post("/transactions/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data[0]["non_field_errors"][0], "outflow amount must be < 0.",
        )

    # def test_transactions_create_multiple_with_duplicates(self):
    #     user = User.objects.create()
    #     customer = Customer.objects.create(
    #         name="Jane Doe", email="jane@email.com", age=23
    #     )

    #     self.client.force_authenticate(user=user)
    #     data = [
    #         {
    #             "reference": "000051",
    #             "account": "S00099",
    #             "date": "2020-01-13",
    #             "amount": "-51.13",
    #             "type": "outflow",
    #             "category": "groceries",
    #             "user_id": customer.id,
    #         },
    #         {
    #             "reference": "000051",
    #             "account": "S00099",
    #             "date": "2020-01-13",
    #             "amount": "-51.13",
    #             "type": "outflow",
    #             "category": "groceries",
    #             "user_id": customer.id,
    #         },
    #     ]
    #     response = self.client.post("/transactions/", data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(
    #         response.data["reference"][0],
    #         "transaction with this reference already exists.",
    #     )
