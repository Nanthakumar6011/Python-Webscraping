from bs4 import BeautifulSoup
import requests
import openpyxl

# Create an Excel workbook and active sheet
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "Movies List"
sheet.append(["Rank", "Movie Name", "Production"])  # Column headers

try:
    # Fetch the Wikipedia page
    response = requests.get("https://en.wikipedia.org/wiki/List_of_Tamil_films_of_2024")
    response.raise_for_status()  # Raise an HTTPError for bad responses

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate the table
    table = soup.find("table", class_="wikitable")
    rows = table.find("tbody").find_all("tr")  # Find all rows in the table

    # Iterate through rows and extract the relevant details
    for row in rows[1:]:  # Skip the header row
        cells = row.find_all("td")
        if len(cells) >= 3:  # Ensure there are enough columns
            rank = cells[0].text.strip()  # Rank column
            movie_name = cells[1].text.strip()  # Movie name column
            production = cells[2].text.strip()  # Production column

            print(f"Rank: {rank}, Movie Name: {movie_name}, Production: {production}")
            sheet.append([rank, movie_name, production])  # Append to Excel sheet

except Exception as e:
    print(f"An error occurred: {e}")

# Save the workbook
workbook.save("Movies_List.xlsx")
print("Movies list saved to 'Movies_List.xlsx'")
