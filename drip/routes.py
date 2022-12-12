from drip import app, limiter, s, mail
from flask import render_template, redirect, url_for, flash, request,session
from drip.models import User, Product, Sale
from drip.forms import RegisterForm, LoginForm, AddProductForm, DeleteProductForm, UpdateProductForm, ForgotPasswordForm
from drip import db
from flask_login import login_user, logout_user, login_required
from flask_mail import Mail, Message
from datetime import datetime, timedelta, date, time, timezone, tzinfo
from itsdangerous import SignatureExpired
from flask_limiter.util import get_remote_address


@app.route('/')
@app.route('/home')
@app.route('/index')
def home_page():
    return render_template('index.html')

@app.route('/shop')
def shop_page():
    return render_template('shop.html')

@app.route('/cart')
def cart_page():
    return render_template('cart.html')

@app.route('/checkout')
@login_required
def checkout_page():
    return render_template('checkout.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')


@app.route('/detail')
def detail_page():
    return render_template('detail.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        remote_address = get_remote_address()
        user_to_create = User(
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            username = form.username.data,
            email = form.email.data,
            phone_number = form.phone_number.data,
            password = form.password1.data,
            ip_address=remote_address,
        )
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Successfully logged in as:{user_to_create.username}', category='success')
        return redirect(url_for('shop_page'))
    if form.errors != {}: #if there are not errors from validation
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user:{err_msg}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email=form.email.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('shop_page'))
        else:
            flash('Email or password is  wrong! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have successfully logout!", category='info')
    return redirect(url_for("home_page"))


@app.route('/base')
def base_page():
    return render_template('base.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        product_to_create = Product(
            name = form.name.data,
            description = form.description.data,
            old_price = form.old_price.data,
            price = form.price.data,
            stock = form.stock.data,
            image = form.image.data,
            category = form.category.data,
        )
        db.session.add(product_to_create)
        db.session.commit()
        flash(f'Successfully added product:{product_to_create.name}', category='success')
        return redirect(url_for('shop_page'))
    if form.errors != {}: #if there are not errors from validation
          for err_msg in form.errors.values():
             flash(f'There was an error in creating a user:{err_msg}', category='danger')
    return render_template('add_product.html', form=form)


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/delete_product', methods=['GET', 'POST'])
@app.route('/delete_product/<int:product_id>', methods=['GET', 'POST'])
def delete_product():
    form = DeleteProductForm()
    if form.validate_on_submit():
        product_to_delete = Product.query.filter_by(product_id=form.product_id.data).first()
        if product_to_delete:
            db.session.delete(product_to_delete)
            db.session.commit()
            flash(f'Successfully deleted product:{product_to_delete.name}', category='success')
            return redirect(url_for('admin'))
        else:
            flash('Product does not exist!', category='danger')

    """ product_to_delete = Product.query.get(form.product_id.data)
    db.session.delete(product_to_delete)
    db.session.commit()
    return redirect(url_for('admin')) """

    return render_template('delete_product.html', form=form)

@app.route('/edit_product/<product_id>', methods=['GET', 'POST'])
@app.route('/edit_product', methods=['GET', 'POST']) 
@login_required
def edit_product(product_id):
    product = Product.query.get(product_id)
    form = UpdateProductForm(name=product.name, 
                            description=product.description, 
                            old_price=product.old_price, 
                            price=product.price, 
                            stock=product.stock, 
                            image=product.image, 
                            category=product.category)
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        description = request.form.get('description')
        old_price = request.form.get('old_price')
        price = request.form.get('price')
        stock = request.form.get('stock')
        image = request.form.get('image')
        category = request.form.get('category')

        # Update product in the database
        product = Product.query.get(product_id)
        product.name = name
        product.description = description
        product.old_price = old_price
        product.price = price
        product.stock = stock
        product.image = image
        product.category = category

        db.session.commit()

        return redirect(url_for('admin', product_id=product_id))
    else:
        # Render the edit product template with the current product's information
        product = Product.query.get(product_id)
        return render_template('edit_product.html', product=product, form=form)




@app.route('/sales')
def show_sales():
    product=Product.query.all()
    user=User.query.all()
    sales = (
    db.session.query(Sale, Product, User)
    .join(Product)
    .join(User)
    .all()
    )
    return render_template('sales.html', sales=sales, product=product, user=user)


"""@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            pass

    return render_template('forgot_password.html', form=form)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ForgotPasswordForm()
    # If the request is a POST request, the user has submitted the form
    if request.method == 'POST':
        # Get the email address from the form
        email = request.form['email']
        # Check if the email address exists in the database
        user = User.query.filter_by(email=email).first()
        if user:

            # Generate a unique token for the user
            #token = secrets.token_hex(16)
            # Generate a unique token
            token = uuid.uuid4().hex

            # Save the token and the time it was generated in the database
            user.reset_password_token = token
            user.reset_password_token_timestamp = datetime.utcnow()
            db.session.commit()

            # Generate the reset password link
            reset_link = url_for('reset_password_confirm', token=token, _external=True)

            # Send an email to the user with the reset password link
            send_email(
                to=user.email,
                subject='Reset your password',
                body=f'Click on the link to reset your password: {reset_link}'
            )
            # Redirect the user to the password reset confirmation page
            return redirect(url_for('reset_password_confirmation'))
        else:
               # If the email address doesn't exist in the database, redirect the user
               # to the password reset page with an error message
              return redirect(url_for('reset_password', error='Invalid email address'))
    else:
       # If the request is a GET request, the user has not submitted the form
       # Render the password reset page
       return render_template('reset_password.html', form=form)

# Define a route for the page where the user can enter a new password
@app.route('/reset_password_confirm/<token>', methods=['GET', 'POST'])
def reset_password_confirm(token):

       # Check if the provided token is valid
         user = User.query.filter_by(reset_password_token=token).first()
         if user:
        # Check if the token has expired
           time_elapsed = datetime.utcnow() - user.reset_password_token_timestamp
           if time_elapsed > timedelta(minutes=30):
               # If the token has expired, redirect the user to the password reset page
               return redirect(url_for('reset_password', error='Token expired'))
           else:
                # If the token is valid, render the page where the user can enter a new password
                return render_template('reset_password_confirm.html', token=token)"""
        
                   
@app.route("/reset-password", methods=["GET", "POST"])
@limiter.Limit("10 per minute")
def reset_password():
    form = ForgotPasswordForm()
    if request.method == "GET":
        # Render a form for the user to enter their email address.
        return render_template("reset-password.html")
    else:
         # Handle the form submission.
        email = request.form["email"]
        # Check if the email address exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate a password reset token and send it to the user via email.
            token = s.dumps(email, salt="password-reset")
            """ Save the token and the time it was generated in the database
            user.reset_password_token = token
            user.reset_password_token_timestamp = datetime.utcnow()
            db.session.commit()"""


            reset_link = url_for('reset_password_confirm', token=token, _external=True)

            msg = Message('Password Reset Request', sender='noreply@example.com', recipients=[email])
            msg.body = f'To reset your password, visit the following link: {reset_link}'
            mail.send(msg)
            return redirect(url_for('password_reset_sent'))
        else:
            return redirect(url_for('reset_password', error='Invalid email address'))

@app.route("/password-reset-sent")
def password_reset_sent():
    # Display a message to the user that the password reset email has been sent.
    return render_template("password-reset-sent.html")

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password_with_token(token):
    try:
        # Verify the password reset token and get the email address it corresponds to.
        email = s.loads(token, salt="password-reset", max_age=3600)
    except SignatureExpired:
        # The password reset token has expired.
        return redirect("/invalid-token")

    if request.method == "GET":
        # Render a form for the user to enter a new password.
        return render_template("reset-password-with-token.html", token=token)

    else:
        # Handle the form submission.
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Check if the new password and confirmation match.
        if password != confirm_password:
            # The passwords do not match. Display an error message and allow the user to try again.
            return render_template(
                "reset-password-with-token.html",
                token=token,
                error="The passwords do not match."
            )
        else:
           # The passwords match. Update the user's password and log them in.
           user = User.get_by_email(email)
           user.set_password(password)
           login_user(user)
           return redirect("/shop_page")
 
    

