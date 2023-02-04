#Homework1
#Ghaida Alshiddi
#This program runs the file data.csv and orgnizes
# the data and stores them in a new file
#CS 4395
#2/4/2O23

import sys
import pathlib
import re
import pickle
import nltk
nltk.download("all")
from nltk import word_tokenize
from nltk import sent_tokenize

#Person class has 5 fields: first, last and middle names, employee id, and phone
# the class has a display function to display the employee info, including the 5 fields
class Person:
    def __init__(self, last, first, mi, id_, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id_ = id_
        self.phone = phone#self.text.split()

    def display(self):
        print('\n')
        print('Employee id: ', self.id_)
        print(self.first, ' ', self.mi, ' ', self.last)
        print(self.phone)

#this function takes a list of strings 'line' and processes it using for loop and nlkt functions
def process_lines(line):
    d = {}
    #process each line (each employee)
    for i in line:
        #contains the data of the entire line (split comma from the data )
        tokens = i.split(',')
        #checks if first name is not capitalized and fix it when needed
        if not tokens[0].istitle():
            tokens[0] = tokens[0].title()
        # checks if last name is not capitalized and fix it when needed
        if not tokens[1].istitle():
            tokens[1] = tokens[1].title()
        # if there's no mi, assign value 'X'
        if tokens[2] == '':
            tokens[2] = 'X'
        # checks if mi is not capitalized and fix it when needed,
        elif not tokens[2].istitle():
            tokens[2] = tokens[2].title()
        #check if ID matches the format: 2 letter, and 4 digits
        m = re.match('\D\D\d\d\d\d', tokens[3])
        # id doesn't match the id format, ask user to type their id and save response
        if not m:
            print('ID invalid: ', tokens[3])
            print('ID is two letters followed by 4 digits')
            v = input('Please enter a valid id: ')
            tokens[3] = v
        #check phone number format
        m2 = re.match('\d\d\d-\d\d\d-\d\d\d\d', tokens[4])
        # phone doesn't match the format, ask user to type their phone with correct format and save response
        if not m2:
            print('Phone ', tokens[4], ' is invalid')
            print('Enter phone number in form 123-456-7890')
            val = input("Enter a correct phone number: ")
            tokens[4] = val
        #checks for duplicate ids
        for j in d.keys():
            if j==tokens[3]:
                print("ID already exists " , j)
                exit(0)
        # create a person object
        person = Person(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4])
        #creates a dict of employees
        d[person.id_] = person

    return d


if __name__ == '__main__':
    #checks for args
    if len(sys.argv)<2:
        print("Please enter a filename as sys arg")
        quit()
    rel_path=sys.argv[1]
    #takes the file lines and stores them as a list of strings
    with open(pathlib.Path.cwd().joinpath(rel_path), 'r') as f:
        text_in=f.read().splitlines()
    # passes the list in the process_line function
    employees= process_lines(text_in[1:])
    #create a pickle file and read it
    pickle.dump(employees,open("employees.pickle", 'wb'))
    employees_in = pickle.load(open('employees.pickle', 'rb'))

    print('\n\nEmployee list:')
    #prints employees data
    for emp_id in employees_in.keys():
        employees_in[emp_id].display()
