import requests

# Replace this with the actual URL
url = 'http://192.168.1.43:8000/home/areas/'

data_list = [
    "Mamurdi",
    "Gahunje",
    "Kiwale",
    "Ravet",
    "Akurdi",
    "Punawale",
    "Tathawade",
    "Kasarsai",
    "Wakad",
    "Marunji",
    "Hinjawadi Phase 1",
    "Hinjawadi Phase 2",
    "Hinjawadi Phase 3",
    "Pimple Saudagar",
    "Pimple Gurav",
    "New Sanghavi",
    "Pimple Nilakh",
    "Balewadi",
    "Baner",
    "Sus",
    "Mahalunge",
    "Pashan",
    "Bavdhan",
    "Warje",
    "Kothrud",
    "Aundh"
]

formatted_version = 1  # Change this if necessary

for name in data_list:
    data = {
        "formatted_version": formatted_version,
        "name": name
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        print(f"Data for '{name}' posted successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to post data for '{name}': {e}")

