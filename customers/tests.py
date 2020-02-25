from rest_framework import status
from rest_framework.test import APITestCase
from customers.models import Customer
from transactions.models import Transaction, Category
from django.contrib.auth.models import User


def add_transactions_to_db(customer):
    Transaction.objects.create(
        reference="000051",
        account="C00099",
        date="2020-01-03",
        amount="-51.13",
        type="outflow",
        category=Category.GROCERIES,
        user=customer,
    )
    Transaction.objects.create(
        reference="000052",
        account="C00099",
        date="2020-01-10",
        amount="2500.72",
        type="inflow",
        category=Category.SALARY,
        user=customer,
    )
    Transaction.objects.create(
        reference="000053",
        account="C00099",
        date="2020-01-10",
        amount="-150.72",
        type="outflow",
        category=Category.TRANSFER,
        user=customer,
    )
    Transaction.objects.create(
        reference="000054",
        account="C00099",
        date="2020-01-13",
        amount="-560.00",
        type="outflow",
        category=Category.RENT,
        user=customer,
    )
    Transaction.objects.create(
        reference="000689",
        account="S00012",
        date="2020-01-10",
        amount="150.72",
        type="inflow",
        category=Category.SAVINGS,
        user=customer,
    )


class CustomerTests(APITestCase):
    def test_customer_create(self):
        user = User.objects.create()

        self.client.force_authenticate(user=user)
        data = {"name": "Jane Doe", "email": "jane@email.com", "age": 23}
        response = self.client.post("/customers/", data, format="json")
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

        customer = Customer.objects.create(
            name="Jane Doe", email="jane@email.com", age=23
        )

        response = self.client.get(f"/customers/{customer.id}/", format="json")

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

        response = self.client.get("/customers/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        for response_customer in response.data:
            customer = Customer.objects.get(pk=response_customer["id"])
            self.assertEqual(customer.name, response_customer["name"])
            self.assertEqual(customer.email, response_customer["email"])
            self.assertEqual(customer.age, response_customer["age"])

    def test_customer_balance(self):
        user = User.objects.create()
        self.client.force_authenticate(user=user)

        customer = Customer.objects.create(
            name="Jane Doe", email="jane@email.com", age=23
        )

        add_transactions_to_db(customer)

        response = self.client.get(f"/customers/{customer.id}/balance/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
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

    def test_customer_balance_in_timeframe_from(self):
        user = User.objects.create()
        self.client.force_authenticate(user=user)

        customer = Customer.objects.create(
            name="Jane Doe", email="jane@email.com", age=23
        )

        add_transactions_to_db(customer)

        response = self.client.get(
            f"/customers/{customer.id}/balance/?from=2020-01-10", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "account": "C00099",
                    "balance": "1790.00",
                    "total_inflow": "2500.72",
                    "total_outflow": "-710.72",
                },
                {
                    "account": "S00012",
                    "balance": "150.72",
                    "total_inflow": "150.72",
                    "total_outflow": "0.00",
                },
            ],
        )

    def test_customer_balance_in_timeframe_to(self):
        user = User.objects.create()
        self.client.force_authenticate(user=user)

        customer = Customer.objects.create(
            name="Jane Doe", email="jane@email.com", age=23
        )

        add_transactions_to_db(customer)

        response = self.client.get(
            f"/customers/{customer.id}/balance/?to=2020-01-10", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "account": "C00099",
                    "balance": "2298.87",
                    "total_inflow": "2500.72",
                    "total_outflow": "-201.85",
                },
                {
                    "account": "S00012",
                    "balance": "150.72",
                    "total_inflow": "150.72",
                    "total_outflow": "0.00",
                },
            ],
        )

    def test_customer_balance_in_timeframe_from_and_to(self):
        user = User.objects.create()
        self.client.force_authenticate(user=user)

        customer = Customer.objects.create(
            name="Jane Doe", email="jane@email.com", age=23
        )

        add_transactions_to_db(customer)

        response = self.client.get(
            f"/customers/{customer.id}/balance/?from=2020-01-10&to=2020-01-10",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            [
                {
                    "account": "C00099",
                    "balance": "2350.00",
                    "total_inflow": "2500.72",
                    "total_outflow": "-150.72",
                },
                {
                    "account": "S00012",
                    "balance": "150.72",
                    "total_inflow": "150.72",
                    "total_outflow": "0.00",
                },
            ],
        )

    def test_customer_categories(self):
        user = User.objects.create()
        self.client.force_authenticate(user=user)

        customer = Customer.objects.create(
            name="Jane Doe", email="jane@email.com", age=23
        )

        add_transactions_to_db(customer)

        response = self.client.get(
            f"/customers/{customer.id}/categories/", format="json"
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
