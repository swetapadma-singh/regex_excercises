import requests
from bs4 import BeautifulSoup
import random
from groq import Groq

def scrape_site1():
    url = "http://books.toscrape.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    data = {}

    for item in soup.select("article.product_pod"):
        name = item.h3.a["title"]
        price = float(item.select_one(".price_color").text.replace("Â£", ""))
        data[name] = price

    return data

def scrape_site2(base_data):
    return {k: v + random.randint(-5, 10) for k, v in base_data.items()}

def scrape_site3(base_data):
    return {k: v + random.randint(-10, 15) for k, v in base_data.items()}

def scrape_site4(base_data):
    return {k: v + random.randint(-8, 12) for k, v in base_data.items()}

def compare_prices(sites_data):
    result = {}

    for product in sites_data[0]:
        prices = {}

        for i, site in enumerate(sites_data):
            prices[f"site{i+1}"] = site.get(product)

        best_site = min(prices, key=prices.get)

        result[product] = {
            "best_price": prices[best_site],
            "best_site": best_site,
            "all_prices": prices
        }

    return result

client = Groq()

def explain_results(data):
    prompt = f"""
    Here is product price comparison:

    {data}

    Explain:
    - Which site is cheapest overall
    - Any patterns you see
    - Keep it simple
    """

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return res.choices[0].message.content

site1 = scrape_site1()
site2 = scrape_site2(site1)
site3 = scrape_site3(site1)
site4 = scrape_site4(site1)

comparison = compare_prices([site1, site2, site3, site4])

for product, info in list(comparison.items())[:5]:
    print(f"\n{product}")
    print(info)

print(explain_results(comparison))