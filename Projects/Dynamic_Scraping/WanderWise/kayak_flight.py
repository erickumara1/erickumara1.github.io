import time
from playwright.sync_api import sync_playwright
from datetime import datetime

us_cities_airports = {
    "New York": "JFK",
    "Los Angeles": "LAX",
    "Chicago": "ORD",
    "Houston": "IAH",
    "Phoenix": "PHX",
    "Philadelphia": "PHL",
    "San Antonio": "SAT",
    "San Diego": "SAN",
    "Dallas": "DFW",
    "San Jose": "SJC",
    "Austin": "AUS",
    "Jacksonville": "JAX",
    "Fort Worth": "DFW",
    "Columbus": "CMH",
    "Indianapolis": "IND",
    "Charlotte": "CLT",
    "San Francisco": "SFO",
    "Seattle": "SEA",
    "Denver": "DEN",
    "Washington": "DCA",
    "Boston": "BOS",
    "El Paso": "ELP",
    "Nashville": "BNA",
    "Detroit": "DTW",
    "Oklahoma City": "OKC",
    "Portland": "PDX",
    "Las Vegas": "LAS",
    "Memphis": "MEM",
    "Louisville": "SDF",
    "Baltimore": "BWI",
    "Milwaukee": "MKE",
    "Albuquerque": "ABQ",
    "Tucson": "TUS",
    "Fresno": "FAT",
    "Mesa": "PHX",  # Shares Phoenix's airport
    "Sacramento": "SMF",
    "Kansas City": "MCI",
    "Atlanta": "ATL",
    "Omaha": "OMA",
    "Colorado Springs": "COS",
    "Raleigh": "RDU",
    "Miami": "MIA",
    "Long Beach": "LGB",
    "Virginia Beach": "ORF",
    "Oakland": "OAK",
    "Minneapolis": "MSP",
    "Tulsa": "TUL",
    "Tampa": "TPA",
    "Arlington": "DFW",  # Shares Dallas's airport
    "New Orleans": "MSY",
    "Wichita": "ICT",
    "Cleveland": "CLE",
    "Bakersfield": "BFL",
    "Aurora": "DEN",  # Shares Denver's airport
    "Anaheim": "SNA",
    "Honolulu": "HNL",
    "Santa Ana": "SNA",
    "Riverside": "ONT",
    "Corpus Christi": "CRP",
    "Lexington": "LEX",
    "Henderson": "LAS",  # Shares Las Vegas's airport
    "Stockton": "SCK",
    "St. Paul": "MSP",  # Shares Minneapolis's airport
    "Cincinnati": "CVG",
    "St. Louis": "STL",
    "Pittsburgh": "PIT",
    "Greensboro": "GSO",
    "Lincoln": "LNK",
    "Anchorage": "ANC",
    "Plano": "DFW",  # Shares Dallas's airport
    "Orlando": "MCO",
    "Irvine": "SNA",
    "Newark": "EWR",
    "Durham": "RDU",
    "Chula Vista": "SAN",  # Shares San Diego's airport
    "Toledo": "TOL",
    "Fort Wayne": "FWA",
    "St. Petersburg": "PIE",  # Nearby Tampa Airport
    "Laredo": "LRD",
    "Jersey City": "EWR",  # Shares Newark's airport
    "Chandler": "PHX",
    "Madison": "MSN",
    "Lubbock": "LBB",
    "Scottsdale": "PHX",
    "Reno": "RNO",
    "Buffalo": "BUF",
    "Gilbert": "PHX",
    "Glendale": "PHX",
    "North Las Vegas": "LAS",
    "Winston-Salem": "INT",
    "Chesapeake": "ORF",
    "Norfolk": "ORF",
    "Fremont": "SJC",
    "Garland": "DFW",
    "Irving": "DFW",
    "Hialeah": "MIA",
    "Richmond": "RIC",
    "Boise": "BOI",
    "Spokane": "GEG",
    "Baton Rouge": "BTR",
    "Tacoma": "SEA"
}

#format the kayak time format from XhYm to just minutes
def kayak_time_format(time_in):
    time_in = time_in.split("h")
    time_in[1] = time_in[1].replace("m","")
    h = int(time_in[0])
    m = int(time_in[1])
    return str(h*60+m)

def scrape_kayak(from_place,to_place,departure_date,return_date,number):
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=False,)

        depart_object = datetime.strptime(departure_date, "%m/%d/%Y")
        return_object = datetime.strptime(return_date, "%m/%d/%Y")


        page = browser.new_page()
        url = '''https://www.kayak.com/flights/{city_s}-{city_d}/{d}/{r}/{n}adults?sort=bestflight_a'''.format(
            city_s= us_cities_airports[from_place], 
            city_d = us_cities_airports[to_place], 
            d = depart_object.strftime("%Y-%m-%d"), 
            r = return_object.strftime("%Y-%m-%d"), 
            n= str(number))
        page.goto(url)
        time.sleep(2)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)
        #click on show more button
        page.query_selector('.ULvh').click()
        time.sleep(2)
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(4)

        #flights are in a seperate div box and times in another
        #running into issues where each website has different conventions, hard coded page locator values for each site
        #starting to think web scraping flights is not feasible without AI
        flights = page.locator('div.zx8F-price-tile').all()
        flight_times = page.locator('div.xdW8').all()
        flights = zip(flights,flight_times)

        file = open("kayak.txt","w")
        for f  in flights:
            top = f[0].all_inner_texts()[0].split("\n")
            if top != ['']:
                bottom = f[1].all_inner_texts()[0].split("\n") 
                time_in =  str(bottom[0]).replace(" ","")
                entry = str(top[-2].split(" ")[0]) + ";" +  kayak_time_format(time_in) + ";" + str(top[2].split(" ")[0][1:]).replace(",","") + "\n"
                if '$' in str(top[2]):
                    print(entry)
                    file.write(entry)
            
        file.close()