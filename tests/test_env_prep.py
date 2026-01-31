import requests
import os

# Get the directory where THIS script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Make sure the 'data' folder exists
data_dir = os.path.join(current_dir, "test_data")
os.makedirs(data_dir, exist_ok=True)  # creates folder if it doesn't exist

# URLs to download
urls = {
    "team_rocket.html": "https://bulbapedia.bulbagarden.net/wiki/Team_Rocket",
    "type.html": "https://bulbapedia.bulbagarden.net/wiki/Type"
}

# Download and save each HTML file
for filename, url in urls.items():
    response = requests.get(url)
    html_content = response.text
    file_path = os.path.join(data_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

print(f"HTML files downloaded to {data_dir}!")
