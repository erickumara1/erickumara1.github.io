import time
from playwright.sync_api import sync_playwright
from datetime import datetime

def scrape_airbnb(from_place, to_place, departure_date, return_date, number):
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=False,)
        depart_object = datetime.strptime(departure_date, "%m/%d/%Y")
        return_object = datetime.strptime(return_date, "%m/%d/%Y")

        page = browser.new_page()
        url = 'https://www.airbnb.com/s/{city}/homes?checkin={d}&checkout={r}&adults={n}'.format(
                city = to_place, 
                d = depart_object.strftime("%Y-%m-%d"), 
                r = return_object.strftime("%Y-%m-%d"), 
                n= str(number))
        
        page.goto(url)
        
        file = open("airbnb.txt","w")
        num_pages = 3
        #it clicks on the next page num_pages time and scrapes the website
        for i in range(num_pages):
            time.sleep(6)
            #locator for entry 
            cards = page.locator('div[class="c4mnd7m atm_9s_11p5wf0 atm_dz_1osqo2v dir dir-ltr"]').all()
            for c in cards:
                c = c.all_inner_texts()[0].split("\n")
                try:
                    rating = float(c[-1].split(" ")[0]) * 2
                    rating = str(rating)
                    price = c[-4].split(" ")[0]
                    # name of airbnb is a collection of the description
                    # airbnb names are usually 'lovely home of 2....' and not a recognizable brand like
                    # Hilton suites, need to find a unique identifier
                    name =  c[2] + "-" + c[3]
                    if c[2]!="Free cancellation":
                        line = name+";"+rating+";"+price[1:].replace(",","")+ "\n"
                        print(line)
                        file.write(line)
                except:
                    continue
            time.sleep(3)
            page.click('a[aria-label="Next"]')
        file.close()

    