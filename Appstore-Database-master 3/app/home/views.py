# app/home/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, current_user
import MySQLdb
import os
import random


from . import home
from .forms import DeveloperForm, ApplicationForm, UserForm, PurchaseForm, ReviewForm


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    if current_user:
        return render_template('home/dashboard.html')
    else:
        return render_template('home/index.html', title="Welcome")


@home.route('/home/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")


# developer Views
@home.route('/developers', methods=['GET', 'POST'])
@login_required
def list_developers():
    """
    List all developers
    """
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from developers;"
    cur.execute(query_string)

    developers = cur.fetchall()

    db.close()


    return render_template('home/developers/developers.html',
                           developers=developers, title="Developers")


@home.route('/developers/add', methods=['GET', 'POST'])
@login_required
def add_developer():
    """
    Add a developer to the database
    """
    add_developer = True

    form = DeveloperForm()

    if form.validate_on_submit():
        try:
            pk = random.getrandbits(32)

            # add developer to the database
            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "INSERT INTO developers \
                            VALUES(%s, %s, %s, %s, %s, %s, %s);"

            cur.execute(query_string, (pk, 
                                                                       form.name.data, 
                                                                       form.email.data,
                                                                       form.country.data,
                                                                       form.address.data,
                                                                       form.website.data,
                                                                       form.bank_acc_number.data))
            db.commit()
            db.close()

            flash('You have successfully added a new developer.')

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            # in case developer name already exists
            flash('Error: Developer Name already exists.')

            # redirect to developers page
        return redirect(url_for('home.list_developers'))

    # load developer template
    return render_template('home/developers/developer.html', action="Add",
                           add_developer=add_developer, form=form,
                           title="Add developer")





@home.route('/developers/edit/<int:developer_id>', methods=['GET', 'POST'])
@login_required
def edit_developer(developer_id):
    """
    Edit a developer
    """
    add_developer = False

    form = DeveloperForm()

    if form.validate_on_submit():
        try:
   
            # add developer to the database
            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "UPDATE developers SET \
                            name = %s, email = %s, country = %s, address = %s, \
                            website = %s, bank_acc_number = %s \
                            WHERE developer_id = %s"
            cur.execute(query_string, (form.name.data, 
                                        form.email.data,
                                        form.country.data,
                                        form.address.data,
                                        form.website.data,
                                        form.bank_acc_number.data,
                                        developer_id))
            db.commit()
            db.close()

            flash('You have successfully Edited the developer information.')

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            
            flash('Error: Could Not Update Developer Information')

        return redirect(url_for('home.list_developers'))

    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from developers WHERE developer_id = {};".format(developer_id)
    cur.execute(query_string)

    developer = cur.fetchone()

    db.close()

    print("ROW:", developer)
    
    form.bank_acc_number.data = developer[6]
    form.address.data = developer[5]
    form.website.data = developer[4]
    form.country.data = developer[3]
    form.email.data = developer[2]
    form.name.data = developer[1]

    return render_template('home/developers/developer.html', action="Edit",
                           add_developer=add_developer, form=form,
                           developer=developer, title="Edit developer")


@home.route('/developers/delete/<int:developer_id>', methods=['GET', 'POST'])
@login_required
def delete_developer(developer_id):
    """
    Delete a developer from the database
    """
    try:

        db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

        cur = db.cursor()

        query_string = "DELETE FROM developers WHERE developer_id = {}".format(developer_id);

        cur.execute(query_string)
        db.commit()
        db.close()

        flash('You have successfully deleted a developer.')

    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        # in case developer name already exists
        flash('Error: Developer Doesnt exists.')
    # redirect to the developers page
    return redirect(url_for('home.list_developers'))


# Application Views
@home.route('/applications', methods=['GET', 'POST'])
@login_required
def list_applications():
    """
    List all applications
    """
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from applications;"
    cur.execute(query_string)

    applications = cur.fetchall()

    db.close()


    return render_template('home/applications/applications.html',
                           applications=applications, title="Applications")


@home.route('/applications/add/dev', methods=['GET', 'POST'])
@login_required
def add_app_under_dev():
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from developers;"
    cur.execute(query_string)

    developers = cur.fetchall()

    db.close()


    return render_template('/home/applications/developers_compact.html',
                           developers=developers, title="Developers")


@home.route('/applications/add/dev/<int:developer_id>', methods=['GET', 'POST'])
@login_required
def add_application(developer_id):
    """
    Add a application to the database
    """
    add_app = True

    form = ApplicationForm()

    if form.validate_on_submit():
        try:

            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "INSERT INTO applications \
                            VALUES(%s, %s, %s, %s, %s);"

            cur.execute(query_string, (form.package_name.data, 
                                        developer_id,
                                        form.name.data,
                                        form.app_type.data,
                                        form.price.data))
            db.commit()
            db.close()

            flash('You have successfully added a new Application.')

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)

            flash('Error: Application already exists.')

  
        return redirect(url_for('home.list_applications'))


    return render_template('home/applications/application.html', action="Add",
                           add_app=add_app, form=form,
                           title="Add Application")

