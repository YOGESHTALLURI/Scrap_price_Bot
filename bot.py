# # import json
# # import random
# # import re
# # from flask import Flask, request, jsonify, render_template
# # from fuzzywuzzy import process

# # app = Flask(__name__)

# # # Load scrap prices from JSON file
# # with open("scrap_prices.json", "r", encoding="utf-8") as file:
# #     scrap_data = json.load(file)

# # scrap_dict = {item["Name"].lower(): item for item in scrap_data}

# # agents = [
# #     {"name": "Ramesh Kumar", "contact": "+91 98765 43210", "vehicle": "AP 23 AB 4567"},
# #     {"name": "Suresh Verma", "contact": "+91 91234 56789", "vehicle": "TS 09 CD 7890"},
# #     {"name": "Vikram Singh", "contact": "+91 87876 54321", "vehicle": "KA 05 EF 1234"},
# # ]

# # user_sessions = {}

# # @app.route("/")
# # def home():
# #     return render_template("index.html")

# # @app.route("/get_price", methods=["POST"])
# # def get_price():
# #     data = request.json
# #     user_id = data.get("user_id", "default")
# #     user_input = data.get("material", "").strip().lower()

# #     if user_id not in user_sessions:
# #         user_sessions[user_id] = {"state": "start"}

# #     state = user_sessions[user_id]["state"]

# #     if state == "start":
# #         if user_input in ["yes", "y"]:
# #             user_sessions[user_id]["state"] = "ask_scrap_type"
# #             return jsonify({"response": "Great! What type of scrap do you have?"})
# #         elif user_input in ["no", "n"]:
# #             return jsonify({"response": "Alright! Let me know if you need help later. Thank you!"})
# #         else:
# #             return jsonify({"response": "Please answer Yes or No."})

# #     elif state == "ask_scrap_type":
# #         closest_match, confidence = process.extractOne(user_input, scrap_dict.keys())
# #         if confidence > 70:
# #             item = scrap_dict[closest_match]
# #             user_sessions[user_id]["scrap_type"] = item["Name"]
# #             user_sessions[user_id]["price"] = item["Price"]
# #             user_sessions[user_id]["state"] = "ask_quantity"
# #             return jsonify({"response": f"The price of {item['Name']} is ₹{item['Price']} per {item['Unit']}.\n\nHow much quantity do you have in KGs?"})
# #         else:
# #             return jsonify({"response": "Sorry, I couldn't find that material. Try another one."})

# #     elif state == "ask_quantity":
# #         try:
# #             quantity = float(user_input)
# #             user_sessions[user_id]["quantity"] = quantity
# #             total_price = quantity * float(user_sessions[user_id]["price"])
# #             user_sessions[user_id]["state"] = "confirm_booking"
# #             return jsonify({"response": f"Your estimated total price is ₹{total_price:.2f}.\n\nDo you want to proceed with booking? (Yes/No)"})
# #         except ValueError:
# #             return jsonify({"response": "Please enter a valid quantity in numbers."})

# #     elif state == "confirm_booking":
# #         if user_input in ["yes", "y"]:
# #             user_sessions[user_id]["state"] = "ask_address"
# #             return jsonify({"response": "Please provide your address for pickup."})
# #         elif user_input in ["no", "n"]:
# #             return jsonify({"response": "Okay, let me know if you need assistance later. Thank you!"})
# #         else:
# #             return jsonify({"response": "Please answer Yes or No."})

# #     elif state == "ask_address":
# #         user_sessions[user_id]["address"] = user_input
# #         user_sessions[user_id]["state"] = "ask_time_slot"
# #         return jsonify({"response": "What time slot do you prefer for pickup? (e.g., 10 AM - 12 PM or 14:00 - 16:00)"})

# #     elif state == "ask_time_slot":
# #         time_format_12hr = r"^\d{1,2} ?(AM|PM|am|pm) ?- ?\d{1,2} ?(AM|PM|am|pm)$"
# #         time_format_24hr = r"^\d{2}:\d{2} ?- ?\d{2}:\d{2}$"

# #         if re.match(time_format_12hr, user_input) or re.match(time_format_24hr, user_input):
# #             user_sessions[user_id]["time_slot"] = user_input
# #             user_sessions[user_id]["state"] = "address_change"

# #             booking_id = f"BK{random.randint(1000,9999)}"
# #             customer_id = f"CUST{random.randint(1000,9999)}"
# #             assigned_agent = random.choice(agents)

# #             user_sessions[user_id]["booking_id"] = booking_id
# #             user_sessions[user_id]["customer_id"] = customer_id
# #             user_sessions[user_id]["agent"] = assigned_agent

