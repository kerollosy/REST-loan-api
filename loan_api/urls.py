from django.urls import path
from .views import *


app_name = "loany"

urlpatterns = [
    path('create-investor/', create_investor, name='create-investor'),
    path('investors/', get_investors, name='get-offers'),
    path('investors/<int:pk>', get_investor, name='get-offers'),
    path('investors/<int:pk>/offers', get_investor_offers, name='get-offers'),

    path('create-borrower/', create_borrower, name='create-borrower'),
    path('borrowers/', get_borrowers, name='get-offers'),
    path('borrowers/<int:pk>', get_borrower, name='get-offers'),
    path('borrowers/<int:pk>/loans/', get_borrower_loans, name='get-offers'),

    path('request-loan/', create_loan, name='create-loan'),
    path('loans/', get_loans, name='get-offers'),
    path('loans/<int:pk>', get_loan, name='get-offers'),
    path('loans/<int:pk>/offers/', get_loan_offers, name='get-offers'),

    path('create-offer/', create_offer, name='create-offer'),
    path('offers/', get_offers, name='get-offers'),
    path('offers/<int:pk>', get_offer, name='get-offer'),
    path('offers/<int:pk>/accept/', accept_offer, name='accept-offer'),
]
