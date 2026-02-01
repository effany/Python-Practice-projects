import stripe
import os
from dotenv import load_dotenv
import json
from flask import Flask, render_template, jsonify, request, redirect, flash, abort, session, url_for

load_dotenv()

class PaymentManager:
    def __init__(self):
        self.stripe_api_key = os.environ.get('stripe_api_key')
        self.stripe_publishable_key = os.environ.get('stripe_publishable_key')
        self.stripe_session = None

    def create_session(self, cart_items, order_num):
        # Build line_items in Stripe's expected format
        stripe_line_items = []
        for item in cart_items:
            item_price = float(item['itemDiscountPrice']) if item['itemDiscountPrice'] != 'None' else float(item['itemPrice'])
            stripe_line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['itemName'],
                        'images': [item['itemImage']] if item.get('itemImage') else [],
                    },
                    'unit_amount': int(item_price * 100),  # Convert to cents
                },
                'quantity': item['itemCount'],
            })
        
        stripe.api_key = self.stripe_api_key
        self.stripe_session = stripe.checkout.Session.create(
            success_url = url_for('success_payment', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = url_for('cart', _external=True),
            line_items = stripe_line_items,
            mode = 'payment',
            metadata = {'order_number': order_num}
        )

        return redirect(self.stripe_session.url, code=303)

    def retrieve_payment_status(self, session_id):
        stripe.api_key = self.stripe_api_key
        return stripe.checkout.Session.retrieve(session_id)

    