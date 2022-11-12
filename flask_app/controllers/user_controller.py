# Imports

from flask_app import app
from flask import render_template,redirect,request,session,flash,jsonify,make_response,send_file,url_for
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask_app.models.user import User
from flask_app.models.image import Img
from flask_app.models import image_converter
from PIL import Image
import os, sys

# Imports above this line
# /////////////////////////////////////////////////////////////////////////////////////////////////

# User Register Route

@app.route('/register_user', methods = ['POST'])
def register_user():
    
    if User.get_user_by_email(request.form):
        flash(u'Email already taken!', 'email_invalid_taken')
        return redirect('/')
    
    if not User.validate_register_user(request.form):
        return redirect('/')
        
    User.register_user(request.form)
    
    user = User.get_user_by_email(request.form)
    
    session['id'] = user.id
    
    return redirect('/upload_file_page')
    


# User Register Route above this line
# /////////////////////////////////////////////////////////////////////////////////////////////////

# User Login Route

@app.route('/login_user' , methods = ['POST'])
def login_user():
    
    if not User.get_user_by_email(request.form):
        return redirect('/')
    
    user = User.get_user_by_email(request.form)
    
    user_in_db = {
        'email' : user.email,
        'password' : user.password
    }
    

    if not User.validate_user_login(user_in_db, request.form):
        return redirect('/')
    
    session['id'] = user.id
    
    return redirect('/upload_file_page')

    
@app.route('/logout_user', methods = ['GET'])
def logout_user(): 
    
    session.clear()
    
    return redirect('/')


# User Login and logout
# Route above this line
# /////////////////////////////////////////////////////////////////////////////////////////////////

# User home page

@app.route('/upload_file_page', methods =['GET', 'POST'])
def upload_file_page():
    
    if 'id' not in session: 
        return redirect('/')
    
    f = ''
    new_filename = ''
    
    data = {
        'id' : session['id']
    }
    
    user = User.get_user_by_id(data)
    
    if 'filename' in session:
        new_filename = session['filename']
        print(session["filename"])
        if os.path.exists(f'flask_app/static/uploads/{new_filename}'):
            os.remove(f'flask_app/static/uploads/{new_filename}')
            session.pop('filename')
            session.pop('filepath')
            
    
    
    if request.method == "POST": 
        
        file = request.files['file']
        file_extension = request.form['file_out'] 
        filename_without_ext = request.files['file'].filename.split('.')
        new_filename = filename_without_ext[0] + f'.{file_extension}'
        
        
        if 'filename' in session:
            if os.path.exists(session["filename"]):
                os.remove(session["filename"])
            session.pop('filename')
            session.pop('filepath')
            
            
        im = Image.open(file)
        
        rgb_im = im.convert("RGB")
        
        rgb_im.save(f'flask_app/static/uploads/{new_filename}')
        session['filename'] = f'{new_filename}'
        session['filepath'] = f'http://localhost:5000/static/uploads/{new_filename}'
        print(new_filename)
        print(session['filename'])
        f = new_filename
        new_filepath = session['filepath']
        return new_filepath , 200
        
    return render_template('/upload_file_page.html', user = user, filename = f,)

# ///////////////////////////////////////////////////////////////////////////////////////////////// 


@app.route('/remove_file', methods =['GET'])
def remove_file():
    
    
    if 'filename' in session:
        new_filename = session['filename']
        print(session["filename"])
        if os.path.exists(f'flask_app/static/uploads/{new_filename}'):
            os.remove(f'flask_app/static/uploads/{new_filename}')
            session.pop('filename')
            session.pop('filepath')
            return 'success',200
        return 'success', 200
    else: 
        return 'There was no file!', 200
    
    
@app.route('/download_file', methods =['GET'])
def download_file():
    
    if 'filename' in session:
        new_filepath = session['filename']
        
        print('new filepath under')
        
        return (f'http://localhost:5000/static/uploads/{new_filepath}') ,200
    else: 
        return 'There was no file!',400
    
    

@app.route('/save_file', methods = ['GET'])
def save_file():
    

    if 'id' not in session: 
        
        return redirect('/')
    
    print('filepath here')
    print(session['filepath'])
    data = {
        'users_id': session['id'],
        'filepath': session['filepath'],
        'filename': session['filename']
    }
    
    Img.save_file(data)
    
    session.pop('filepath')
    session.pop('filename')
    
    return redirect('/saved_files')
    
    




@app.route('/saved_files', methods =['GET'])
def saved_file_page():
    
    if 'id' not in session: 
        return redirect('/')
    
    data = {
        'id' : session['id']
    }
    
    images = Img.get_saved_files()
    user = User.get_user_by_id(data)
    return render_template('/saved_files.html', user = user, images = images)

@app.route('/delete_file' , methods = ['post'])
def delete_file():
    
    if 'id' not in session: 
        return redirect('/')
    
    
    
    filename_to_delete = request.form['image_name']
    if os.path.exists(f'flask_app/static/uploads/{filename_to_delete}'):
            os.remove(f'flask_app/static/uploads/{filename_to_delete}')
    
    data = {'id': request.form['image_id'] }
    
    Img.delete_file(data)
    
    return redirect('/saved_files'), 200