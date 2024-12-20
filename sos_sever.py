from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
from twilio.rest import Client 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#SQLite Database Configuration
db_file = 'sos_alerts.db'

def init_db():
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                latitude REAL,
                longitude REAL,
                timestamp TEXT
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Database and table initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

twilio_sid = 'your_twilio_sid'
twilio_auth_token = 'your_twilio_auth_token'
twilio_phone_number = 'your_twilio_phone_number'
emergency_phone_number = '911_phone_number_or_other_contact'

def send_sms(latitude,longitude,timestamp):
    client = Client(twilio_sid, twilio_auth_token)
    message = client.messages.create(
        body= f"Emergency Alert: SOS Alert received. Location: Lat: {latitude}, Long: {longitude}, Timestamp: {timestamp}",
        from_= twilio_phone_number,
        to=emergency_phone_number
    )
    print(f"Message sent with SID: {message.sid}")
        
@app.route('/sos-alert', methods=['POST'])
def sos_alert():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        timestamp = data.get('timestamp', datetime.utcnow().isoformat())
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts (latitude, longitude, timestamp) 
            VALUES (?, ?, ?)
        ''', (latitude, longitude, timestamp))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "SOS alert recorded successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)