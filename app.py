from flask import Flask, render_template, request, send_from_directory, redirect
import os

app = Flask(__name__)

# =========================
# Upload Folder
# =========================

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# =========================
# Routes
# =========================

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/dashboard')
def dashboard():

    files = os.listdir(app.config['UPLOAD_FOLDER'])

    return render_template(
        'dashboard.html',
        files=files
    )


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']

    if file and file.filename != "":

        filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            file.filename
        )

        file.save(filepath)

        return redirect('/dashboard')

    return "No file selected"


@app.route('/download/<filename>')
def download(filename):

    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )


@app.route('/delete/<filename>')
def delete(filename):

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        filename
    )

    if os.path.exists(filepath):
        os.remove(filepath)

    return redirect('/dashboard')


if __name__ == '__main__':
    app.run(debug=True)