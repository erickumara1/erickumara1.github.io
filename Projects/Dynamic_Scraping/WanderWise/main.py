import scrape

exit = ""
while exit != "Exit": 
    from_place = input("from:")
    to_place = input("to:")
    print("MM/DD/YYYY Format for Dates")
    departure_date = input("departure date:")
    return_date = input("return date:")
    number = int(input("number of passengers:"))


    scrape.run(from_place,to_place,departure_date,return_date,number)

    exit = input("Type 'Exit' to exit or rescrape new entry")





