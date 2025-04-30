import json
import random
import re
import os
import logging
import requests
from flask import Flask, request, jsonify, render_template, session
from fuzzywuzzy import process

app = Flask(__name__)

# Set Secret Key for Sessions
app.secret_key = os.getenv("SECRET_KEY", "your_fallback_secret_key")

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Load scrap prices from JSON file
json_path = os.path.join(os.path.dirname(__file__), "scrap_prices.json")
with open(json_path, "r", encoding="utf-8") as file:
    scrap_data = json.load(file)

scrap_dict = {item["Name"].lower(): item for item in scrap_data}

agents = [
    {"name": "Ramesh Kumar", "contact": "98765 43210", "vehicle": "AP 23 AB 4567"},
    {"name": "Suresh Verma", "contact": "91234 56789", "vehicle": "TS 09 CD 7890"},
    {"name": "Vikram Singh", "contact": "87876 54321", "vehicle": "KA 05 EF 1234"},
]

# Helper function to parse price (handles both single values and ranges)
def parse_price(price_str):
    try:
        if " - " in price_str:
            lower_bound = float(price_str.split(" - ")[0].strip())
            return lower_bound, f"₹{price_str}"
        else:
            return float(price_str), f"₹{price_str}"
    except ValueError as e:
        logging.error(f"Error parsing price: {price_str}, Error: {e}")
        return 0.0, "₹0.00"

@app.route("/")
def home():
    session.clear()
    return render_template("index.html")

