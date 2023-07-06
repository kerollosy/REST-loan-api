import math
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LoanSerializer, OfferSerializer, InvestorSerializer, BorrowerSerializer
from .models import Investor, Borrower, Loan, Offer, Payment
from .utils import calculate_payment_dates, calculate_monthly_payment
from rest_framework import status
from decimal import Decimal
import datetime


@api_view(['POST'])
def create_investor(request):
    serializer = InvestorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_investors(request):
    investors = Investor.objects.all()
    serializer = InvestorSerializer(investors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_investor(request, pk):
    investor = get_object_or_404(Investor, pk=pk)
    serializer = InvestorSerializer(investor)
    return Response(serializer.data)


@api_view(['GET'])
def get_investor_offers(request, pk):
    investor = get_object_or_404(Investor, id=pk)
    offers = investor.investor_offers
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_borrower(request):
    serializer = BorrowerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_borrowers(request):
    borrowers = Borrower.objects.all()
    serializer = BorrowerSerializer(borrowers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_borrower(request, pk):
    borrower = get_object_or_404(Borrower, pk=pk)
    serializer = BorrowerSerializer(borrower)
    return Response(serializer.data)


@api_view(['GET'])
def get_borrower_loans(request, pk):
    borrower = get_object_or_404(Borrower, id=pk)
    loans = borrower.loan
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)


# Request a loan
@api_view(['POST'])
def create_loan(request):
    serializer = LoanSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_loans(request):
    loans = Loan.objects.all()
    serializer = LoanSerializer(loans, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    serializer = LoanSerializer(loan)
    return Response(serializer.data)


@api_view(['GET'])
def get_loan_offers(request, pk):
    loan = get_object_or_404(Loan, id=pk)
    offers = loan.offer
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_offer(request):
    serializer = OfferSerializer(data=request.data)
    if serializer.is_valid():
        investor_id = request.data["investor"]
        investor = get_object_or_404(Investor, id=investor_id)
        loan_id = request.data["loan"]
        loan = get_object_or_404(Loan, id=loan_id)

        if loan.status == "FUNDED":
            return Response({"error": "This loan is already funded"}, status=status.HTTP_400_BAD_REQUEST)

        # Assume we charge 5% of the loan amount
        fee = loan.loan_amount * Decimal(5/100)

        if investor.balance > (loan.loan_amount + fee):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"error": "Insufficient Funds"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_offers(request):
    offers = Offer.objects.all()
    serializer = OfferSerializer(offers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_offer(request, pk):
    offer = get_object_or_404(Offer, pk=pk)
    serializer = OfferSerializer(offer)
    return Response(serializer.data)


@api_view(['POST'])
def accept_offer(request, pk):
    offer = get_object_or_404(Offer, id=pk)
    loan = offer.loan

    if loan.status == "FUNDED":
        return Response({"error": "This loan is already funded"}, status=status.HTTP_400_BAD_REQUEST)

    if offer.status == "PENDING":
        investor = offer.investor
        fee = loan.loan_amount * Decimal(5/100)

        # In case the investor creates more than one offer and runs out of money
        if investor.balance < (loan.loan_amount + fee):
            return Response({"error": "Insufficient Funds"}, status=status.HTTP_400_BAD_REQUEST)


        offer.status = "ACCEPTED"
        offer.save()


        loan.status = "FUNDED"
        loan.funded_date = datetime.date.today()
        loan.investor = investor
        loan.save()


        investor.balance -= (loan.loan_amount + fee)
        investor.save()


        borrower = loan.borrower
        borrower.balance += loan.loan_amount
        borrower.save()


        payment_dates = calculate_payment_dates(
            datetime.date.today(), loan.loan_period)
        # payment_dates = [datetime.date.today()] #! DEBUG

        # Create Payment objects
        for payment_date in payment_dates:
            payment = Payment(
                loan=loan, due_date=payment_date, status="PENDING")
            payment.save()

        return Response({"message": "Loan funded successfully"}, status=status.HTTP_201_CREATED)

    return Response({"error": "Offer already accepted"}, status=status.HTTP_400_BAD_REQUEST)
