
from flask import Flask, render_template_string, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ADMIN_PASSWORD = '192856'

# ✅ Google Site Verification File (HTML file method)
@app.route('/googlefcb469fbe4112161.html')
def google_verification_file():
    return 'google-site-verification: googlefcb469fbe4112161.html', 200, {'Content-Type': 'text/html'}

@app.route('/auto-login', methods=['POST'])
def auto_login():
    session['logged_in'] = True
    return ('', 204)

@app.route('/', methods=['GET', 'POST'])
def home():
    is_admin = session.get('logged_in', False)
    if request.method == 'POST' and is_admin:
        file = request.files.get('file')
        if file:
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            return redirect(url_for('home'))

    files = os.listdir(UPLOAD_FOLDER)
    file_links = ''.join(f'<li><a href="/download/{f}">{f}</a></li>' for f in files)

    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Secure Hacker Web</title>
    <style>
    html, body {
        margin: 0;
        padding: 0;
        background: black;
        color: #00ff00;
        font-family: monospace;
        overflow: hidden;
    }
    .content {
        text-align: center;
        padding: 40px 20px;
    }
    li a {
        color: #0f0;
        text-decoration: none;
    }
    </style>
</head>
<body>
    <div class="content">
        <h1>Secure Hacker Web</h1>
        <ul>
            {{ file_links|safe }}
        </ul>
        {% if is_admin %}
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload</button>
        </form>
        <a href="/logout">Logout</a>
        {% endif %}
    </div>
</body>
</html>
""", file_links=file_links, is_admin=is_admin, password=ADMIN_PASSWORD)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
