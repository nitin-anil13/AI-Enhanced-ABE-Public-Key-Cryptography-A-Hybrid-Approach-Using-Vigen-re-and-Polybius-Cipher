from flask import Flask, request, jsonify, render_template
from cryptography.fernet import Fernet
from cryptography.fernet import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_email():
    data = request.json
    recipient_email = data.get('email')
    key = data.get('key')
    message = data.get('message')

    if not recipient_email or not key or not message:
        return jsonify({'success': False, 'error': 'Missing required fields.'}), 400

    try:
        # Generate Fernet key from user-provided key (pad to 32 bytes)
        padded_key = key.encode().ljust(32, b'0')
        fernet_key = Fernet(base64.urlsafe_b64encode(padded_key))
        encrypted_message = fernet_key.encrypt(message.encode()).decode()

        # Email credentials (use app password)
        sender_email = 'rahulshu123ssipmt@gmail.com'
        sender_password = 'ckaf iwca irkq zkdw'

        # Compose email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = 'Encrypted Message'
        msg.attach(MIMEText(encrypted_message, 'plain'))

        # Send email securely using SMTP with TLS
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        return jsonify({'success': True, 'message': 'Encrypted email sent successfully!'})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
