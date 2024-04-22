'''
https://pynative.com/python-random-number-generation-exercise-questions-and-challenge/#h-exercise-1-generate-3-random-integers-between-100-and-999-which-is-divisible-by-5

Exercise 2: Random Lottery Pick. Generate 100 random lottery tickets and pick two lucky tickets from it as a winner.

Note you must adhere to the following conditions:

    The lottery number must be 10 digits long.
    All 100 ticket number must be unique.

'''

# Solved by Gejnemin Huskic
# www.gejnem.in

import random
import json
import validator_collection
from tabulate import tabulate


# Class LotteryTicket generates a ticket ID number, and a boolean value stating if it is a winning ticket or not.
class LotteryTicket():
    def __init__(self):
        temp = self.lottery_number_generate()
        self.ticket_id = self.lottery_number_convert_to_string(temp)
        self.ticket_numbers_list = temp
        self.winning_ticket = self.generate_win_value()

    # method lottery_number_generate() returns a string with the following format:
    # ##-##-##-##-## (pound being a random integer 0-9)
    def lottery_number_generate(self):
        result = []
        for x in range(5):
            result.append(f"{random.choice(range(0, 10))}{random.choice(range(0, 10))}")
        return result

    # method lottery_number_convert_to_string() takes a list of numbers, returns a string with the list of appended
    # together with a dash inbetween each index value
    def lottery_number_convert_to_string(self, lottery_list):
        result = ""
        counter = 0
        for value in lottery_list:
            counter = counter + 1
            result = result + value
            # appends a dash to the final result, only if the current iteration is not the last.
            if counter < len(lottery_list):
                result = result + "-"
        return result

    # returns self.ticket_id
    def return_ticket_id(self):
        return self.ticket_id

    # returns self.ticket_numbers_list
    def return_ticket_list(self):
        return self.ticket_numbers_list

    # returns self.winning_ticket
    def return_winning_status(self):
        return self.winning_ticket

    # 2% chance to return boolean value True, 98% to return boolean value False
    def generate_win_value(self):
        result = False
        _ = random.choice(range(1, 101))
        if _ in [1, 2]:
            result = True
        return result


lottery_list = []  # array of objects created with the LotteryTicket() class
# lottery_dict = {}  # dict of objects created with the LotteryTicket() class
lottery_json = ""  # json of objects created with the LotteryTicket() class

# generate 100 LotteryTicket objects, and append them to a list, along with a string in json format
for x in range(1, 101):
    x = LotteryTicket()
    lottery_list.append(x)
    ticket_json = json.dumps(x.__dict__, indent=4)
    lottery_json = f"{lottery_json}\n{ticket_json}"

# write out the lottery_json variable as "lottery_tickets.json" in the same directory as this python file
with open("lottery_tickets.json", "w") as f:
    f.write(lottery_json)

# using lottery_list to create a pretty table and print it to the screen.
roll_number_string_list = [f"Roll {roll + 1}" for roll in range(0, (len(lottery_list) + 1))]
lottery_string = [ticket.ticket_id for ticket in lottery_list]
table = []
for x in range(0, (len(lottery_list))):
    table.append([roll_number_string_list[x], lottery_string[x]])
print(tabulate(table, tablefmt="psql", headers=["Roll #", "Ticket-ID"]))


# while-loop runs until the user inputs a value that meets the following criteria:
# follows this format exactly: ##-##-##-##-##
# if the variable passed is acceptable, the function returns True
def ticket_variable_validator(ticket_entry="gejnemin was here"):
    result = False
    # check to see if the player's choice contains any invalid characters:
    if validator_collection.is_string(ticket_entry):
        if validator_collection.has_length(value=ticket_entry, minimum=14, maximum=14):
            if "-" in ticket_entry:
                dash_index = [2, 5, 8, 11]
                number_index = [0, 1, 3, 4, 6, 7, 8, 9, 10, 12, 13]
                counter = 0
                suitable_input = True
                for character in ticket_entry:
                    if counter in dash_index:
                        if character == "-":
                            pass
                        else:
                            suitable_input = False
                    elif counter in number_index:
                        if validator_collection.is_numeric(character):
                            pass
                        else:
                            suitable_input = False
                    counter = counter + 1
                if suitable_input:
                    result = True
                else:
                    print("\n [!] The input does not match the necessary format.")
            else:
                print("\n [!] The input does not match the necessary format.")
        else:
            print("\n [!] The input must be 14 characters long")
    else:
        print("\n [!] The input must be a string.")
    return result


# example of an acceptable input: 11-11-11-11-11

attempts = 3
while attempts >= 1:
    print(f"\nPick the winning lottery ticket from the table above.\nEnter it in the following format: ##-##-##-##-##."
          f"\nYou have [{attempts}] attempt(s) left.")
    user_input = input(">>> ")
    if ticket_variable_validator(user_input):
        try:
            pulled_object = next(
                (obj for obj in lottery_list if obj.ticket_id == user_input)
            )
        except StopIteration as e:
            print("\n [!] There is no ticket with that ID. Try again...")
        else:
            if pulled_object.return_winning_status():
                print(f"\nYou picked the winning ticket!!!\n{user_input} is a winning roll!")
                print("Here is your prize: \n$$$\n$$$\n$$$")
                break
            else:
                attempts = attempts - 1
    else:
        pass
    if attempts <= 0:
        print("\nYou did not guess the winning ticket.\nBetter luck next time.")
