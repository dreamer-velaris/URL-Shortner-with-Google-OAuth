from flask import Flask, render_template, request, redirect, abort, session, url_for, make_response, jsonify
from models import db, Url, User
from datetime import datetime
import string, random

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "your-super-secret-key"

db.init_app(app)

def generate_short_id(user_id, num_chars=6):
    while True:
        short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))
        # Check if this short_id already exists for this user
        if not Url.query.filter_by(short_id=short_id, user_id=user_id).first():
            return short_id
        # If it exists, try again with a longer ID
        num_chars += 1



@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user_id = session.get('user_id')
    if request.method == 'POST':
        original_url = request.form['original_url']
        custom_alias = request.form.get('custom_alias')
        expiry_date = request.form.get('expiry_date')

        if custom_alias:
            exists = Url.query.filter_by(short_id=custom_alias, user_id=user_id).first()

            if exists:
                return "Custom alias already taken!", 400
            short_id = custom_alias
        else:
            short_id = generate_short_id(user_id)

        new_link = Url(
            original_url=original_url,
            short_id=short_id,
            created_at=datetime.utcnow(),
            expires_at=datetime.strptime(expiry_date, "%Y-%m-%d") if expiry_date else None,
            user_id=user_id
        )
        db.session.add(new_link)
        db.session.commit()

        return render_template("index.html", short_url=request.host_url + short_id, expiry_date=expiry_date)
    return render_template("index.html")

@app.route('/<short_id>')
def redirect_to_url(short_id):
    link = Url.query.filter_by(short_id=short_id).first()
    if link is None or (link.expires_at and datetime.utcnow() > link.expires_at):
        return abort(404)
    link.clicks += 1
    db.session.commit()
    return redirect(link.original_url)

@app.route('/stats/<short_id>')
def stats(short_id):
    link = Url.query.filter_by(short_id=short_id).first()
    if link is None:
        return abort(404)
    return render_template("stats.html", link=link)

@app.route('/export/<short_id>/<format>')
def export_stats(short_id, format):
    link = Url.query.filter_by(short_id=short_id).first()
    if not link:
        return abort(404)

    if format == 'json':
        return jsonify({
            "short_id": link.short_id,
            "original_url": link.original_url,
            "clicks": link.clicks,
            "created_at": link.created_at.isoformat(),
            "expires_at": link.expires_at.isoformat() if link.expires_at else None
        })

    elif format == 'csv':
        csv_data = (
            f"Short ID,Original URL,Clicks,Created At,Expires At\n"
            f"{link.short_id},{link.original_url},{link.clicks},{link.created_at},{link.expires_at or 'Never'}\n"
        )
        response = make_response(csv_data)
        response.headers["Content-Disposition"] = "attachment; filename=stats.csv"
        response.headers["Content-Type"] = "text/csv"
        return response

    return abort(400)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            error = "Username already exists"
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect('/login')
    return render_template('signup.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            session['user_id'] = user.id
            next_page = request.args.get('next') or '/'
            return redirect(next_page)
        else:
            error = "Invalid username or password"

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=81)

