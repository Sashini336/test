import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_automoto_bg():
    url = "https://automoto.bg/listings/search?type_id=1&order=1&person=1&firm=2&coupe_id=&door_id=&mark_id=10&fuel_id=&speed_id=&year_id=&year_id_to=&price_for=&price_to=&power_from=&power_to=&color_id=&where_been=&area_id=23&place_id=111&condition_new=1"

    data = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.find_all("div", class_="result-item-data")

        for item in items:

            name_element = item.find("a", class_="col-md-4")
            name = name_element.text.strip() if name_element else "N/A"

            year_element = item.find("div", class_="col-md-2")
            year = year_element.text.strip() if year_element else "N/A"

            price_element = item.find("div", class_="col-md-3").find(
                "div", class_="result-item-pricing").find("div", class_="price")
            price = price_element.text.strip() if price_element else "N/A"

            region_element = item.find(
                "div", class_="col-md-3").find("div", class_="region")
            region = region_element.text.strip() if region_element else "N/A"

            data.append({"Name": name, "Year": year,
                        "Price": price, "Region": region})

        df = pd.DataFrame(data)

        print(df)

        file_name = "automoto_bg_data.csv"
        df.to_csv(file_name, index=False)

        print(f"Data successfully scraped and saved to {file_name}.")
    else:
        print("Failed to fetch data. Status code:", response.status_code)

    return df


if __name__ == "__main__":
    scraped_data = scrape_automoto_bg()
