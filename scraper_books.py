import requests
from bs4 import BeautifulSoup
import csv

# URL of the website to scrape
url = "http://books.toscrape.com/"

# Headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

# Open CSV file for writing
with open("books.csv", "w", newline='', encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the headers to the CSV file
    csv_writer.writerow([
        'Book Title', 'Price', 'Rating', 'Availability'
    ])

    # Send GET request to fetch the page content
    response = requests.get(url, headers=headers)
    
    # Check for successful response
    if response.status_code != 200:
        print(f"Failed to retrieve the page: {url}")
        exit()

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all books on the page
    books = soup.find_all("article", class_="product_pod")

    # Iterate over each book
    for book in books:
        # Extract book title
        title = book.find("h3").find("a")["title"]
        
        # Extract book price
        price = book.find("p", class_="price_color").get_text()
        
        # Extract book rating
        rating = book.find("p", class_="star-rating")["class"][1]
        
        # Extract availability status
        availability = book.find("p", class_="instock availability").get_text(strip=True)
        
        # Write the extracted information to CSV
        csv_writer.writerow([title, price, rating, availability])

    print("Scraping completed! Data saved to books.csv.")
