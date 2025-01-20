from bson import ObjectId  # Import ObjectId from bson
import pymongo
import requests

# MongoDB setup
client = pymongo.MongoClient("mongodb+srv://chorkoccse2023:11281058@cluster0.b0nh98b.mongodb.net/")
db = client["sme_waiver"]
collection = db["user_details"]

# Google Gemini API key
API_KEY = "AIzaSyCTvpqoQvxzUEEdrKVwe88wGHwePryWxj4"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyCTvpqoQvxzUEEdrKVwe88wGHwePryWxj4"

def chatbot_interface():
    print("\nHello! I'm your SME Tax Waiver Assistant. Let's get started!")
    while True:
        print("\nHow can I assist you today?")
        print("1. Add User Inputs")
        print("2. Modify User Inputs")
        print("3. Analyze Data with AI")
        print("4. List All Records")
        print("5. Exit")

        choice = input("Select an option by typing the number: ").strip()

        if choice == "1":
            add_user_inputs_chatbot()
        elif choice == "2":
            modify_user_inputs_chatbot()
        elif choice == "3":
            analyze_data_with_ai_chatbot()
        elif choice == "4":
            list_all_records()
        elif choice == "5":
            print("Goodbye! Have a great day!")
            break
        else:
            print("\nInvalid input. Please select a valid option (1-5).")

def add_user_inputs_chatbot():
    print("\nGreat! Let's add some details about your business.")
    business_sector = input("What is the nature of your business? (e.g., Food Industry, Textiles): ")
    annual_turnover = float(input("What is your annual turnover? (in INR): "))
    subsidies = input("Are you availing any government subsidies or schemes? (Yes/No): ").strip().lower()
    state = input("In which state is your business registered? (e.g., Tamil Nadu, Maharashtra): ")

    user_data = {
        "business_sector": business_sector,
        "annual_turnover": annual_turnover,
        "subsidies": subsidies,
        "state": state
    }

    result = collection.insert_one(user_data)
    print(f"\nData saved successfully to MongoDB. Your record ID is: {result.inserted_id}")

def modify_user_inputs_chatbot():
    user_id = input("\nPlease provide the ID of the user record you want to modify: ")
    try:
        user_data = collection.find_one({"_id": ObjectId(user_id)})

        if not user_data:
            print("Sorry, no data found for the given ID.")
            return

        print("\nAlright, let's modify your data. Press Enter to keep existing values.")
        updated_data = {}
        for key, value in user_data.items():
            if key == "_id":
                continue
            new_value = input(f"{key} (Current: {value}): ")
            updated_data[key] = new_value if new_value else value

        collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})
        print("\nYour data has been successfully updated.")
    except Exception as e:
        print(f"Error: {e}")

def analyze_data_with_ai_chatbot():
    user_id = input("\nPlease provide the ID of the user record you want to analyze: ")
    try:
        user_data = collection.find_one({"_id": ObjectId(user_id)})

        if not user_data:
            print("Sorry, no data found for the given ID.")
            return

        user_payload = {
            "business_sector": user_data["business_sector"],
            "annual_turnover": user_data["annual_turnover"],
            "subsidies": user_data["subsidies"],
            "state": user_data["state"]
        }

        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        response = requests.post(API_URL, json=user_payload, headers=headers)
        response.raise_for_status()
        suggestions = response.json().get("suggestions", [])

        print("\nHere's what I found based on your data:")
        if suggestions:
            for suggestion in suggestions:
                print(f"- {suggestion}")
        else:
            print("No specific suggestions available at this time. Please try again later.")
    except requests.exceptions.RequestException as e:
        print(f"Oops! Something went wrong while communicating with the AI: {e}")
    except Exception as e:
        print(f"Error: {e}")

def list_all_records():
    print("\nHere are all the records in the database:")
    try:
        for record in collection.find():
            print(f"ID: {record['_id']} | Business Sector: {record['business_sector']} | State: {record['state']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    chatbot_interface()