@home.route('/applications/delete/<string:package_name>', methods=['GET', 'POST'])
@login_required
def delete_app(package_name):
    """
    Delete a application from the database
    """
    try:

        db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

        cur = db.cursor()

        query_string = "DELETE FROM applications WHERE package_name='{}'".format(package_name);

        cur.execute(query_string)
        db.commit()
        db.close()

        flash('You have successfully deleted an application.')
   
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
    
        flash('Error: Application Doesnt exists.')
    
    return redirect(url_for('home.list_applications'))


@home.route('/applications/edit/<int:developer_id>/<string:package_name>,', methods=['GET', 'POST'])
@login_required
def edit_app(developer_id, package_name):
    """
    Edit an application
    """
    add_app = False

    form = ApplicationForm()

    if form.validate_on_submit():
        try:

            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "UPDATE applications SET \
                            package_name = %s, developer_id = %s, name = %s, app_type = %s, \
                            price = %s \
                            WHERE package_name = %s"
            cur.execute(query_string, (form.package_name.data,
                                       developer_id,
                                       form.name.data,
                                       form.app_type.data,
                                       form.price.data,
                                       package_name))
            db.commit()
            db.close()

            flash('You have successfully Edited the App information.')
            print("COMPLETED!!!")
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
  
            flash('Error: Could Not Update App Information')

        return redirect(url_for('home.list_applications'))

    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from applications WHERE package_name='{}';".format(package_name)
    cur.execute(query_string)

    application = cur.fetchone()

    db.close()

    
    form.package_name.data = application[0]
    form.name.data = application[2]
    form.app_type.data = application[3]
    form.price.data = application[4]


    return render_template('home/applications/application.html', action="Edit",
                           add_app=add_app, form=form,
                           application=application, title="Edit Application")


# User Views
@home.route('/users', methods=['GET', 'POST'])
@login_required
def list_users():
    """
    List all users
    """
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from users;"
    cur.execute(query_string)

    users = cur.fetchall()

    db.close()


    return render_template('home/users/users.html',
                           users=users, title="Users")


@home.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    """
    Add a users to the database
    """
    add_user = True

    form = UserForm()

    if form.validate_on_submit():
        try:

            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "INSERT INTO users \
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"

            cur.execute(query_string, (form.apple_id.data, 
                                                                       form.name.data, 
                                                                       form.email.data,
                                                                       form.country.data,
                                                                       form.address.data,
                                                                       form.device.data,
                                                                       form.credit_card_num.data,
                                                                       form.age.data))
            db.commit()
            db.close()

            flash('You have successfully added a new user.')

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            # in case users name already exists
            flash('Error: User already exists.')

            # redirect to developers page
        return redirect(url_for('home.list_users'))

    # load users template
    return render_template('home/users/user.html', action="Add",
                           add_user=add_user, form=form,
                           title="Add User")





