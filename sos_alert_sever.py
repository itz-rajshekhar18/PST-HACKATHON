from flask import Flask, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# Twilio Configuration
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

# Twilio Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/SOSpage', methods=['POST'])
def send_sos():
    try:
        # Extract data from the request
        data = request.json
        if not data:
            raise ValueError("No data provided in the request.")

        latitude = data.get('latitude')
        longitude = data.get('longitude')
        timestamp = data.get('timestamp')

        if not latitude or not longitude:
            raise ValueError("Latitude and Longitude are required.")

        # Construct the SOS message
        message_body = (
            f"\ud83d\udea8 SOS Alert \ud83d\udea8\n"
            f"Location: Latitude {latitude}, Longitude {longitude}\n"
            f"Timestamp: {timestamp}\nPlease assist immediately."
        )
        app.logger.info(f"Message body: {message_body}")

        # Replace with actual emergency contact numbers
        emergency_contacts = ["+1234567890", "+0987654321"]

        # Send the message to each contact
        for contact in emergency_contacts:
            client.messages.create(
                to=contact,
                from_=TWILIO_PHONE_NUMBER,
                body=message_body
            )
            app.logger.info(f"Message sent to {contact}")

        return jsonify({"status": "success", "message": "SOS alert sent successfully"}), 200

    except ValueError as ve:
        app.logger.error(f"Validation Error: {ve}")
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        app.logger.error(f"Unhandled Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)