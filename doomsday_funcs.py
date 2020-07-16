import random
import time
import sys
import re

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
months = ["January", "February", "March", "April", "May", "June",\
        "July", "August", "September", "October", "November", "December"]

# Class to hold values that can be changed during runtime from settings menu
class Settings:
    def __init__(self, min_year=1583, max_year=2500, saving=True, calendar="Gregorian"):
        self.min_year = min_year
        self.max_year = max_year
        self.saving = saving
        self.calendar = calendar
    def set_min_year(self, min_year):
        self.min_year = min_year
    def set_max_year(self, max_year):
        self.max_year = max_year
    def set_saving(self, saving):
        self.saving = saving
    def set_calendar(self, calendar):
        self.calendar = calendar
    def saving_string(self):
        return "On" if self.saving else "Off"

config = Settings()

def get_min_year():
    return config.min_year

def get_max_year():
    return config.max_year

def get_saving():
    return config.saving_string()

def get_calendar():
    return config.calendar

def is_leap(year):
    return (year%4 == 0) and ((year%100 != 0) or (year%400 == 0))

# What to do if month is not integer between 1 and 12?
def days_in_month(year,month):
    len_months = [31, 28+is_leap(year), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return len_months[month-1]

# Assumes year, month, and day are integers
def valid_date(year,month,day):
    return year > 0 and month >= 1 and month <= 12 and day >= 1 and day <= days_in_month(year,month)

# Assumes that a valid date is passed in.
# BCE is probably problematic.
def day_of_the_week(year, month, day):
    if config.calendar == "Gregorian":
        anchor = 2 + year + (year // 4) - (year // 100) + (year // 400)
    elif config.calendar == "Julian":
        anchor = year + year // 4
    day_zero = [4, 0, 0, 3, 5, 1, 3, 6, 2, 4, 0, 2]
    if is_leap(year):
        day_zero[0] = 3
        day_zero[1] = 6
    ans = (anchor + day_zero[month-1] + day) % 7
    return ans

# What if date is invalid?
def eng_date(year, month, day):
    if valid_date(year,month,day):
        return f"{months[month-1]} {day}, {year}"
    # else:
    #

def parse_date(string):
    # Returns year, month, day
    iso_format = re.compile("^\d{4,4}-\d{1,2}-\d{1,2}$")
    eng_format = re.compile("^\d{1,2}/\d{1,2}/\d{4,4}$")
    if iso_format.match(string) != None:
        lst = [int(x) for x in string.split("-")]
        return lst[0], lst[1], lst[2]
    elif eng_format.match(string) != None:
        lst = [int(x) for x in string.split("/")]
        return lst[2], lst[1], lst[0]
    else:
        return None

def practice():
    while True:
        # Randomly generate a date
        year = random.randint(config.min_year,config.max_year)
        month = random.randint(1,12)
        day = random.randint(1,days_in_month(year,month))

        # Display date
        print(eng_date(year,month,day))
        ans = day_of_the_week(year,month,day)
        # Measuring time taken for user response
        tic = time.perf_counter()
        while True:
            try:
                user_ans = int(input())
                if user_ans < 0 or user_ans > 6:
                    raise ValueError
                break
            except ValueError:
                print("Input should be an integer between 0 and 6.")
        toc = time.perf_counter()
        # Display answer and time
        print(f"Correct Answer: {days[ans]} ({ans})")
        print(f"Elapsed Time: {toc-tic:.1f} s")

        # Store statistics in a file
        is_correct = ans == user_ans
        N = 0
        if config.saving:
            with open("doomsday_stats.csv", "r+") as f:
                for line in f:
                    N += 1
                print(f"{N}, {is_correct}, {toc-tic:.3f}", file=f)

        # Go to next page
        while True:
            next_page = input("Continue [c], Return to Main Menu [m], or Exit [e] ")
            if next_page.lower() == "c":
                break
            elif next_page.lower() == "m":
                return None
            elif next_page.lower() == "e":
                exit_program()
            else:
                print("Invalid Option")

# Calculates the day of the week given the date as a string
def calendar():
    while True:
        try:
            date_str = input("Enter a date in YYYY-MM-DD or DD/MM/YYYY format. ")
            year, month, day = parse_date(date_str)
            if not valid_date(year,month,day):
                raise ValueError
            print(day_of_the_week(year,month,day))
        except TypeError:
            print("Not proper format")
        except ValueError:
            print("Not a valid date")
        while True:
            next_page = input("Continue with another date [c], Return to Main Menu [m], or Exit [e] ")
            if next_page.lower() == "c":
                break
            elif next_page.lower() == "m":
                return None
            elif next_page.lower() == "e":
                exit_program()
            else:
                print("Invalid Option")

# Displays times and correctness statistics from practices
def view_stats():
    print("Statistics")
    with open("doomsday_stats.csv", "r") as f:
        print(f.read())

    while True:
        next_page = input("Return to Main Menu [m], or Exit [e] ")
        if next_page.lower() == "m":
            return None
        elif next_page.lower() == "e":
            exit_program()
        else:
            print("Invalid Option")

def reset_stats():
    confirm = input("Confirm reset statistics [y/n] ")
    if confirm.lower() == "y":
        with open("doomsday_stats.csv", "w") as f:
            # Resets statistics file to contain only a header
            print("Problem Number, Correct?, Time (s)", file=f)
        print("Statistics Reset, Returning to Main Menu")
    else:
        print("Returning to Main Menu")
    return None

# Add more pages (Next page [n])
def tutorial():
    print("You will be presented with a date in the format Month Day, Year. Your task is to determine the day of the week on which that date occurred. Your answer should be a single-digit number as follows:")
    print("0: Sunday")
    print("1: Monday")
    print("2: Tuesday")
    print("3: Wednesday")
    print("4: Thursday")
    print("5: Friday")
    print("6: Saturday")
    while True:
        next_page = input("Return to Main Menu [m], or Exit [e] ")
        if next_page.lower() == "m":
            return None
        elif next_page.lower() == "e":
            exit_program()
        else:
            print("Invalid Option")

def settings():
    while True:
        print("Settings")
        print("Set range of years [s]")
        print("Set calendar [c]")
        print("Save results and times from practice [y/n]")
        print("Return to Main Menu [m], or Exit [e]")
        next_page = input()
        # Setting year range
        if next_page.lower() == "s":
            while True:
                try:
                    config.set_min_year(int(input("Minimum year? ")))
                    if config.min_year < 1583:
                        raise ValueError
                    break
                except ValueError:
                    print("Please input a positive integer for the year.")
            while True:
                try:
                    config.set_max_year(int(input("Maximum year? ")))
                    if config.max_year < config.min_year:
                        raise ValueError
                    break
                except ValueError:
                    print(f"Please input a year greater than the minimum year ({config.min_year}).")
        # Sets calendar to Gregorian or Julian
        elif next_page.lower() == "c":
            print("Set calendar to Gregorian [g] or Julian [j]?")
            while True:
                try:
                    calendar = input()
                    if calendar.lower() == "g":
                        config.set_calendar("Gregorian")
                        print("Calendar set to (proleptic) Gregorian")
                        break
                    elif calendar.lower() == "j":
                        config.set_calendar("Julian")
                        print("Calendar set to (proleptic) Julian")
                        break
                    else:
                        raise ValueError
                except ValueError:
                    print("Invalid Input")
        # Setting whether saving will occur
        elif next_page.lower() == "y":
            config.set_saving(True)
            print("Results and times will be saved")
        elif next_page.lower() == "n":
            config.set_saving(False)
            print("Results and times will not be saved")
        elif next_page.lower() == "m":
            return None
        elif next_page.lower() == "e":
            exit_program()
        else:
            print("Invalid Option")

def exit_program():
    sys.exit("Exiting.")
