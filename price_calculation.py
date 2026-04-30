import csv
import pdfplumber
import requests
from bs4 import BeautifulSoup
from groq import Groq

client = Groq(api_key="API_KEY")

# ---------------- CSV ----------------
def get_prices_from_csv(file):
    prices = []
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prices.append(int(row["price"]))
    return prices

# ---------------- PDF ----------------
def get_prices_from_pdf(file):
    prices = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for word in text.split():
                if word.isdigit():
                    prices.append(int(word))
    return prices

# ---------------- WEBSITE ----------------
def get_prices_from_website(url):
    prices = []
    while True:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, "html.parser")

        for tag in soup.find_all("p", class_="price_color"):
            value = tag.text.replace("Â£", "").strip()
            prices.append(float(value))
        next_btn = soup.find("li", class_="next")
        if next_btn:
            next_url = next_btn.find("a")["href"]
            url = url + next_url
        else:
            break        

    return prices

# ---------------- AI EXPLANATION ----------------
def explain_with_ai(all_prices):
    print("hello")
    prompt = f"""
        You are a calculator.

        Given this list of prices:
        {all_prices}

        Calculate:
        1. Total sum
        2. Average price
        3. Maximum price

        Do not skip any values.

        Return ONLY in this format:
        Sum: <value>
        Average: <value>
        Max: <value>

        Don't need to explain calculations. Only give the result.
        """

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[{"role": "user", "content": prompt}],
        max_completion_tokens=5000
    )

    return response.choices[0].message.content

# ---------------- MAIN ----------------
def main():
    all_prices = []

    try:
        csv_prices = get_prices_from_csv("prices1.csv")
        print("CSV Prices:", csv_prices)
        all_prices.extend(csv_prices)
    except:
        print("No csv file found, skipping...")    

    try:
        pdf_prices = get_prices_from_pdf("sample_prices_1.pdf")
        print("PDF Prices:", pdf_prices)
        all_prices.extend(pdf_prices)
    except:
        print("No PDF found, skipping...")

    try:
        url = "http://books.toscrape.com/"
        web_prices = get_prices_from_website(url)
        print("Website Prices:", web_prices)
        all_prices.extend(web_prices)
    except:
        print("Website scraping skipped")

    total = sum(all_prices)
    avg_val = total/len(all_prices)
    max_val = max(all_prices)
    print("\nTotal Price:", total)
    print("\nAverage Price:", avg_val)
    print("\nMaximum Price:", max_val)

    explanation = explain_with_ai(all_prices)
    print("\nAI Explanation:\n", explanation)


if __name__ == "__main__":
    main()