# #             return jsonify({
# #                 "response": f"""
# # 📌 **Booking Confirmed!** 🎉\n
# # 🔹 **Booking ID:** {booking_id}\n
# # 🆔 **Customer ID:** {customer_id}\n\n
# # 🏠 **Pickup Details:**\n
# # 📍 Address: {user_sessions[user_id]['address']}\n
# # ⏰ Time Slot: {user_sessions[user_id]['time_slot']}\n\n
# # 📦 **Scrap Details:**\n
# # 🗑️ Material: {user_sessions[user_id]['scrap_type']}\n
# # ⚖️ Quantity: {user_sessions[user_id]['quantity']} KGs\n
# # 💰 Estimated Price: ₹{user_sessions[user_id]['quantity'] * float(user_sessions[user_id]['price']):.2f}\n\n
# # 👨‍🔧 **Agent Details:**\n
# # 👤 Name: {assigned_agent['name']}\n
# # 📞 Contact: {assigned_agent['contact']}\n
# # 🚛 Vehicle Number: {assigned_agent['vehicle']}\n\n
# # Do you want to change the address? (Yes/No)
# # """
# #             })
# #         else:
# #             return jsonify({"response": "❌ Invalid time format! Please enter a valid time slot.\n\nExamples:\n- `10 AM - 12 PM`\n- `14:00 - 16:00`"})

# #     elif state == "address_change":
# #         if user_input in ["yes", "y"]:
# #             user_sessions[user_id]["state"] = "ask_address"
# #             return jsonify({"response": "Please provide your new address."})
# #         elif user_input in ["no", "n"]:
# #             user_sessions[user_id]["state"] = "thank_you"
# #             return jsonify({"response": "✅ Thank you! Your pickup is confirmed.\n\nWe appreciate your contribution to recycling! ♻️"})
# #         else:
# #             return jsonify({"response": "Please answer Yes or No."})

# #     elif state == "thank_you":
# #         return jsonify({"response": "Your booking is already confirmed. Thank you! 😊"})

# #     return jsonify({"response": "I'm not sure how to proceed. Let's start over!"})

# # if __name__ == "__main__":
# #     app.run(debug=True)

# import json
# import random
# import re
# from flask import Flask, request, jsonify, render_template
# from fuzzywuzzy import process

# app = Flask(__name__)

# # Load scrap prices from JSON file
# with open("scrap_prices.json", "r", encoding="utf-8") as file:
#     scrap_data = json.load(file)

# scrap_dict = {item["Name"].lower(): item for item in scrap_data}

# agents = [
#     {"name": "Ramesh Kumar", "contact": "+91 98765 43210", "vehicle": "AP 23 AB 4567"},
#     {"name": "Suresh Verma", "contact": "+91 91234 56789", "vehicle": "TS 09 CD 7890"},
#     {"name": "Vikram Singh", "contact": "+91 87876 54321", "vehicle": "KA 05 EF 1234"},
# ]

# user_sessions = {}

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/get_price", methods=["POST"])
# def get_price():
#     data = request.json
#     user_id = data.get("user_id", "default")
#     user_input = data.get("material", "").strip().lower()

#     # ✅ Fix: Reset session only when the user starts a new conversation
#     if user_id not in user_sessions or user_sessions[user_id]["state"] == "thank_you":
#         user_sessions[user_id] = {"state": "start"}

#     state = user_sessions[user_id]["state"]

#     if state == "start":
#         if user_input in ["yes", "y"]:
#             user_sessions[user_id]["state"] = "ask_scrap_type"
#             return jsonify({"response": "Great! What type of scrap do you have?"})
#         elif user_input in ["no", "n"]:
#             return jsonify({"response": "Alright! Let me know if you need help later. Thank you!"})
#         else:
#             return jsonify({"response": "Please answer Yes or No."})

#     elif state == "ask_scrap_type":
#         closest_match, confidence = process.extractOne(user_input, scrap_dict.keys())
#         if confidence > 70:
#             item = scrap_dict[closest_match]
#             user_sessions[user_id]["scrap_type"] = item["Name"]
#             user_sessions[user_id]["price"] = item["Price"]
#             user_sessions[user_id]["state"] = "ask_quantity"
#             return jsonify({"response": f"The price of {item['Name']} is ₹{item['Price']} per {item['Unit']}.\n\nHow much quantity do you have in KGs?"})
#         else:
#             return jsonify({"response": "Sorry, I couldn't find that material. Try another one."})

#     elif state == "ask_quantity":
#         try:
#             quantity = float(user_input)
#             user_sessions[user_id]["quantity"] = quantity
#             total_price = quantity * float(user_sessions[user_id]["price"])
#             user_sessions[user_id]["state"] = "confirm_booking"
#             return jsonify({"response": f"Your estimated total price is ₹{total_price:.2f}.\n\nDo you want to proceed with booking? (Yes/No)"} )
#         except ValueError:
#             return jsonify({"response": "Please enter a valid quantity in numbers."})

