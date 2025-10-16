from flask import Blueprint, render_template, current_app, request
from .models import Product
import requests
from datetime import datetime
payments_bp = Blueprint('payments', __name__, url_prefix='')

def payfast_base(app):
    if app.config.get('PAYFAST_TEST', True):
        return 'https://sandbox.payfast.co.za/eng/process'
    return 'https://www.payfast.co.za/eng/process'

def build_payfast_data(app, product, order_id):
    data = {
        'merchant_id': app.config.get('PAYFAST_MERCHANT_ID'),
        'merchant_key': app.config.get('PAYFAST_MERCHANT_KEY'),
        'return_url': app.config.get('PAYFAST_RETURN_URL'),
        'cancel_url': app.config.get('PAYFAST_CANCEL_URL'),
        'notify_url': app.config.get('PAYFAST_NOTIFY_URL'),
        'm_payment_id': str(order_id),
        'amount': f"{float(product.price):.2f}",
        'item_name': product.name_en or product.name_zu,
        'email_address': app.config.get('MAIL_DEFAULT_SENDER')
    }
    return data

@payments_bp.route('/checkout/<int:product_id>', methods=['POST','GET'])
def checkout(product_id):
    product = Product.query.get_or_404(product_id)
    order_id = f"{product_id}-{int(datetime.utcnow().timestamp())}"
    pf_data = build_payfast_data(current_app, product, order_id)
    return render_template('payments/payfast_redirect.html', pf_url=payfast_base(current_app), pf_data=pf_data, product=product)

@payments_bp.route('/payfast/notify', methods=['POST'])
def payfast_notify():
    pf_data = request.form.to_dict(flat=True)
    verify_url = 'https://sandbox.payfast.co.za/eng/query/validate' if current_app.config.get('PAYFAST_TEST', True) else 'https://www.payfast.co.za/eng/query/validate'
    try:
        r = requests.post(verify_url, data=pf_data, timeout=10)
        if r.status_code == 200 and r.text == 'VALID':
            current_app.logger.info('PayFast ITN valid: %s', pf_data.get('m_payment_id'))
            return 'OK', 200
        else:
            current_app.logger.warning('Invalid PayFast ITN: %s', r.text)
            return 'ERROR', 400
    except Exception as e:
        current_app.logger.error('PayFast ITN error: %s', e)
        return 'ERROR', 500
