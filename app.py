import flask
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from werkzeug.exceptions import HTTPException
import arionpaylib
import os

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = "YOUR SECRET KEY"

"""
@app.errorhandler(Exception)
def custom_excepthandler(e):
    return render_template("error.html")
"""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_mnemonic = request.form['message']
        user_skey, user_pk = arionpaylib.mnemonic_to_pskey(user_mnemonic)
        asset_id = 42087963
        user_balance = arionpaylib.get_balance(user_pk, asset_id)
        return render_template("accpage.html", bal=user_balance, addr=user_pk)


@app.route('/signup')
def signup():
    address_sk, address, mnemonic = arionpaylib.generate_acc()
    acc_sk, acc_pk = arionpaylib.mnemonic_to_pskey(os.getenv('ip_mnc'))
    arionpaylib.acc_send1mil(address, acc_pk, acc_sk)
    asset_id = 42087963
    arionpaylib.auth_accasset(address, address_sk, asset_id)
    return render_template('acc_signup.html', addr=address, mnc=mnemonic)


@app.route('/transact', methods=['POST', 'GET'])
def transact():
    if request.method == 'POST':
        sender_address = request.form["address"]
        mnc = request.form["mnemonic"]
        login_sk, login_pk = arionpaylib.mnemonic_to_pskey(mnc)
        amount = request.form["amount"]
        asset_id = 42087963
        arionpaylib.send_transaction(login_pk, sender_address, amount, login_sk, asset_id)
        return render_template("success.html")

    else:
        return render_template("transact.html")


if __name__ == '__main__':
    app.run()
