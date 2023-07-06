from django.contrib import admin
from .models import Investor, Borrower, Loan, Offer, Payment


class InvestorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'balance')


class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'balance')


class LoanAdmin(admin.ModelAdmin):
    list_display = ('id', 'borrower', 'loan_amount',
                    'loan_period', 'status', 'funded_date')


class OfferAdmin(admin.ModelAdmin):
    list_display = ('id', 'loan', 'interest', 'status')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'status')


admin.site.register(Investor, InvestorAdmin)
admin.site.register(Borrower, BorrowerAdmin)
admin.site.register(Loan, LoanAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Offer, OfferAdmin)