#     elif state == "confirm_booking":
#         if user_input in ["yes", "y"]:
#             user_sessions[user_id]["state"] = "ask_address"
#             return jsonify({"response": "Please provide your address for pickup."})
#         elif user_input in ["no", "n"]:
#             return jsonify({"response": "Okay, let me know if you need assistance later. Thank you!"})
#         else:
#             return jsonify({"response": "Please answer Yes or No."})

#     elif state == "ask_address":
#         user_sessions[user_id]["address"] = user_input
#         user_sessions[user_id]["state"] = "ask_time_slot"
#         return jsonify({"response": "What time slot do you prefer for pickup? (e.g., 10 AM - 12 PM or 14:00 - 16:00)"})

#     elif state == "ask_time_slot":
#         time_format_12hr = r"^\d{1,2} ?(AM|PM|am|pm) ?- ?\d{1,2} ?(AM|PM|am|pm)$"
#         time_format_24hr = r"^\d{2}:\d{2} ?- ?\d{2}:\d{2}$"

#         if re.match(time_format_12hr, user_input) or re.match(time_format_24hr, user_input):
#             user_sessions[user_id]["time_slot"] = user_input
#             user_sessions[user_id]["state"] = "address_change"

#             booking_id = f"BK{random.randint(1000,9999)}"
#             customer_id = f"CUST{random.randint(1000,9999)}"
#             assigned_agent = random.choice(agents)

#             user_sessions[user_id]["booking_id"] = booking_id
#             user_sessions[user_id]["customer_id"] = customer_id
#             user_sessions[user_id]["agent"] = assigned_agent

#             return jsonify({
#                 "response": f"""
# 📌 **Booking Confirmed!** 🎉\n
# 🔹 **Booking ID:** {booking_id}\n
# 🆔 **Customer ID:** {customer_id}\n\n
# 🏠 **Pickup Details:**\n
# 📍 Address: {user_sessions[user_id]['address']}\n
# ⏰ Time Slot: {user_sessions[user_id]['time_slot']}\n\n
# 📦 **Scrap Details:**\n
# 🗑️ Material: {user_sessions[user_id]['scrap_type']}\n
# ⚖️ Quantity: {user_sessions[user_id]['quantity']} KGs\n
# 💰 Estimated Price: ₹{user_sessions[user_id]['quantity'] * float(user_sessions[user_id]['price']):.2f}\n\n
# 👨‍🔧 **Agent Details:**\n
# 👤 Name: {assigned_agent['name']}\n
# 📞 Contact: {assigned_agent['contact']}\n
# 🚛 Vehicle Number: {assigned_agent['vehicle']}\n\n
# Do you want to change the address? (Yes/No)
# """
#             })
#         else:
#             return jsonify({"response": "❌ Invalid time format! Please enter a valid time slot.\n\nExamples:\n- `10 AM - 12 PM`\n- `14:00 - 16:00`"})

#     elif state == "address_change":
#         if user_input in ["yes", "y"]:
#             user_sessions[user_id]["state"] = "ask_address"
#             return jsonify({"response": "Please provide your new address."})
#         elif user_input in ["no", "n"]:
#             user_sessions[user_id]["state"] = "thank_you"
#             return jsonify({"response": "✅ Thank you! Your pickup is confirmed.\n\nWe appreciate your contribution to recycling! ♻️"})
#         else:
#             return jsonify({"response": "Please answer Yes or No."})

#     elif state == "thank_you":
#         return jsonify({"response": "Your booking is already confirmed. Thank you! 😊"})

#     return jsonify({"response": "I'm not sure how to proceed. Let's start over!"})

# if __name__ == "__main__":
#     app.run(debug=True)

import json
import random
import re
import os
from flask import Flask, request, jsonify, render_template, session
from fuzzywuzzy import process

app = Flask(__name__)

# ✅ Step 1: Set Secret Key for Sessions
app.secret_key = os.getenv("SECRET_KEY", "your_fallback_secret_key")  # Use a secure key

# Load scrap prices from JSON file
json_path = os.path.join(os.path.dirname(__file__), "scrap_prices.json")
with open(json_path, "r", encoding="utf-8") as file:
    scrap_data = json.load(file)

scrap_dict = {item["Name"].lower(): item for item in scrap_data}

agents = [
    {"name": "Ramesh Kumar", "contact": "+91 98765 43210", "vehicle": "AP 23 AB 4567"},
    {"name": "Suresh Verma", "contact": "+91 91234 56789", "vehicle": "TS 09 CD 7890"},
    {"name": "Vikram Singh", "contact": "+91 87876 54321", "vehicle": "KA 05 EF 1234"},
]

@app.route("/")
def home():
    session.clear()  # ✅ Step 2: Clears session on page reload
    return render_template("index.html")

