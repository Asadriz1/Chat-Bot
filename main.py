# Import necessary libraries
import os
import openai
from metaphor_python import Metaphor

# Initialize API keys
openai.api_key = os.getenv("OPENAI_API_KEY")  # Use your OpenAI API key
metaphor = Metaphor(os.getenv("METAPHOR_API_KEY"))  # Use your Metaphor API key

# Function to ask for user preferences
def get_user_preferences():
    print("Welcome to the Real Estate Advisor!")
    print("Please answer a few questions to help us find the best properties for you.")

    location = input("1. Enter the location you are interested in: ")
    price_range = input("2. Enter your price range (e.g., $100,000 - $500,000): ")
    bedrooms = input("3. Number of bedrooms (e.g., 2): ")
    bathrooms = input("4. Number of bathrooms (e.g., 2): ")

    return {
        "location": location,
        "price_range": price_range,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms
    }

# Function to search for real estate listings
def search_real_estate_listings(user_preferences):
    query = f"Real estate listings in {user_preferences['location']} with {user_preferences['bedrooms']} bedrooms and {user_preferences['bathrooms']} bathrooms within {user_preferences['price_range']} price range"

    search_options = {
        "query": query,
        "num_results": 5  # You can adjust this number as needed
    }
    search_response = metaphor.search(**search_options)

    return search_response.results

# Function to summarize text using OpenAI
def summarize_text(text):
    summary = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Summarize the following text: '{text}'",
        max_tokens=50  # Adjust the max_tokens as needed
    ).choices[0].text

    return summary

# Main function
def main():
    user_preferences = get_user_preferences()

    real_estate_listings = search_real_estate_listings(user_preferences)

    if not real_estate_listings:
        print("Sorry, no real estate listings found based on your preferences.")
        return

    print("\nHere are some real estate listings that match your preferences:")

    for idx, listing in enumerate(real_estate_listings, start=1):
        print(f"\nListing {idx}:")
        print(f"Location: {listing.location}")
        print(f"Price: {listing.price}")
        print(f"Bedrooms: {listing.bedrooms}")
        print(f"Bathrooms: {listing.bathrooms}")
        print(f"Description: {listing.extract}")

        # Summarize the description
        summary = summarize_text(listing.extract)
        print(f"Summarized Description: {summary}")

if __name__ == "__main__":
    main()
