import time
import pandas as pd
import matplotlib.pyplot as plt

# from playwright.sync_api import sync_playwright
# from datetime import datetime
from kayak_flight import scrape_kayak
from google_flight import scrape_google
from airbnb import scrape_airbnb
from expedia import scrape_expedia

def scrape(from_place,to_place,departure_date,return_date,number):
    try:
        print("Scraping Google Flight")
        scrape_google(from_place,to_place,departure_date,return_date,number)
        time.sleep(2)
        print("Done")
    except:
        print("Error in Google Scraping")

    try:
        print("Scraping Kayak")
        scrape_kayak(from_place,to_place,departure_date,return_date,number)
        time.sleep(2)
        print("Done")
    except:
        print("Error in Kayak Scraping")

    try:
        print("Scraping Airbnb")
        scrape_airbnb(from_place,to_place,departure_date,return_date,number)
        time.sleep(2)
        print("Done")
    except:
        print("Error in Airbnb Scraping")

    try:
        print("Scraping Expedia")
        scrape_expedia(from_place,to_place,departure_date,return_date,number)
        time.sleep(2)
        print("Done")
    except:
        print("Error in Expedia Scraping")

def reading_files():
    file_names = ["google.txt","kayak.txt","airbnb.txt","expedia.txt"]
    tables = []
    for f in file_names:
        print(f)
        file = open(f,'r')
        lines = file.readlines()
        table = []
        for l in lines:
            l = l.replace("\n","")
            l = l.split(";")
            if len(l) == 4:
                l = l[1:]
            table.append(l)
        if f == "google.txt" or f == "kayak.txt":
            table = pd.DataFrame(table, columns=['Airline','Minutes','Cost'])
        else:
            table = pd.DataFrame(table, columns=['Name','Rating','Cost'])
        tables.append(table)
    return tables

def compare_site(table_1, name_1, table_2, name_2, element):
    fig, axes = plt.subplots(1, 2, figsize=(12, 6), sharey=True)
    table_1.plot(y=element, kind='bar', ax=axes[0], legend=False, color='skyblue')
    axes[0].set_title(name_1 + ' ' + element)
    axes[0].set_ylabel(element)
    axes[0].xaxis.set_visible(False)
    axes[0].axhline(y=table_1[element].mean(), color='black', linestyle='--', linewidth=1.5, label='Average') 
    table_2.plot(y=element, kind='bar', ax=axes[1], legend=False, color='orange')
    axes[1].set_title(name_2 + ' ' + element)
    axes[1].set_ylabel(element)
    axes[1].xaxis.set_visible(False)
    axes[1].axhline(y=table_2[element].mean(), color='black', linestyle='--', linewidth=1.5, label='Average') 
    fig.legend(['Average'], loc='upper right', ncol=2)
    fig.suptitle('Comparison of ' + element + ' Between ' + name_1 + ' and ' + name_2, fontsize=16)
    plt.tight_layout()
    plt.show()

def hotel_choice(airbnb,expedia):
    hotel_key = ""
    while hotel_key not in ['Cost','Rating','Rating per Dollar']:
        print("What is most important in a Hotel? Type: 'Cost', 'Rating' or 'Rating per Dollar'")
        hotel_key = input()

    airbnb['Label'] = "Airbnb"
    expedia['Label'] = "Expedia"
    hotel_stacked = pd.concat([airbnb, expedia], ignore_index=True)

    if hotel_key == 'Cost':
        sorted_hotel = hotel_stacked.sort_values(by=hotel_key)
    else:
        sorted_hotel = hotel_stacked.sort_values(by=hotel_key, ascending=False)
    
    n_hotels = 15
    sorted_hotel = sorted_hotel.reset_index(drop=True)
    print(sorted_hotel.head(n_hotels))
    print("\n")
    return sorted_hotel.iloc[0]

