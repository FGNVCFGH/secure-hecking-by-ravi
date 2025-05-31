from flask import Flask, render_template_string, request, redirect, url_for, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ADMIN_PASSWORD = '192856'

# ✅ Google Site Verification Route
@app.route('/googlefcb469fbe4112161.html')
def google_verify():
    return 'google-site-verification: googlefcb469fbe4112161.html'

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
    @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

    html, body {
        margin: 0;
        padding: 0;
        background: black;
        color: #00ff00;
        font-family: 'Share Tech Mono', monospace;
        overflow: hidden;
    }

    canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: 0;
        pointer-events: none;
    }

    .content {
        text-align: center;
        padding: 40px 20px;
        position: relative;
        z-index: 1;
    }

    li a {
        color: #0f0;
        text-decoration: none;
        font-size: 18px;
        border-bottom: 1px dashed #0f0;
    }

    li a:hover {
        color: #f00;
        text-shadow: 0 0 5px red;
    }

    .upload-form {
        margin-top: 30px;
        border: 1px solid #0f0;
        padding: 10px;
        display: inline-block;
    }

    input[type=file], button {
        background: black;
        font-family: 'Share Tech Mono', monospace;
        font-size: 14px;
        color: #00ff00;
        border: 1px solid #00ff00;
        padding: 10px;
        margin: 10px;
        cursor: pointer;
        transition: 0.3s;
    }

    input[type=file]:hover, button:hover {
        background: #ff0000;
        color: #ffffff;
        border-color: #ff0000;
    }

    .secret-heart {
        position: fixed;
        bottom: 10px;
        right: 10px;
        font-size: 24px;
        cursor: pointer;
        opacity: 0.3;
        z-index: 2;
    }

    .secret-heart:hover {
        opacity: 1;
    }

    .modal {
        display: none;
        position: fixed;
        z-index: 3;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.9);
        justify-content: center;
        align-items: center;
    }

    .modal-content {
        background-color: black;
        padding: 30px;
        border: 1px solid #00ff00;
        color: #0f0;
    }

    .modal input, .modal button {
        padding: 10px;
        margin-top: 10px;
        border: 1px solid #0f0;
        background: black;
        color: #0f0;
    }

    .glow-red {
        color: red;
        animation: glow 1s infinite alternate;
        text-shadow: 0 0 5px red, 0 0 10px red;
    }

    @keyframes glow {
        from {
            text-shadow: 0 0 5px red, 0 0 10px red;
        }
        to {
            text-shadow: 0 0 20px red, 0 0 40px red;
        }
    }
    </style>
</head>
<body>

    <canvas id="matrix"></canvas>

    <div class="content">
        <h1 class="glow-red">⚠ Secure Hacker Web ⚠</h1>
        <h2 class="glow-red">⚠ Developed by Raj Panchal ⚠</h2>

        <div>
            <h3 class="glow-red">💾 Uploaded Files</h3>
            <ul>
                {{ file_links|safe }}
            </ul>
        </div>

        {% if is_admin %}
        <div class="upload-form">
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <button type="submit">Upload</button>
            </form>
            <div style="margin-top: 20px;">
                <a href="/logout" style="color: #ff0000; font-weight: bold; font-size: 18px; text-decoration: none; border: 1px solid #f00; padding: 5px 10px; display: inline-block;">🚪 Logout</a>
            </div>
        </div>
        {% endif %}
    </div>

    <div class="secret-heart" onclick="showModal()">❤️</div>

    <div class="modal" id="loginModal">
        <div class="modal-content">
            <h3>Admin Access</h3>
            <input type="password" id="secretPassword" placeholder="Enter Password"><br>
            <button onclick="submitPassword()">Login</button>
        </div>
    </div>

    <script>
    function showModal() {
        document.getElementById("loginModal").style.display = "flex";
    }

    function submitPassword() {
        const entered = document.getElementById("secretPassword").value;
        const correct = "{{ password }}";
        if (entered === correct) {
            fetch("/auto-login", { method: "POST" }).then(() => location.reload());
        } else {
            alert("Wrong password!");
        }
    }

    // Matrix background animation
    const canvas = document.getElementById("matrix");
    const ctx = canvas.getContext("2d");

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', () => {
        resizeCanvas();
        initMatrix();
    });
    resizeCanvas();

    const codeLines = [
        "ssh connect root@192.168.0.1",
        "nmap -sV -T4 10.0.0.1",
        "hydra -l admin -P passlist.txt",
        "export PATH=$PATH:/opt/exploit",
        "git clone https://github.com/hacktool",
        "python3 exploit.py --target 10.10.10.10",
        "curl -X POST http://malware.inj",
        "decrypt --key abc123",
        "chmod +x backdoor.sh",
        "whoami && sudo su",
        "scp payload.sh user@host:/tmp",
        "iptables --flush",
        "echo 'hacked' >> /var/log/syslog"
    ];

    const fontSize = 14;
    let columns;
    let drops;

    function initMatrix() {
        columns = Math.floor(canvas.width / fontSize);
        drops = new Array(columns).fill(1);
    }
    initMatrix();

    function drawMatrix() {
        ctx.fillStyle = "rgba(0, 0, 0, 0.1)";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.font = fontSize + "px 'Share Tech Mono'";
        ctx.shadowColor = "transparent";
        ctx.shadowBlur = 0;
        ctx.fillStyle = "#00ff00";

        for (let i = 0; i < drops.length; i++) {
            const text = codeLines[Math.floor(Math.random() * codeLines.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);

            if (drops[i] * fontSize > canvas.height && Math.random() > 0.95) {
                drops[i] = 0;
            }

            drops[i]++;
        }
    }

    setInterval(drawMatrix, 45);
    </script>
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
