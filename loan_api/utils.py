import datetime
import math
from decimal import Decimal


def calculate_loan_period_month(loan_period):
    return math.ceil(loan_period / 30)


def calculate_payment_dates(funding_date, loan_period):
    payment_dates = []
    current_date = funding_date
    loan_period_months = calculate_loan_period_month(loan_period)

    for _ in range(loan_period_months):
        # Add one month to the current date
        current_date += datetime.timedelta(days=30)

        # Add the current date to the list of payment dates
        payment_dates.append(current_date)

    return payment_dates


def calculate_monthly_payment(loan_amount, loan_period, annual_interest_rate):
    loan_period_months = calculate_loan_period_month(loan_period)

    base = Decimal(loan_amount / loan_period_months)

    fee = loan_amount * Decimal(5 / 100)
    monthly_fee = fee / loan_period_months

    monthly_interest_rate = Decimal(annual_interest_rate / 100) / 12
    monthly_interest = monthly_interest_rate * loan_amount

    monthly_payment = base + monthly_fee + monthly_interest
    return Decimal(monthly_payment)
