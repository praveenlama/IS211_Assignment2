# Praveen Lama
# IS 211
# Assignment 2
# Fall 2017

import sys
import argparse
import logging
import urllib2
import csv
import datetime

def main():
    logging.basicConfig(file_name='error.log')

    # function to return the file from url
    def downloadData(url):
        file = urllib2.urlopen(url)
        return file

    # function to process the data from csv file and return a formatted data
    def processData(data):
        storeResults = {} # dictionary to store the processed data
        file = csv.reader(data)
        date_format = '%d/%m/%Y'

        for row in file:
            if row[0] == 'id':
                continue
            else:
                try:
                    row[2] = datetime.datetime.strptime(row[2], date_format)

                except ValueError:
                    line_num = int(row[0]) + 1
                    userID = int(row[0])
                    # logging error for lines which cannot be processed
                    logger = logging.getLogger('assignment_2')
                    logger.error('Error processing line #{} for ID #{}'.format(line_num, userID))

                finally:
                    storeResults[int(row[0])] = (row[1], row[2])

        print 'TOTAL USERS: {}'.format(len(storeResults))
        return storeResults

    # function to display person's information by id
    def displayPerson(id, Database):

        try:
            response = 'USER #{idnum} : {name} : {date}'
            print response.format(idnum=id, name=Database[id][0], date=Database[id][1])
        except KeyError:
            print 'USER NOT FOUND'

    # main function, the parser will parse the --url argument from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='Fetching the CSV')
    args = parser.parse_args()
    logging.basicConfig(filename='error.log', level=logging.ERROR)

    # if url argument is passed
    if args.url:
        csvData = downloadData(args.url)
        usersRecord = processData(csvData)
        prompt = 'Enter an ID # for User Info. Or <= 0 to exit. '

        while True:
            try:
                userInput = int(raw_input(prompt))
            except ValueError:
                logging.info('Invalid USER ID');
                print 'Invalid USER ID. Please try again.'
                continue

            if userInput > 0:
                displayPerson(userInput, usersRecord)
            else:
                print 'Ending Program ...'
                sys.exit()
    else:
        print 'Please run the program with an url Argument. Example python test.py --url urlpath'


if __name__ == '__main__':
    main()