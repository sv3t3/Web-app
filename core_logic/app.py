# ------------------------------
# Imports
# ------------------------------
from datetime import date
from flask import Flask, url_for, render_template, request, session
from flask_session import Session
from functools import wraps
from kinde_sdk import Configuration
from kinde_sdk.kinde_api_client import GrantType, KindeApiClient
from flask_sqlalchemy import SQLAlchemy

# ------------------------------
# App Setup
# ------------------------------
app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
Session(app)

# ------------------------------
# Kinde Client Setup
# ------------------------------
configuration = Configuration(host=app.config["KINDE_ISSUER_URL"])
kinde_api_client_params = {
    "configuration": configuration,
    "domain": app.config["KINDE_ISSUER_URL"],
    "client_id": app.config["CLIENT_ID"],
    "client_secret": app.config["CLIENT_SECRET"],
    "grant_type": app.config["GRANT_TYPE"],
    "callback_url": app.config["KINDE_CALLBACK_URL"],
}
if app.config["GRANT_TYPE"] == GrantType.AUTHORIZATION_CODE_WITH_PKCE:
    kinde_api_client_params["code_verifier"] = app.config["CODE_VERIFIER"]

kinde_client = KindeApiClient(**kinde_api_client_params)
user_clients = {}

# ------------------------------
# Database Models
# ------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'
    
# ------------------------------
# Kinde auth
# ------------------------------
def get_authorized_data(kinde_client):
    user = kinde_client.get_user_details()
    
    return {
        "id": user.get("id"),
        "user_given_name": user.get("given_name"),
        "user_family_name": user.get("family_name"),
        "user_email": user.get("email"),
        "user_picture": user.get("picture"),
    }

def login_required(user):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not user.is_authenticated():
                return app.redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/")
def index():
    data = {"current_year": date.today().year}
    template = "logged_out.html"
    if session.get("user"):
        kinde_client = user_clients.get(session.get("user"))
        if kinde_client.is_authenticated():
            data.update(get_authorized_data(kinde_client))        
            template = "home.html"
    return render_template(template, **data)

@app.route("/api/auth/login")
def login():
    return app.redirect(kinde_client.get_login_url())

@app.route("/users", methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route("/api/auth/register")
def register():
    return app.redirect(kinde_client.get_register_url())

@app.route("/api/auth/kinde_callback")
def callback():
    kinde_client.fetch_token(authorization_response=request.url)
    data = {"current_year": date.today().year}
    data.update(get_authorized_data(kinde_client))
    session["user"] = data.get("id")
    user_clients[data.get("id")] = kinde_client
    # print(f"User ID: {data.get('id')}")
    # print(f"Email: {data.get('user_email')}")

    # Fetch user details
    user_details = kinde_client.get_user_details()
    user_email = user_details["email"]
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=user_email).first()
    if not existing_user:
        new_user = User(email=user_email)
        db.session.add(new_user)
        db.session.commit()

    # Redirect to home or another appropriate page
    return app.redirect(url_for("index"))

@app.route("/api/auth/logout")
def logout():
    user_clients[session.get("user")] = None
    session["user"] = None
    return app.redirect(
        kinde_client.logout(redirect_to=app.config["LOGOUT_REDIRECT_URL"])
    )

@app.route("/details")
def get_details():
    template = "logged_out.html"
    if session.get("user"):
        kinde_client = user_clients.get(session.get("user"))
        data = {"current_year": date.today().year}
        data.update(get_authorized_data(kinde_client))
        data["access_token"] = kinde_client.configuration.access_token
        template = "details.html"
    return render_template(template, **data)

@app.route("/helpers")
def get_helper_functions():
    template = "logged_out.html"
    if session.get("user"):
        kinde_client = user_clients.get(session.get("user"))
        data = {"current_year": date.today().year}
        data.update(get_authorized_data(kinde_client))
        data["claim"] = kinde_client.get_claim("iss")
        data["organization"] = kinde_client.get_organization()
        data["user_organizations"] = kinde_client.get_user_organizations()
        data["flag"] = kinde_client.get_flag("theme")
        data["bool_flag"] = kinde_client.get_boolean_flag("is_dark_mode")
        data["str_flag"] = kinde_client.get_string_flag("theme")
        data["int_flag"] = kinde_client.get_integer_flag("competitions_limit")
        template = "helpers.html"
    return render_template(template, **data)

# ------------------------------
# Database Initialization
# ------------------------------
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/portfolio', methods=['GET', 'POST'])
# def portfolio():
#     if request.method == 'POST':
#         exchange = request.form.get('exchange')
#         session['exchange'] = exchange
#         session['holdings'] = {}
#         return redirect(url_for('add_coins', exchange=exchange))
#     return render_template('exchange_form.html')

# @app.route('/add_coins/<exchange>', methods=['GET', 'POST'])
# def add_coins(exchange):
#     if request.method == 'POST':
#         coin = request.form.get('coin')
#         amount = float(request.form.get('amount'))
#         session['holdings'][coin] = amount
#         session.modified = True  # add this line
#         return redirect(url_for('add_coins', exchange=exchange))
#     return render_template('coin_form.html', exchange=exchange)

# @app.route('/calculate_portfolio', methods=['GET'])
# def calculate_portfolio():
#     exchange = session.get('exchange')
#     holdings = session.get('holdings')
#     if exchange and holdings:
#         total_value = calculate_portfolio_value(exchange, holdings)
#         return render_template('portfolio_value.html', total_value=total_value, exchange=exchange)
#     else:
#         return 'No exchange or holdings found in session.'

