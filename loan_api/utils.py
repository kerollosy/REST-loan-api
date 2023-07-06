import datetime
import math


def calculate_payment_dates(funding_date, loan_period):
    payment_dates = []
    current_date = funding_date
    loan_period_months = math.ceil(loan_period / 30)

    for _ in range(loan_period_months):
        # Add one month to the current date
        current_date += datetime.timedelta(days=30)

        # Add the current date to the list of payment dates
        payment_dates.append(current_date)

    return payment_dates


def calculate_repayment(loan_amount, loan_period, annual_interest_rate):
    loan_period_months = math.ceil(loan_period / 30)

    monthly_interest_rate = (annual_interest_rate / 100) / 12
    monthly_interest = loan_amount * monthly_interest_rate

    total_repayment = loan_amount + (monthly_interest * loan_period_months)

    return total_repayment
