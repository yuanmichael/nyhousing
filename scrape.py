import requests
from collections import defaultdict
import webbrowser

# TODO: Filter to exclude Bronx locations
# TODO: output the URLs in a list. Then open each of them in a web browser


def scrape_ids():
    # web scraping set up
    url = "https://a806-housingconnectapi.nyc.gov/HPDPublicAPI/api/Lottery/SearchLotteries"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    # required POST fields, per Dev Tools. The "search lottery" header
    data = {
    "UnitTypes": [],
    "NearbyPlaces": [],
    "NearbySubways": [],
    "Amenities": [],
    "Boroughs": [],
    "Neighborhoods": [],
    "HouseholdSize": 1,
    "Income": 57000,
    "HouseholdType": 1,
    "OwnerTypes": [],
    "Min": None,
    "Max": None,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    response = response.json()["rentals"]
    
    # output is a nested dictionary. Keys are ID #s. Sub-dicts are the key-value pairs that we're interested in. Like listing ID, name, end date, etc.
    num_listings = len(response) # confirmed that there are 39 listings
    output_dict = defaultdict(dict)
    keys_to_extract = ["lotteryId", "lotteryName", "endIn", "minIncome", "maxIncome", "lotteryEndDate", "trains", "amenities"]
        
    # parse through each of the 39 dictionaries. Append only the keys that we're interested in
    for listing in response:
        id = listing["lotteryId"]

        update_dict = {key: listing[key] for key in keys_to_extract}

        output_dict[id].update(update_dict)
        output_dict[id].update({
            "url": f"https://housingconnect.nyc.gov/PublicWeb/details/{id}"
            })


    # print function
    for key, values in output_dict.items():
        print(key)
        for a, b in values.items():
            print(f"{a}: {b}")
        print()
    
    print(len(output_dict.keys()))

    #output_list = list(output_dict.keys())
    #print(output_list)
    #print(type(output_list))
    #return output_list

    # output the urls only

    return (output_dict)


# open the URLs from the scraped IDs
def open_urls(output_dict):
    for key, values in output_dict.items():
        url = output_dict[key]["url"]
        webbrowser.open(url)


# function to grab the important details from a listing, given the ID# 
def get_url(id):
    url = f"https://a806-housingconnectapi.nyc.gov/HPDPublicAPI/api/Lottery/GetLotteryAdvertisement?lotteryid={id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        data = None

    # grab data for this listing
    name = data["lotteryName"]
    end_date = data["endDate"]
    address = data["lotteryBuildings"][0]["address"]
    city = data["lotteryBuildings"][0]["city"]
    address = address + ", " + city 

    url_link = f"https://housingconnect.nyc.gov/PublicWeb/details/{id}"

    print(name) 
    print(end_date)
    print(address)
    print(url_link)
    print()

    if end_date == "null":
        exit()




def main():
    output_dict = scrape_ids()
    open_urls(output_dict)

main()