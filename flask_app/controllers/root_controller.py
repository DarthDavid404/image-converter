# Imports

from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user import User

# Imports above this line
# /////////////////////////////////////////////////////////////////////////////////////////////////

# Root Route Login and Registration Page

@app.route('/')
def home():
    if 'id' in session:

        return redirect(f'/upload_file_page')
    
    return render_template('login_register.html')  


# Root Route Login and Registration page above this line
# //////////////////////////////////////////////////////////////////////////////////////////////// 