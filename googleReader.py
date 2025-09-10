import requests
from bs4 import BeautifulSoup

def extract_table_from_google_doc(url):
    # Fetch the document from the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find table data
    table = soup.find('table')
    
    # Read the table... if it's there
    if table:
        headerSkipped = False
        rows = []
        for tr in table.find_all('tr'):
            if (headerSkipped == False):
                headerSkipped = True
                continue
            row = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
            rows.append(row)
        return rows
    else:
        print("table not found!")
        return []

def print_letters(table_data):

    # Sort table by y's decending, then sort the x's ascending.
    sorted_table = sorted(table_data, key=lambda row: (-int(row[2]), int(row[0])))

    current_y = int(sorted_table[0][2])
    current_x = int(sorted_table[0][0])

    for i in range(0, len(sorted_table)):
        row = sorted_table[i]

        # Print a new line every time y changes. 
        new_y = int(row[2])
        if new_y < current_y:
            current_y = new_y
            print()
        
        # Add whitespace for every gap in x's. 
        new_x = int(row[0])
        x_diff = new_x - current_x
        if x_diff > 1:
            x_diff = x_diff - 1
            for _ in range(x_diff):
                print(" ", end="")

        # Print character. 
        print(f"{row[1]}", end="")
        current_x = new_x

    # End with a new line. 
    print()

url = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"
table_data = extract_table_from_google_doc(url)

print_letters(table_data)