@home.route('/users/edit/<string:apple_id>', methods=['GET', 'POST'])
@login_required
def edit_user(apple_id):
    """
    Edit a users
    """
    add_user = False

    form = UserForm()

    if form.validate_on_submit():
        try:

            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "UPDATE users SET \
                            apple_id = %s, name = %s, email = %s, country = %s, address = %s, \
                            device = %s, credit_card_num = %s, age = %s \
                            WHERE apple_id = %s"
            cur.execute(query_string, ( form.apple_id.data,
                                        form.name.data, 
                                        form.email.data,
                                        form.country.data,
                                        form.address.data,
                                        form.device.data,
                                        form.credit_card_num.data,
                                        form.age.data,
                                        apple_id))
            db.commit()
            db.close()

            flash('You have successfully Edited the User information.')
  
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            # in case users name already exists
            flash('Error: Could Not Update User Information')

        # redirect to users page
        return redirect(url_for('home.list_users'))

    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from users WHERE apple_id = '{}';".format(apple_id)
    cur.execute(query_string)

    user = cur.fetchone()

    db.close()

    
    form.age.data = user[7]
    form.credit_card_num.data = user[6]
    form.device.data = user[5]
    form.address.data = user[4]
    form.country.data = user[3]
    form.email.data = user[2]
    form.name.data = user[1]
    form.apple_id.data = user[0]

    return render_template('home/users/user.html', action="Edit",
                           add_user=add_user, form=form,
                           user=user, title="Edit User")


@home.route('/users/delete/<string:apple_id>', methods=['GET', 'POST'])
@login_required
def delete_user(apple_id):
    """
    Delete a users from the database
    """
    try:
     
        db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

        cur = db.cursor()

        query_string = "DELETE FROM users WHERE apple_id = '{}'".format(apple_id);

        cur.execute(query_string)
        db.commit()
        db.close()

        flash('You have successfully deleted a user.')

    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        # in case users name already exists
        flash('Error: User Doesnt exists.')
    # redirect to the users page
    return redirect(url_for('home.list_users'))


@home.route('/purchases', methods=['GET', 'POST'])
@login_required
def list_purchases():
    """
    List all purchases
    """
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from purchases;"
    cur.execute(query_string)

    purchases = cur.fetchall()

    db.close()


    return render_template('home/purchases/purchases.html',
                           purchases=purchases, title="Purchases")


@home.route('/purchases/add/user', methods=['GET', 'POST'])
@login_required
def add_purchase_under_user():
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from users;"
    cur.execute(query_string)

    users = cur.fetchall()

    db.close()


    return render_template('/home/purchases/users_compact.html',
                           users=users, title="Users")


@home.route('/purchases/add/user/<string:apple_id>/app', methods=['GET', 'POST'])
@login_required
def add_purchase_under_user_app(apple_id):
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT a.package_name, a.name, a.price from \
                    applications a \
                    where not exists (select * from purchases where apple_id = '{}' and app = a.package_name) \
                    ;".format(apple_id)
    cur.execute(query_string)

    applications = cur.fetchall()

    db.close()


    return render_template('/home/purchases/applications_compact.html',
                           applications=applications, apple_id=apple_id, title="applications")


@home.route('/purchases/add/user/<string:apple_id>/app/<string:package_name>/<float:price>', methods=['GET', 'POST'])
@login_required
def add_purchase(apple_id, package_name, price):
    """
    Add a purchase to the database
    """
    add_purchase = True

    form = PurchaseForm()

    if form.validate_on_submit():
        try:
            order_id = random.getrandbits(32)

            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "INSERT INTO purchases \
                            VALUES(%s, %s, %s, %s, %s);"

            cur.execute(query_string, (order_id, 
                                       apple_id,
                                       package_name,
                                       price,
                                       form.purchase_date.data.strftime('%Y-%m-%d')))
            db.commit()
            db.close()

            flash('You have successfully added a new purchase.')

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            # in case purchase already exists
            flash('Error: Purchase already exists.')

        # redirect to purchases page
        return redirect(url_for('home.list_purchases'))


    return render_template('home/purchases/purchase.html', action="Add",
                           add_purchase=add_purchase, form=form,
                           title="Add Purchase")


