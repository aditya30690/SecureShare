from flask import Flask, render_template, request, redirect, send_from_directory
import os

app = Flask(__name__)

# =========================
# Upload Folder
# =========================

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =========================
# Temporary User Storage
# =========================

users = []

# =========================
# Home
# =========================

@app.route('/')
def home():
    return render_template('home.html')

# =========================
# Register
# =========================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        users.append({
            "name": name,
            "email": email,
            "password": password
        })

        print("User Registered:", email)

        return redirect('/login')

    return render_template('register.html')

# =========================
# Login
# =========================

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        for user in users:

            if (
                user['email'] == email and
                user['password'] == password
            ):
                return redirect('/dashboard')

        return "Invalid Email or Password"

    return render_template('login.html')

# =========================
# Dashboard
# =========================

@app.route('/dashboard')
def dashboard():

    files = os.listdir(app.config['UPLOAD_FOLDER'])

    return render_template(
        'dashboard.html',
        files=files
    )

# =========================
# Upload
# =========================

@app.route('/upload', methods=['POST'])
def upload():

    if 'file' not in request.files:
        return redirect('/dashboard')

    file = request.files['file']

    if file.filename == '':
        return redirect('/dashboard')

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    file.save(filepath)

    return redirect('/dashboard')

# =========================
# Download
# =========================

@app.route('/download/<filename>')
def download(filename):

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )

# =========================
# Delete
# =========================

@app.route('/delete/<filename>')
def delete(filename):

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        filename
    )

    if os.path.exists(filepath):
        os.remove(filepath)

    return redirect('/dashboard')

# =========================
# Run
# =========================

if __name__ == '__main__':
    app.run(debug=True)