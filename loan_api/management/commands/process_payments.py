from django.core.management.base import BaseCommand
from django.db import transaction
from loan_api.models import Payment
from loan_api.utils import calculate_monthly_payment
import datetime


class Command(BaseCommand):
    help = 'Process due payments'

    @transaction.atomic
    def handle(self, *args, **options):
        due_payments = Payment.objects.filter(
            status="PENDING", due_date__lte=datetime.date.today())

        if due_payments:
            for payment in due_payments:
                loan = payment.loan

                if loan.status == "PENDING":
                    self.stdout.write(self.style.ERROR(
                        "Loan is not being funded"))
                elif loan.status == "COMPLETED":
                    self.stdout.write(self.style.ERROR("Loan is Completed"))

                # Deduct monthly payment from borrower's balance
                monthly_payment = calculate_monthly_payment(
                    loan.loan_amount, loan.loan_period, loan.offer.first().interest)
                borrower = loan.borrower
                borrower.balance -= monthly_payment
                borrower.save()

                # Add monthly payment to investor's balance
                investor = loan.investor
                investor.balance += monthly_payment
                investor.save()

                # Update the payment status
                payment.status = "PAID"
                payment.save()

                # Check if all payments for the loan are paid
                all_payments_paid = loan.payment_set.filter(
                    status="PAID").count() == loan.payment_set.count()

                if all_payments_paid:
                    # Mark the loan as completed
                    offer = loan.offer.first()
                    offer.status = "PAID"
                    offer.save()

                    loan.status = "COMPLETED"
                    loan.save()

                    self.stdout.write(self.style.SUCCESS("Loan Completed"))
                else:
                    self.stdout.write(self.style.SUCCESS(
                        "Payments processed successfully"))
        else:
            self.stdout.write(self.style.ERROR(
                "There are no pending payments"))
