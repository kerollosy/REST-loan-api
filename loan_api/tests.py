import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Investor, Borrower, Loan, Offer, Payment


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
            loan=self.loan, interest=15, investor=self.investor)
        response = self.client.post(
            f'/api/offers/{offer.id}/accept/', format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Loan.objects.get(id=self.loan.id).status, 'FUNDED')

    def test_process_payments(self):
        offer = Offer.objects.create(
            loan=self.loan, interest=15, investor=self.investor)
        self.loan.status = 'FUNDED'
        self.loan.investor = self.investor
        self.loan.save()
        Payment.objects.create(loan=self.loan, due_date=datetime.date.today())
        response = self.client.post('/api/process-payments/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(int(Borrower.objects.get(id=self.borrower.id).balance), int(
            self.loan.loan_amount / (self.loan.loan_period / 30)))
        self.assertEqual(Payment.objects.get(id=1).status, 'PAID')

    def test_process_payments_no_pending_payments(self):
        response = self.client.post('/api/process-payments/', format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