@home.route('/purchases/delete/<int:order_id>', methods=['GET', 'POST'])
@login_required
def delete_purchase(order_id):
    """
    Delete a purchase from the database
    """
    try:
        db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

        cur = db.cursor()

        query_string = "DELETE FROM purchases WHERE order_id={}".format(order_id);

        cur.execute(query_string)
        db.commit()
        db.close()

        flash('You have successfully deleted a purchase.')

    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        # in case purchase  already exists
        flash('Error: Purchase Doesnt exists.')
    # redirect to the purchase page
    return redirect(url_for('home.list_purchases'))


@home.route('/reviews', methods=['GET', 'POST'])
@login_required
def list_reviews():
    """
    List all reviews
    """
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from reviews;"
    cur.execute(query_string)

    reviews = cur.fetchall()

    db.close()


    return render_template('home/reviews/reviews.html',
                           reviews=reviews, title="Reviews")


@home.route('/reviews/add/user', methods=['GET', 'POST'])
@login_required
def add_review_under_user():
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from users;"
    cur.execute(query_string)

    users = cur.fetchall()

    db.close()


    return render_template('/home/reviews/users_compact.html',
                           users=users, title="Users")


@home.route('/reviews/add/user/<string:apple_id>/app', methods=['GET', 'POST'])
@login_required
def add_review_under_user_app(apple_id):
    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT app from purchases where apple_id = '{}'".format(apple_id)
    cur.execute(query_string)

    applications = cur.fetchall()

    db.close()


    return render_template('/home/reviews/applications_compact.html',
                           applications=applications, apple_id=apple_id, title="applications")

@home.route('/reviews/add/user/<string:apple_id>/app/<string:package_name>', methods=['GET', 'POST'])
@login_required
def add_review(apple_id, package_name):
    """
    Add a review to the database
    """
    add_review = True

    form = ReviewForm()

    if form.validate_on_submit():
        try:

            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "INSERT INTO reviews \
                            VALUES(%s, %s, %s, %s);"

            cur.execute(query_string, (apple_id, 
                                       package_name,
                                       form.rating.data,
                                       form.comment.data))
            db.commit()
            db.close()

            flash('You have successfully added a new review.')
            print("COMPLETED!!!")
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)

            flash('Error: Review cant be added.')


        return redirect(url_for('home.list_reviews'))


    # load review template
    return render_template('home/reviews/review.html', action="Add",
                           add_review=add_review, form=form,
                           title="Add Review")


@home.route('/reviews/edit/user/<string:apple_id>/app/<string:package_name>', methods=['GET', 'POST'])
@login_required
def edit_review(apple_id, package_name):
    """
    Edit a review
    """
    add_review = True

    form = ReviewForm()


    if form.validate_on_submit():
        try:

            db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

            cur = db.cursor()

            query_string = "UPDATE reviews SET \
                            rating = %s, comment = %s \
                            WHERE user = %s and app = %s"
            cur.execute(query_string, (form.rating.data,
                                        form.comment.data, 
                                        apple_id,
                                        package_name))
            db.commit()
            db.close()

            flash('You have successfully Edited the Review.')

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
         
            flash('Error: Could Not Update Review')

           
        return redirect(url_for('home.list_reviews'))

    db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

    cur = db.cursor()

    query_string = "SELECT * from reviews WHERE user = '{}' and app = '{}';".format(apple_id, package_name)
    cur.execute(query_string)

    review = cur.fetchone()

    db.close()
    
    form.comment.data = review[3]
    form.rating.data = review[2]

    return render_template('home/reviews/review.html', action="Edit",
                           add_review=add_review, form=form,
                           review=review, title="Edit Review")


@home.route('/reviews/delete/user/<string:apple_id>/app/<string:package_name>', methods=['GET', 'POST'])
@login_required
def delete_review(apple_id, package_name):
    """
    Delete a review from the database
    """
    try:

        db = MySQLdb.connect("localhost", 'AppstoreDB', 'appstore12345', 'Appstore')

        cur = db.cursor()

        query_string = "DELETE FROM reviews WHERE user='{}' and app = '{}'".format(apple_id, package_name);

        cur.execute(query_string)
        db.commit()
        db.close()

        flash('You have successfully deleted a review.')
 
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
 
        flash('Error: Review Doesnt exists.')
    return redirect(url_for('home.list_reviews'))
