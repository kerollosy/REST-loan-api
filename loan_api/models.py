from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Investor(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(decimal_places=2, max_digits=99)

    def __str__(self):
        return self.name


class Borrower(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(decimal_places=2, max_digits=99, default=0)

    def __str__(self):
        return self.name


class Loan(models.Model):
    LOAN_CHOICES = (
        ("PENDING", "Pending"),
        ("FUNDED", "Funded"),
        ("COMPLETED", "Completed"),
    )
    borrower = models.ForeignKey(
        Borrower, on_delete=models.CASCADE, related_name="loan")
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, null=True, blank=True)
    loan_amount = models.DecimalField(decimal_places=2, max_digits=99)
    loan_period = models.PositiveIntegerField()  # In Days
    # Initialize status to be null and change it when it's funded
    status = models.CharField(
        max_length=10, choices=LOAN_CHOICES, default="PENDING")
    funded_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class Offer(models.Model):
    OFFER_CHOICES = (
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("PAID", "Paid"),
    )
    loan = models.ForeignKey(
        Loan, on_delete=models.CASCADE, related_name="offer")
    interest = models.DecimalField(decimal_places=1, max_digits=99, validators=[
                                   MinValueValidator(1), MaxValueValidator(100)])
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, related_name="investor_offers")
    status = models.CharField(
        max_length=10, choices=OFFER_CHOICES, default="PENDING")

    def __str__(self):
        return str(self.pk)


class Payment(models.Model):
    PAYMENT_CHOICES = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
    )
    loan = models.ForeignKey(
        Loan, on_delete=models.CASCADE, related_name='payment_set')
    due_date = models.DateField()
    status = models.CharField(
        max_length=10, choices=PAYMENT_CHOICES, default="PENDING")
