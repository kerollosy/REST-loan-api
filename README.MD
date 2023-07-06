# Loan Management System
## Use Case
A borrower submitted a loan request for $5,000 to pay them back in 6 months. They received an offer from one of the investors on the platform with a 15% Annual Interest Rate. A fee will be added to the total loan amount to be paid by the investor.

## API Endpoints
* GET /api/investors/
* GET /api/investors/{id}
* GET /api/investors/{id}/offers/

* GET /api/borrowers/
* GET /api/borrowers/{id}
* GET /api/borrowers/{id}/loans/

* GET /api/loans/
* GET /api/loans/{id}
* GET /api/loans/{id}/offers/

* GET /api/offers/
* GET /api/offers/{id}

* POST /api/create-investor/
* POST /api/create-borrower/
* POST /api/request-loan/
* POST /api/create-offer/
* POST /api/offers/{id}/accept/

* POST /api/process-payments/

## Getting Started
1. Clone the project repository: `git clone https://github.com/kerollosy/REST-loan-api.git`
2. Open the directory: `cd REST-loan-api`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Create Initial migrations: `python manage.py makemigrations loan_api`
5. Set up the database: `python manage.py migrate`
6. Start the server: `python manage.py runserver`
7. Access the APIs using a tool like cURL or Postman.

## Testing
You can run the tests using `python manage.py test`