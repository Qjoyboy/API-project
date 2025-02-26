import requests
import stripe
from rest_framework import status

from config import settings
from courses.models import Payment

stripe.api_key = f"{settings.STRIPE_API_KEY}"

def create_payment(amount, currency="rub"):
    try:
        payment = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"]

        )
        return payment.client_secret, payment.id
    except Exception as e:
        return str(e)

def retrieve_payment(payment_intent_id):
    try:
        payment = stripe.PaymentIntent.retrieve(payment_intent_id)
        return {
            'status':payment.status,
            'amount':payment.amount_received,
            'currency': payment.currency,
            'payment': payment.payment_method
        }
    except stripe.error.StripeError as e:
        return None


