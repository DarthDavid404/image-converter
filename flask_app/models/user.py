# Imports

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_bcrypt import Bcrypt
from flask import flash
import re

# Imports above this line
# ////////////////////////////////////////////////////////////////////////////////////////////////

# Important stuff
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


# insert the database name that user will be pulling from

db = 'imgconverter_db'

# /////////////////////////////////////////////////////////////////////////////////////////////////

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']
        
        
# Class instance creation above this line
# ///////////////////////////////////////////////////////////////////////////////////////////////////
        
# Register/Create User IN DATABASE

    @classmethod
    def register_user(cls, form_data):
    
        password = form_data['password']
        data = form_data.to_dict()
        data['password'] = bcrypt.generate_password_hash(password)
        query = "INSERT INTO users (email, password, created_at, updated_at ) VALUES (%(email)s, %(password)s, NOW(),NOW());"
        flash(u"Account Created!", 'success')
        return connectToMySQL(db).query_db(query,data)
    
    

    # Create User in Database above this line
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # Read and Retrieve User by ID and Email
    
    # GET USER BY ID

    @classmethod
    def get_user_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s'
        
        results = connectToMySQL(db).query_db(query,data)
        
        result = cls(results[0])
        
        if len(results) < 1:
            return False
        
        return result
    
    # GET USER BY EMAIL

    @classmethod 
    def get_user_by_email(cls, data):
        
        query = 'SELECT * FROM users WHERE email = %(email)s'
        
        results = connectToMySQL(db).query_db(query,data)
        
        if not results:
            flash(u'No account associated with that email!', 'no_account_in_db')
            return False
        
        result = cls(results[0])
        print(result)
        
        return result
    
    # Read and Retrieve User by ID and Email above this line
    # //////////////////////////////////////////////////////////////////////////////////////////////////
    
    # Delete User

    @classmethod
    def delete_user(cls, data):
        
        query = 'DELETE from users where id = %(id)s'
        
        return connectToMySQL(db).query_db(query, data)

    # Delete User from database above this line
    # //////////////////////////////////////////////////////////////////////////////////////////////////

    # Validate information from User Registration, User Login, and User Edit

    @staticmethod
    def validate_register_user(user):
        is_valid = True 
        # Assume true and assign false if it is not valid.
        #Email validation
        if not EMAIL_REGEX.match(user['email']): 
                flash(u"Invalid email address!", 'email_invalid')
                is_valid = False
        if len(user['password']) < 6:
                flash(u"Password Must be more than 6 characters.", 'password_less_than_six')
                is_valid = False
        if (user['confirm_password']) != user['password']:
                flash(u"Passwords must match.", 'confirm_password')
                is_valid = False
        return is_valid
    

    @staticmethod
    def validate_user_login(user_data, form_data):
        new_form_data = form_data.to_dict()
        
        if not new_form_data:
            flash(u"Invalid Email/Password", 'invalid_email_or_password')
            return False
        if not bcrypt.check_password_hash(user_data['password'], new_form_data['password'] ):
            # if we get False after checking the password
            flash(u"Invalid Email/Password",'invalid_password')
            return False
        return True


    # Validate information from User Registration and user Login above this line
    # //////////////////////////////////////////////////////////////////////////////////////////////////