@app.route("/get_price", methods=["POST"])
def get_price():
    data = request.json
    user_input = data.get("material", "").strip().lower()
    logging.debug(f"Received user input: {user_input}, Current state: {session.get('state')}")

    # Initialize session state
    if "state" not in session:
        session["state"] = "start"
        session["booking_attempted"] = False

    state = session["state"]

    if state == "start":
        if user_input in ["yes", "y"]:
            session["state"] = "ask_scrap_type"
            session["booking_attempted"] = False
            material_examples = ", ".join(list(scrap_dict.keys())[:5])
            return jsonify({
                "response": f"Awesome! What type of scrap do you have? For example: {material_examples}.",
                "image": None
            })
        elif user_input in ["no", "n"]:
            return jsonify({
                "response": "No worries! If you change your mind, I'm here to help with your recycling needs. 😊",
                "image": None
            })
        else:
            return jsonify({
                "response": "Please type 'Yes' or 'No' to let me know if you have any scrap!",
                "image": None
            })

    elif state == "ask_scrap_type":
        closest_match, confidence = process.extractOne(user_input, scrap_dict.keys())
        if confidence > 70:
            item = scrap_dict[closest_match]
            session["scrap_type"] = item["Name"]
            session["price"] = item["Price"]
            session["state"] = "ask_quantity"
            _, price_display = parse_price(item["Price"])
            return jsonify({
                "response": f"The price of {item['Name']} is {price_display} per {item['Unit']}.\n\nHow much quantity do you have in KGs?",
                "image": item["Image URL"]
            })
        else:
            material_examples = ", ".join(list(scrap_dict.keys())[:5])
            return jsonify({
                "response": f"Sorry, I couldn't find that material. Try something like: {material_examples}.",
                "image": None
            })

    elif state == "ask_quantity":
        try:
            quantity = float(user_input)
            if quantity <= 0:
                return jsonify({
                    "response": "Please enter a valid quantity greater than zero.",
                    "image": None
                })
            session["quantity"] = quantity
            price_value, _ = parse_price(session["price"])
            total_price = quantity * price_value
            session["total_price"] = total_price
            session["state"] = "ask_name"
            return jsonify({
                "response": f"Your estimated total price is ₹{total_price:.2f}.\n\nMay I have your name, please?",
                "image": None
            })
        except ValueError:
            return jsonify({
                "response": "Please enter a valid quantity in numbers (e.g., 5).",
                "image": None
            })

    elif state == "ask_name":
        if user_input.strip():
            session["name"] = user_input.strip()
            session["state"] = "ask_phone"
            return jsonify({
                "response": "Thank you! Please provide your phone number (10 digits, e.g., 9876543210).",
                "image": None
            })
        else:
            return jsonify({
                "response": "Please enter a valid name.",
                "image": None
            })

    elif state == "ask_phone":
        phone_regex = r"^\d{10}$"
        if re.match(phone_regex, user_input):
            session["phone"] = user_input
            session["state"] = "ask_email"
            return jsonify({
                "response": "Got it! Please provide your email address.",
                "image": None
            })
        else:
            return jsonify({
                "response": "Please enter a valid 10-digit phone number (e.g., 9876543210).",
                "image": None
            })

    elif state == "ask_email":
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(email_regex, user_input):
            session["email"] = user_input
            session["state"] = "ask_address"
            return jsonify({
                "response": "Thanks! Please provide your address (house number, street, city, state).",
                "image": None
            })
        else:
            return jsonify({
                "response": "Please enter a valid email address (e.g., example@domain.com).",
                "image": None
            })

    elif state == "ask_address":
        if user_input.strip():
            session["address"] = user_input.strip()
            session["state"] = "ask_pincode"
            return jsonify({
                "response": "Great! Please provide your pincode.",
                "image": None
            })
        else:
            return jsonify({
                "response": "Please enter a valid address (house number, street, city, state).",
                "image": None
            })

    elif state == "ask_pincode":
        pincode_regex = r"^\d{6}$"
        if re.match(pincode_regex, user_input):
            session["pincode"] = user_input
            session["state"] = "confirm_booking"
            return jsonify({
                "response": "Thank you! Do you want to proceed with booking? (Yes/No)",
                "image": None
            })
        else:
            return jsonify({
                "response": "Please enter a valid 6-digit pincode (e.g., 123456).",
                "image": None
            })

    elif state == "confirm_booking":
        if user_input in ["yes", "y"]:
            session["state"] = "ask_time_slot"
            return jsonify({
                "response": "What time slot do you prefer for pickup? (e.g., 10 AM - 12 PM or 14:00 - 16:00)",
                "image": None
            })
        elif user_input in ["no", "n"]:
            return jsonify({
                "response": "Okay, let me know if you need assistance later. Thank you! 😊",
                "image": None
            })
        else:
            return jsonify({
                "response": "Please answer Yes or No.",
                "image": None
            })

    elif state == "ask_time_slot":
        time_format_12hr = r"^\d{1,2} ?(AM|PM|am|pm) ?- ?\d{1,2} ?(AM|PM|am|pm)$"
        time_format_24hr = r"^\d{2}:\d{2} ?- ?\d{2}:\d{2}$"

        if re.match(time_format_12hr, user_input) or re.match(time_format_24hr, user_input):
            logging.debug("Time slot validated successfully")
            session["time_slot"] = user_input
            session["state"] = "address_change"

            booking_id = f"BK{random.randint(1000,9999)}"
            customer_id = f"CUST{random.randint(1000,9999)}"
            assigned_agent = random.choice(agents)

            session["booking_id"] = booking_id
            session["customer_id"] = customer_id
            session["agent"] = assigned_agent

            # Prepare data for Google Sheets
            _, price_display = parse_price(session["price"])
            total_price = session.get("total_price", 0.0)
            booking_data = {
                "bookingId": booking_id,
                "customerId": customer_id,
                "name": session["name"],
                "phone": session["phone"],
                "email": session["email"],
                "address": session["address"],
                "pincode": session["pincode"],
                "timeSlot": session["time_slot"],
                "material": session["scrap_type"],
                "quantity": session["quantity"],
                "pricePerUnit": price_display,
                "estimatedTotalPrice": f"₹{total_price:.2f}",
                "agentName": assigned_agent["name"],
                "agentContact": assigned_agent["contact"],
                "agentVehicle": assigned_agent["vehicle"]
            }

            # Send data to Google Sheets web app
            google_sheets_url = "https://script.google.com/macros/s/AKfycbx8gFe-bl-Xf6vnaOxwD2fZmYrhMMPrb4VUFsdt7cd3sM4GVtL1o_Gyq9jKVMPqhziu8Q/exec"  # Replace with your deployed URL
            try:
                response = requests.post(google_sheets_url, json=booking_data)
                if response.status_code != 200:
                    logging.error(f"Failed to save to Google Sheets: {response.text}")
                    return jsonify({
                        "response": "Sorry, there was an issue saving your booking. Please try again later.",
                        "image": None
                    })
                logging.debug("Successfully sent data to Google Sheets")
            except Exception as e:
                logging.error(f"Error sending data to Google Sheets: {e}")
                return jsonify({
                    "response": "Sorry, there was an issue saving your booking. Please try again later.",
                    "image": None
                })

            # Prepare response
            response = f"""
📌 **Booking Confirmed!** 🎉\n
🔹 **Booking ID:** {booking_id}\n
🆔 **Customer ID:** {customer_id}\n\n
👤 **Customer Details:**\n
📛 Name: {session['name']}\n
📞 Phone: {session['phone']}\n
📧 Email: {session['email']}\n\n
🏠 **Pickup Details:**\n
📍 Address: {session['address']}\n
📮 Pincode: {session['pincode']}\n
⏰ Time Slot: {session['time_slot']}\n\n
📦 **Scrap Details:**\n
🗑️ Material: {session['scrap_type']}\n
⚖️ Quantity: {session['quantity']} KGs\n
💰 Estimated Price: ₹{total_price:.2f}\n\n
👨‍🔧 **Agent Details:**\n
👤 Name: {assigned_agent['name']}\n
📞 Contact: {assigned_agent['contact']}\n
🚛 Vehicle Number: {assigned_agent['vehicle']}\n\n
Do you want to change the address? (Yes/No)
"""
            logging.debug("Sending booking confirmation response")
            return jsonify({
                "response": response,
                "image": None
            })
        else:
            return jsonify({
                "response": "❌ Invalid time format! Please enter a valid time slot.\n\nExamples:\n- `10 AM - 12 PM`\n- `14:00 - 16:00`",
                "image": None
            })

    elif state == "address_change":
        if user_input in ["yes", "y"]:
            session["state"] = "ask_address"
            return jsonify({
                "response": "Please provide your new address (house number, street, city, state).",
                "image": None
            })
        elif user_input in ["no", "n"]:
            session["state"] = "thank_you"
            return jsonify({
                "response": "✅ Thank you! Your pickup is confirmed.\n\nWe appreciate your contribution to recycling! ♻️",
                "image": None
            })
        else:
            return jsonify({
                "response": "Please answer Yes or No.",
                "image": None
            })

    elif state == "thank_you":
        return jsonify({
            "response": "Your booking is already confirmed. Thank you! 😊",
            "image": None
        })

    return jsonify({
        "response": "I'm not sure how to proceed. Let's start over!",
        "image": None
    })

if __name__ == "__main__":
    app.run(debug=True)