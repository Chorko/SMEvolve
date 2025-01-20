from bson import ObjectId  # Import ObjectId from bson
import pymongo
import requests

# MongoDB setup
client = pymongo.MongoClient("mongodb+srv://chorkoccse2023:11281058@cluster0.b0nh98b.mongodb.net/")
db = client["sme_waiver"]  # Updated database name
collection = db["user_details"]  # Updated collection name

# Google Gemini API key and URL
API_KEY = "AIzaSyCTvpqoQvxzUEEdrKVwe88wGHwePryWxj4"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def chatbot_interface():
    print("\nHello! I'm your SME Tax Waiver Assistant. Let's get started!")
    while True:
        print("\nHow can I assist you today?")
        print("1. Add User Inputs")
        print("2. Modify User Inputs")
        print("3. Analyze Data with AI")
        print("4. Ask Custom AI Prompt")
        print("5. Perform Market & Competitor Analysis")
        print("6. List All Records")
        print("7. Exit")

        choice = input("Select an option by typing the number: ").strip()

        if choice == "1":
            add_user_inputs_chatbot()
        elif choice == "2":
            modify_user_inputs_chatbot()
        elif choice == "3":
            analyze_data_with_ai_chatbot()
        elif choice == "4":
            ask_custom_ai_prompt()
        elif choice == "5":
            market_and_competitor_analysis()
        elif choice == "6":
            list_all_records()
        elif choice == "7":
            print("Goodbye! Have a great day!")
            break
        else:
            print("\nInvalid input. Please select a valid option (1-7).")

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

    try:
        result = collection.insert_one(user_data)  # Insert and get the result
        print(f"\nData saved successfully to MongoDB. Your record ID is: {result.inserted_id}")
    except Exception as e:
        print(f"Error saving data: {e}")

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

        # Generate a contextual search query
        query = {
            "contents": [{"parts": [{"text": (
                f"Analyze tax waivers for {user_data['business_sector']} in {user_data['state']} "
                f"with ₹{user_data['annual_turnover']} turnover, availing {user_data['subsidies']} subsidies.\n\n"
                f"Tax regimes include:\n\n"
                f"Food Industry:\n"
                f"- GST Slabs: 0% (Fresh fruits, vegetables, milk, eggs), 5% (Processed foods), 12% (Packaged foods, frozen goods).\n"
                f"- Waivers: GST exemption on basic unprocessed foods, Subsidies under PMEGP for food manufacturing units.\n\n"
                f"Clothing and Textiles:\n"
                f"- GST Slabs: 5% (Garments below ₹1000), 12% (Garments above ₹1000).\n"
                f"- Waivers: Reduced GST for cotton fabrics, State-level textile industry subsidies.\n\n"
                f"Handicrafts:\n"
                f"- GST Slabs: 0% (Traditional handicrafts and khadi), 5% (Artisan goods).\n"
                f"- Waivers: Market promotion schemes for handicrafts, GST exemption on bamboo products.\n\n"
                f"State-specific benefits:\n"
                f"Tamil Nadu: 15%-25% capital subsidies, Refund of state GST for MSMEs, Subsidized industrial land rates.\n"
                f"Maharashtra: 5% interest subsidies, Stamp duty exemptions, Lower electricity tariffs for MSMEs.\n"
                f"Uttar Pradesh: 20% capital investment subsidy, Wage subsidies for local workers."
            )}]}]
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(API_URL, json=query, headers=headers)
        response.raise_for_status()

        suggestions = response.json().get("candidates", [])

        print("\nHere's what I found based on your data:")
        if suggestions:
            for suggestion in suggestions:
                print(f"- {suggestion}")
        else:
            print("No specific tax waivers available at this time. Please try again later.")
    except requests.exceptions.RequestException as e:
        print(f"Oops! Something went wrong while communicating with the AI: {e}")
    except Exception as e:
        print(f"Error: {e}")

def ask_custom_ai_prompt():
    custom_prompt = input("\nEnter your custom prompt for AI analysis: ")
    try:
        query = {
            "contents": [{"parts": [{"text": custom_prompt}]}]
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(API_URL, json=query, headers=headers)
        response.raise_for_status()

        suggestions = response.json().get("candidates", [])

        print("\nAI Response to your custom prompt:")
        if suggestions:
            for suggestion in suggestions:
                print(f"- {suggestion}")
        else:
            print("No suggestions available. Please try again later.")
    except requests.exceptions.RequestException as e:
        print(f"Oops! Something went wrong while communicating with the AI: {e}")
    except Exception as e:
        print(f"Error: {e}")

def market_and_competitor_analysis():
    user_id = input("\nPlease provide the ID of the user record you want to analyze: ")
    try:
        user_data = collection.find_one({"_id": ObjectId(user_id)})

        if not user_data:
            print("Sorry, no data found for the given ID.")
            return

        business_sector = user_data['business_sector']
        print(f"\nAnalyzing market trends and competitors in the {business_sector} sector...")

        # Placeholder for market trend analysis and competitor research
        trends_query = f"Fetch trending hashtags and market insights for {business_sector} from social media."
        competitors_query = f"Provide a competitor analysis for {business_sector} in the current market."

        # For market analysis (social media trends related to the business sector)
        market_trends = ask_gemini(trends_query)
        print("\nMarket Trends based on social media data:")
        print(market_trends)

        # For competitor analysis (similar businesses in the sector)
        competitor_analysis = ask_gemini(competitors_query)
        print("\nCompetitor Analysis:")
        print(competitor_analysis)

    except Exception as e:
        print(f"Error: {e}")

def ask_gemini(query):
    headers = {"Content-Type": "application/json"}
    response = requests.post(API_URL, json={"contents": [{"parts": [{"text": query}]}]}, headers=headers)
    if response.status_code == 200:
        return response.json().get("candidates", "No suggestions available.")
    return "Error fetching data from Gemini API."

def list_all_records():
    print("\nHere are all the records in the database:")
    try:
        for record in collection.find():
            print(f"ID: {record['_id']} | Business Sector: {record['business_sector']} | State: {record['state']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    chatbot_interface()
