import re
from playwright.sync_api import sync_playwright
from datetime import datetime

def scrape_expedia(from_place, city_name, departure_date, return_date, n_adults):
    count = 0
    #sometimes expedia hangs and only gives 3 output
    # in that case, the website refreshes until output > 3
    while count <= 3: 
        with sync_playwright() as pw:
            browser = pw.firefox.launch(headless=False,)
            page = browser.new_page()

            depart_object = datetime.strptime(departure_date, "%m/%d/%Y")
            return_object = datetime.strptime(return_date, "%m/%d/%Y")

            start = depart_object.strftime("%Y-%m-%d")
            end = return_object.strftime("%Y-%m-%d")

            url = '''https://www.expedia.com/Hotel-Search?destination={city}&d1={d}&startDate={s}&d2={d}&endDate={d}&adults={n}&rooms=1&theme=&userIntent=&semdtl=&useRewards=false&sort=PRICE_LOW_TO_HIGH&children=&latLong=&mapBounds=&pwaDialog='''.format(
            city = city_name, s = start, d=end, n=n_adults)


            # Expedia has more elements the more the window scrolls down
            page.goto(url)
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight/4);")
            page.wait_for_timeout(2000)
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            page.wait_for_timeout(4000)

            #locate all entries and writes in file
            cards = page.locator('[data-stid="lodging-card-responsive"]').all()
            file = open("expedia.txt","w")
            count = 0

            for card in cards: 
                try:
                    content = card.locator('div.uitk-card-content-section')
                    title = content.locator('h3').text_content()
                    if content.locator('span.uitk-badge-base-text').is_visible():
                        rating = content.locator('span.uitk-badge-base-text').text_content()
                    else:
                        rating = False
                    if content.locator('div.uitk-type-200', has_text=re.compile(r"^.*total$")).is_visible():
                        total_price = content.locator('div.uitk-type-200', has_text=re.compile(r"^.*total$")).text_content()
                        total_price = total_price.split(" ")[0]
                    else:
                        total_price = False
                        

                    #compiled element into hotel list
                    hotel = {
                        'title': str(title),
                        'rating': str(rating),
                        'total':str(total_price)}
                    count+=1

                    
                    try:
                        line = hotel['title'] +";"+ hotel['rating']+";"+ hotel['total'][1:].replace(",","")+"\n"
                        if hotel['rating'] != 'False':
                            file.write(line)
                            print(line)
                    except:
                        line = "INVALID" +";"+ hotel['rating']+";"+ hotel['total'][1:].replace(",","")+"\n"
                        if hotel['rating'] != 'False':
                            file.write(line)
                            print(line)
                except: 
                    continue

            file.close()    
            browser.close()


if __name__ == "__main__":
    from_place = "New York"
    to_place = "Boston"
    departure_date = "1/9/2025"    
    return_date = "1/12/2025"
    number = 4
    scrape_expedia(from_place,to_place,departure_date,return_date,number)