import os
from flask import Flask, render_template, request, redirect, flash, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import yaml

UPLOAD_FOLDER = 'static/image-post'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'crp', 'txt'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)
app.config['MYSQL_HOST'] = cred['mysql_host']
app.config['MYSQL_USER'] = cred['mysql_user']
app.config['MYSQL_PASSWORD'] = cred['mysql_password']
app.config['MYSQL_DB'] = cred['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    return render_template('gallery.html')

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect('/admin')
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect('/admin')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash(f"Successfully uploaded image(s)")
            return redirect('/admin')
        else:
            flash('Incorrect file type. Allowed types: jpg, jpeg, crp, txt', 'error')
            return redirect('/admin')
    return render_template('/admin/admin.html')

if __name__ == '__main__':
    app.run(debug=True)