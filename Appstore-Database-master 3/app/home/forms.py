from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, SelectField, DateTimeField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Length


class DeveloperForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    website = StringField('Website', validators=[DataRequired()])
    bank_acc_number = IntegerField('Bank Account Number', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ApplicationForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    package_name = StringField('Package Name', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    app_type = SelectField('App Type', validators=[DataRequired()], 
                               choices = [('Free', 'Free'), ('Paid', 'Paid'), ('Sub', 'Sub')])

    price = FloatField('Price', validators=[InputRequired(), NumberRange(min=0, max=1000)])
    submit = SubmitField('Submit')


class UserForm(FlaskForm):
    apple_id = StringField('Apple Id', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    device = StringField('Device', validators=[DataRequired()])
    credit_card_num = IntegerField('Credit Card Number', validators=[DataRequired(), NumberRange(min=111111111111, max=9999999999999999)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=10, max=100)])
    submit = SubmitField('Submit')


class PurchaseForm(FlaskForm):
    purchase_date = DateTimeField('Purchase Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    rating = FloatField('Rating', validators=[InputRequired(), NumberRange(min=0, max=5)])
    comment = StringField('Comment', validators=[])
    submit = SubmitField('Submit')
