import time
from playwright.sync_api import sync_playwright

#format of google time from XhrYmin to just minutes
def google_time_format(time_in):
    time_in = time_in.split("hr")
    time_in[1] = time_in[1].replace("min","")
    h = int(time_in[0])
    m = int(time_in[1])
    return str(h*60+m)

def scrape_google(from_place,to_place,departure_date,return_date,number):
    with sync_playwright() as pw:
        browser = pw.firefox.launch(headless=False,)
        page = browser.new_page()
        page.goto('https://www.google.com/travel/flights?hl=en-US&curr=USD')

        #edits to have the appropriate number of adults
        adults = page.query_selector_all('.k0gFV')[0]
        adults.click()
        time.sleep(2)
        button = page.query_selector_all('button[aria-label="Add adult"]')[0]
        for i in range(number-1):
            button.click()
            time.sleep(1)
        done = page.query_selector_all('button[jsname="McfNlf"]')[0]
        done.click()
        time.sleep(1)

        #fill in from entry
        from_place_field = page.query_selector_all('.e5F5td')[0]
        from_place_field.click()
        time.sleep(1)
        from_place_field.type(from_place)
        time.sleep(1)
        page.keyboard.press('Enter')
        time.sleep(1)

        #fill in to entry
        to_place_field = page.query_selector_all('.e5F5td')[1]
        to_place_field.click()
        time.sleep(1)
        to_place_field.type(to_place)
        time.sleep(1)
        page.keyboard.press('Enter')
        time.sleep(1)

        #fill in departure date entry
        departure_date_field = page.query_selector_all('[jsname="yrriRe"] [aria-label="Departure"]')[0]
        departure_date_field.click()
        time.sleep(1)
        departure_date_field.type(departure_date)
        time.sleep(1)
        page.keyboard.press('Enter')
        time.sleep(1)
        page.query_selector('.WXaAwc .VfPpkd-LgbsSe').click()
        time.sleep(1)

        #fill in return date entry
        return_date_field = page.query_selector_all('[jsname="yrriRe"] [aria-label="Return"]')[0]
        return_date_field.click()
        time.sleep(1)
        return_date_field.type(return_date)
        time.sleep(1)
        page.query_selector('.WXaAwc .VfPpkd-LgbsSe').click()
        time.sleep(1)

        page.query_selector('.MXvFbd .VfPpkd-LgbsSe').click()
        time.sleep(4)

        #clicks the show more element button 
        page.query_selector('.zISZ5c button').click()
        time.sleep(4)

        page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        flights = page.locator('div.yR1fYc').all()

        file = open("google.txt","w")
        for f in flights:
            try:
                f = f.all_inner_texts()[0].split("\n")
                f[1] = f[1].split(" ")[0]
                line = ""
                if f[1]!='Self' and '$' in str(f[-2]):
                    time_in = str(f[2]).replace(" ","")
                    line = str(f[1]) + ";" + google_time_format(time_in) + ";" + str(f[-2][1:]).replace(",","") + "\n"
                #cases of selt transfer flights, they deviate from the usual pattern
                elif f[1]=='Self' and '$' in str(f[-3]):
                    time_in = str(f[3]).replace(" ","")
                    line = str(f[2]) + ";" +google_time_format(time_in) + ";" + str(f[-3][1:]).replace(",","") + "\n"
                print(line)
                file.write(line)
            except:
                continue
        file.close()

if __name__ == "__main__":
    from_place = "Detroit"
    to_place = "Boston"
    departure_date = "1/9/2025"    
    return_date = "1/12/2025"
    number = 3
    scrape_google(from_place,to_place,departure_date,return_date,number)