def plane_choice(google,kayak):
    plane_key = ""
    while plane_key not in ['Cost','Flight Minutes','Cost per Hour Flying']:
        print("What is most important for Travel? Type: 'Cost', 'Flight Minutes' or 'Cost per Hour Flying'")
        plane_key = input()

    google['Label'] = "Google"
    kayak['Label'] = "Kayak"
    plane_stacked = pd.concat([google, kayak], ignore_index=True)

    sorted_plane = plane_stacked.sort_values(by=plane_key)
    
    n_planes = 15
    sorted_plane = sorted_plane.reset_index(drop=True)
    print(sorted_plane.head(n_planes))
    print("\n")
    return sorted_plane.iloc[0]

def run(from_place, to_place, departure_date, return_date, number):
    #TESTING SCRAPING WITH THESE INPUTS IF CALLED FROM MAIN
    scrape(from_place,to_place,departure_date,return_date,number)
    tables = reading_files()

    #splitting tables by service
    # FLIGHTS
    google = tables[0]
    google['Cost'] = google['Cost'].astype('Int64')
    google['Flight Minutes'] = google['Minutes'].astype('Int64')
    google['Cost per Hour Flying'] = google['Cost']/google['Flight Minutes'] * 60
    google = google[google['Cost'] != 0].reset_index(drop=True)


    kayak = tables[1]
    kayak['Cost'] = kayak['Cost'].astype('Int64')
    kayak['Flight Minutes'] = kayak['Minutes'].astype('Int64')
    kayak['Cost per Hour Flying'] = kayak['Cost']/kayak['Flight Minutes'] * 60
    kayak = kayak[kayak['Cost'] != 0].reset_index(drop=True)

    # # HOTEL
    airbnb = tables[2]
    airbnb['Rating'] = airbnb['Rating'].astype(float)
    airbnb['Cost'] = airbnb['Cost'].astype('Int64')
    airbnb['Rating per Dollar'] = airbnb['Rating']/airbnb['Cost']
    airbnb = airbnb[airbnb['Cost'] != 0].reset_index(drop=True)


    expedia = tables[3]
    expedia['Rating'] = expedia['Rating'].astype(float)
    expedia['Cost'] = expedia['Cost'].astype('Int64')
    expedia['Rating per Dollar'] = expedia['Rating']/expedia['Cost']
    expedia = expedia[expedia['Cost'] != 0].reset_index(drop=True)

    # PLOTTING GOOGLE VS KAYAK COST, FLIGHT MINUTES and COST PER HOUR FLYING
    print("Comparing Flight Between Sites...")
    time.sleep(2)
    compare_site(google,"Google",kayak,"Kayak",'Cost')
    compare_site(google,"Google",kayak,"Kayak",'Flight Minutes')
    compare_site(google,"Google",kayak,"Kayak",'Cost per Hour Flying')

    # PLOTTING EXPEDIA VS AIRBNB COST, RATING AND RATING PER DOLLR
    # rating per dollar matters because a 4/5 hotel worth $400 is 
    # better value than a 5/5 hotel worth $800
    print("Comparing Hotels Between Sites...")
    time.sleep(2)
    compare_site(expedia,"Expedia",airbnb,"Airbnb",'Cost')
    compare_site(expedia,"Expedia",airbnb,"Airbnb",'Rating')
    compare_site(expedia,"Expedia",airbnb,"Airbnb",'Rating per Dollar')

    #Ask user which matters most in hotel: price, rating or rating per dollar
    #Ask user which matters most in flight: price, time or cost per hour flying +

    h_choice = hotel_choice(airbnb,expedia).to_frame().T
    p_choice = plane_choice(google,kayak).to_frame().T

    time.sleep(2)

    print("For your trip to " + to_place + " from " + departure_date + " to " + return_date + " with " + str(number) + " people")
    print("The best combination of hotel and flight is:")
    print(h_choice)
    print("\n")
    print(p_choice)

if __name__ == "__main__":
    
    from_place = "Detroit"
    to_place = "Boston"
    departure_date = "1/9/2025"    
    return_date = "1/12/2025"
    number = 3

    run(from_place, to_place, departure_date, return_date, number)