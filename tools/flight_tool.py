
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")


def search_flights(query):
    if not API_KEY:
        return "ERROR: AVIATIONSTACK_API_KEY not found. Check your .env file."

    url = "https://api.aviationstack.com/v1/flights"

    params = {
        "access_key": API_KEY,
        "limit": 5
    }

    try:
        response = requests.get(url, params=params, timeout=20)

        print("API Status Code:", response.status_code)

        response.raise_for_status()
        data = response.json()

        # Check API errors
        if "error" in data:
            error = data["error"]
            return (
                f"AviationStack API Error: "
                f"{error.get('code', 'Unknown')} - "
                f"{error.get('message', 'No details provided')}"
            )

        flight_records = data.get("data", [])

        if not flight_records:
            return "No live flight records returned by AviationStack."

        flights = []

        for flight in flight_records:
            airline = (flight.get("airline") or {}).get("name", "Unknown")
            departure = (flight.get("departure") or {}).get("airport", "Unknown")
            arrival = (flight.get("arrival") or {}).get("airport", "Unknown")
            status = flight.get("flight_status", "Unknown")

            flights.append(
                f"""
Airline: {airline}
Departure: {departure}
Arrival: {arrival}
Status: {status}
"""
            )

        return "\n".join(flights)

    except requests.exceptions.RequestException as e:
        return f"Flight API request failed: {str(e)}"

    except Exception as e:
        return f"Unexpected flight search error: {str(e)}"
