import argparse
import urllib.request
import csv
import logging
from datetime import datetime
import sys

def downloadData(url):
    """Downloads the data"""
    #url = 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv'
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('utf-8')
        return data

def processData(file_content):
    #a = 'Hi my name
    a_dictionary = {}
    for x in file_content.splitlines():
        a = x.split(",")
        iDstring = a[0] #key
        nameString = a[1]
        DateString = a[2] #turn into date object
        try:
            DateObject = datetime.strptime(DateString, '%d/%m/%Y')
            a_dictionary.update({iDstring: [nameString, DateObject]})
        except ValueError:
            logging.error("Error processing line  # 27 for ID #" + iDstring)
            print("got a bad date value")
            #?what about the names with NO bdays entered....catch?

    print(a_dictionary)
    return a_dictionary

def displayPerson(id, personData):
    dictionary_value = personData.get(id)
    if dictionary_value == None :
        print("No user found with that id")
    else:
        print("Person " + id + " is " + dictionary_value[0] + " with a birthday of " + dictionary_value[1].strftime("%Y-%m-%d"))

def main(url, id):
    logging.basicConfig(filename='errors.log', filemode='w', format='%(name)s -%(levelname)s %(message)s')
    print(f"Running main with URL = {url}...")
    while int(id) >= 0:
        try:
            csvData = downloadData(url)
        except Exception:
            print("There has been a problem. The program will now exit.")
            sys.exit()
        #print(csvData)

        personData = processData(csvData)
        print(personData)
        displayPerson(id, personData)
        id = str(input("please enter another id"))
    sys.exit()

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    parser.add_argument("--id", help="id to the associated person", type=str, required=True)
    args = parser.parse_args()
    main(args.url, args.id)

