import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Investor, Borrower, Loan, Offer, Payment
from .utils import calculate_monthly_payment
from django.core.management import call_command


class LoanTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.investor = Investor.objects.create(
            name="Investor", email="investor@example.com", balance=10000)
        self.borrower = Borrower.objects.create(
            name="Borrower", email="borrower@example.com", balance=0)
        self.loan = Loan.objects.create(
            borrower=self.borrower, loan_amount=5000, loan_period=180)

    def test_create_loan(self):
        loans_count_before = Loan.objects.count()
        data = {
            "borrower": self.borrower.id,
            "loan_amount": 5000,
            "loan_period": 180
        }
        response = self.client.post('/api/request-loan/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.count(), loans_count_before + 1)

    def test_create_offer(self):
        offers_count_before = Offer.objects.count()
        data = {
            "loan": self.loan.id,
            "interest": 15,
            "investor": self.investor.id
        }
        response = self.client.post('/api/create-offer/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), offers_count_before + 1)

    def test_accept_offer(self):
        offer = Offer.objects.create(
            loan=self.loan, interest=15, investor=self.investor
        )
        response = self.client.get(f'/api/loans/{self.loan.pk}/offers/').json()
        self.assertEqual(response[0]["loan"], self.loan.pk)

        investor_balance_before = self.investor.balance

        response = self.client.post(f'/api/offers/{offer.pk}/accept/').json()
        self.assertEqual(response["message"], "Loan funded successfully")

        self.loan.refresh_from_db()
        self.assertEqual(self.loan.status, "FUNDED")

        self.borrower.refresh_from_db()
        self.assertEqual(self.borrower.balance, 5000)

        self.investor.refresh_from_db()
        self.assertEqual(
            int(self.investor.balance),
            investor_balance_before -
            int(self.loan.loan_amount) -
            (int(self.loan.loan_amount) * (5 / 100))
        )

        response = self.client.post(f'/api/offers/{offer.pk}/accept/').json()
        self.assertEqual(response["error"], 'This loan is already funded')

    def test_process_payments(self):
        offer = Offer.objects.create(
            loan=self.loan, interest=15, investor=self.investor)
        self.loan.status = 'FUNDED'
        self.loan.investor = self.investor
        self.loan.save()
        payment = Payment.objects.create(
            loan=self.loan, due_date=datetime.date.today())

        borrower_balance_before = self.borrower.balance
        call_command('process_payments')

        self.borrower.refresh_from_db()
        self.assertEqual(
            int(self.borrower.balance),
            borrower_balance_before -
            int(calculate_monthly_payment(
                self.loan.loan_amount,
                self.loan.loan_period,
                offer.interest
            ))
        )

        payment.refresh_from_db()
        self.assertEqual(payment.status, 'PAID')

        offer.refresh_from_db()
        self.assertEqual(offer.status, 'PAID')

        self.loan.refresh_from_db()
        self.assertEqual(self.loan.status, 'COMPLETED')
