from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class IntegrationTests(APITestCase):
    def test_happy_path(self):
        user = User.objects.create()
        self.client.force_authenticate(user=user)

        # create customer
        customer_creation_response = self.client.post(
            "/customers/",
            {"name": "Jane Doe", "email": "jane@email.com", "age": 23},
            format="json",
        )
        self.assertEqual(
            customer_creation_response.status_code, status.HTTP_201_CREATED
        )
        customer_id = customer_creation_response.data["id"]

        # create transactions
        data = [
            {
                "reference": "000051",
                "account": "C00099",
                "date": "2020-01-03",
                "amount": "-51.13",
                "type": "outflow",
                "category": "groceries",
                "user_id": customer_id,
            },
            {
                "reference": "000052",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "2500.72",
                "type": "inflow",
                "category": "salary",
                "user_id": customer_id,
            },
            {
                "reference": "000053",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "-150.72",
                "type": "outflow",
                "category": "transfer",
                "user_id": customer_id,
            },
            {
                "reference": "000054",
                "account": "C00099",
                "date": "2020-01-13",
                "amount": "-560.00",
                "type": "outflow",
                "category": "rent",
                "user_id": customer_id,
            },
            {
                "reference": "000689",
                "account": "S00012",
                "date": "2020-01-10",
                "amount": "150.72",
                "type": "inflow",
                "category": "savings",
                "user_id": customer_id,
            },
        ]
        transaction_creation_response = self.client.post(
            "/transactions/", data, format="json"
        )
        self.assertEqual(
            transaction_creation_response.status_code, status.HTTP_201_CREATED
        )

        # get balance
        balance_response = self.client.get(
            f"/customers/{customer_id}/balance/", format="json"
        )
        self.assertEqual(balance_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            balance_response.data,
            [
                {
                    "account": "C00099",
                    "balance": "1738.87",
                    "total_inflow": "2500.72",
                    "total_outflow": "-761.85",
                },
                {
                    "account": "S00012",
                    "balance": "150.72",
                    "total_inflow": "150.72",
                    "total_outflow": "0.00",
                },
            ],
        )

        # get category summary
        response = self.client.get(
            f"/customers/{customer_id}/categories/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "inflow": {"salary": "2500.72", "savings": "150.72"},
                "outflow": {
                    "groceries": "-51.13",
                    "rent": "-560.00",
                    "transfer": "-150.72",
                },
            },
        )