@app.route("/get_price", methods=["POST"])
def get_price():
    data = request.json
    user_input = data.get("material", "").strip().lower()

    # ✅ Step 3: Initialize session state if it's a new session
    if "state" not in session:
        session["state"] = "start"

    state = session["state"]

    if state == "start":
        if user_input in ["yes", "y"]:
            session["state"] = "ask_scrap_type"
            return jsonify({"response": "Great! What type of scrap do you have?"})
        elif user_input in ["no", "n"]:
            return jsonify({"response": "Alright! Let me know if you need help later. Thank you!"})
        else:
            return jsonify({"response": "Please answer Yes or No."})

    elif state == "ask_scrap_type":
        closest_match, confidence = process.extractOne(user_input, scrap_dict.keys())
        if confidence > 70:
            item = scrap_dict[closest_match]
            session["scrap_type"] = item["Name"]
            session["price"] = item["Price"]
            session["state"] = "ask_quantity"
            return jsonify({"response": f"The price of {item['Name']} is ₹{item['Price']} per {item['Unit']}.\n\nHow much quantity do you have in KGs?"})
        else:
            return jsonify({"response": "Sorry, I couldn't find that material. Try another one."})

    elif state == "ask_quantity":
        try:
            quantity = float(user_input)
            session["quantity"] = quantity
            total_price = quantity * float(session["price"])
            session["state"] = "confirm_booking"
            return jsonify({"response": f"Your estimated total price is ₹{total_price:.2f}.\n\nDo you want to proceed with booking? (Yes/No)"} )
        except ValueError:
            return jsonify({"response": "Please enter a valid quantity in numbers."})

    elif state == "confirm_booking":
        if user_input in ["yes", "y"]:
            session["state"] = "ask_address"
            return jsonify({"response": "Please provide your address for pickup."})
        elif user_input in ["no", "n"]:
            return jsonify({"response": "Okay, let me know if you need assistance later. Thank you!"})
        else:
            return jsonify({"response": "Please answer Yes or No."})

    elif state == "ask_address":
        session["address"] = user_input
        session["state"] = "ask_time_slot"
        return jsonify({"response": "What time slot do you prefer for pickup? (e.g., 10 AM - 12 PM or 14:00 - 16:00)"})

    elif state == "ask_time_slot":
        time_format_12hr = r"^\d{1,2} ?(AM|PM|am|pm) ?- ?\d{1,2} ?(AM|PM|am|pm)$"
        time_format_24hr = r"^\d{2}:\d{2} ?- ?\d{2}:\d{2}$"

        if re.match(time_format_12hr, user_input) or re.match(time_format_24hr, user_input):
            session["time_slot"] = user_input
            session["state"] = "address_change"

            booking_id = f"BK{random.randint(1000,9999)}"
            customer_id = f"CUST{random.randint(1000,9999)}"
            assigned_agent = random.choice(agents)

            session["booking_id"] = booking_id
            session["customer_id"] = customer_id
            session["agent"] = assigned_agent

            return jsonify({
                "response": f"""
📌 **Booking Confirmed!** 🎉\n
🔹 **Booking ID:** {booking_id}\n
🆔 **Customer ID:** {customer_id}\n\n
🏠 **Pickup Details:**\n
📍 Address: {session['address']}\n
⏰ Time Slot: {session['time_slot']}\n\n
📦 **Scrap Details:**\n
🗑️ Material: {session['scrap_type']}\n
⚖️ Quantity: {session['quantity']} KGs\n
💰 Estimated Price: ₹{session['quantity'] * float(session['price']):.2f}\n\n
👨‍🔧 **Agent Details:**\n
👤 Name: {assigned_agent['name']}\n
📞 Contact: {assigned_agent['contact']}\n
🚛 Vehicle Number: {assigned_agent['vehicle']}\n\n
Do you want to change the address? (Yes/No)
"""
            })
        else:
            return jsonify({"response": "❌ Invalid time format! Please enter a valid time slot.\n\nExamples:\n- `10 AM - 12 PM`\n- `14:00 - 16:00`"})

    elif state == "address_change":
        if user_input in ["yes", "y"]:
            session["state"] = "ask_address"
            return jsonify({"response": "Please provide your new address."})
        elif user_input in ["no", "n"]:
            session["state"] = "thank_you"
            return jsonify({"response": "✅ Thank you! Your pickup is confirmed.\n\nWe appreciate your contribution to recycling! ♻️"})
        else:
            return jsonify({"response": "Please answer Yes or No."})

    elif state == "thank_you":
        return jsonify({"response": "Your booking is already confirmed. Thank you! 😊"})

    return jsonify({"response": "I'm not sure how to proceed. Let's start over!"})

if __name__ == "__main__":
    app.run(debug=True)

