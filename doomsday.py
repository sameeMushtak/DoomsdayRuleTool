import random
import time
import sys

# Calculate statistics (percent correct, average time) for last n attempts
# Leaderboard of record times
# Code assumes existence of a doomsday_stats.csv file with header row already existing

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
months = ["January", "February", "March", "April", "May", "June",\
        "July", "August", "September", "October", "November", "December"]

class Settings:
    def __init__(self, min_year=1583, max_year=2500, saving=True):
        self.min_year = min_year
        self.max_year = max_year
        self.saving = saving
    def set_min_year(self, min_year):
        self.min_year = min_year
    def set_max_year(self, max_year):
        self.max_year = max_year
    def set_saving(self, saving):
        self.saving = saving
    def saving_string(self):
        return "On" if self.saving else "Off"

config = Settings()

# Assumes that a valid date is passed in.
# BCE is probably problematic.
def day_of_the_week(year, month, day):
    anchor = 2 + year + (year // 4) - (year // 100) + (year // 400)
    is_leapyear = (year%4 == 0) and ((year%100 != 0) or (year%400 == 0))
    day_zero = [4, 0, 0, 3, 5, 1, 3, 6, 2, 4, 0, 2]
    if is_leapyear:
        day_zero[0] = 3
        day_zero[1] = 6
    ans = (anchor + day_zero[month-1] + day) % 7
    return ans

def eng_date(year, month, day):
    return f"{months[month-1]} {day}, {year}"

def practice():
    while True:
        # Randomly generate a date
        year = random.randint(config.min_year,config.max_year)
        is_leapyear = (year%4 == 0) and ((year%100 != 0) or (year%400 == 0))
        len_months = [31, 28+is_leapyear, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month = random.randint(1,12)
        day = random.randint(1,len_months[month-1])

        # Display date
        print(eng_date(year,month,day))
        ans = day_of_the_week(year,month,day)
        # Measuring time taken for user response
        tic = time.perf_counter()
        user_ans = int(input())
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
            print("Problem Number, Correct?, Time (s)", file=f)
        print("Statistics Reset, Returning to Main Menu")
    else:
        print("Returning to Main Menu")
    return None

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
        print("Save results and times from practice [y/n]")
        print("Return to Main Menu [m], or Exit [e]")
        next_page = input()
        if next_page.lower() == "s":
            while True:
                try:
                    # min_year = int(input("Minimum year?"))
                    config.set_min_year(int(input("Minimum year?")))
                    if config.min_year < 1583:
                        raise ValueError
                    break
                except ValueError:
                    print("The Gregorian calendar began in October 1582. Please input an integer that is at least 1583.")
            while True:
                try:
                    config.set_max_year(int(input("Maximum year?")))
                    # max_year = int(input("Maximum year?"))
                    if config.max_year < config.min_year:
                        raise ValueError
                    break
                except ValueError:
                    print(f"Please input a year greater than the minimum year ({config.min_year}).")
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

# Consider consequences of having this always be true
while True:
    print("Begin Practice [p]")
    print("View Statistics [v]")
    print("Reset Statistics [r]")
    print("Tutorial [t]")
    print("Settings [s]")
    print("Exit [e]")
    print(f"Year Range: {config.min_year}-{config.max_year}")
    print(f"Saving: {config.saving_string()}")
    next_page = input()
    if next_page.lower() == "p":
        practice()
    elif next_page.lower() == "v":
        view_stats()
    elif next_page.lower() == "r":
        reset_stats()
    elif next_page.lower() == "t":
        tutorial()
    elif next_page.lower() == "s":
        settings()
    elif next_page.lower() == "e":
        exit_program()
    else:
        print("Invalid Option")
