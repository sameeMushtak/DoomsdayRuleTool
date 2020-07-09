import random
import time
import sys

# Add Settings to the Main Menu
    # Year Ranges
    # What Else?
# Calculate statistics (percent correct, average time) for last n attempts
# Leaderboard of record times
# Code assumes existence of a doomsday_stats.csv file with header row already existing

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
months = ["January", "February", "March", "April", "May", "June",\
        "July", "August", "September", "October", "November", "December"]

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

def main_menu():
    print("Begin Practice [p]")
    print("View Statistics [v]")
    print("Reset Statistics [r]")
    print("Tutorial [t]")
    print("Exit [e]")
    # Consider consequences of having this always be true
    while True:
        next_page = input()
        if next_page.lower() == "p":
            practice()
        elif next_page.lower() == "v":
            view_stats()
        elif next_page.lower() == "r":
            reset_stats()
        elif next_page.lower() == "t":
            tutorial()
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
            main_menu()
        elif next_page.lower() == "e":
            exit_program()
        else:
            print("Invalid Option")

def reset_stats():
    while True:
        confirm = input("Confirm reset statistics [y/n] ")
        if confirm.lower() == "y":
            with open("doomsday_stats.csv", "w") as f:
                print("Problem Number, Correct?, Time (s)", file=f)
            print("Statistics Reset")
            break
        else:
            print("Returning to Main Menu")
            main_menu()

    while True:
        next_page = input("Return to Main Menu [m], or Exit [e] ")
        if next_page.lower() == "m":
            main_menu()
        elif next_page.lower() == "e":
            exit_program()
        else:
            print("Invalid Option")

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
            main_menu()
        elif next_page.lower() == "e":
            exit_program()
        else:
            print("Invalid Option")

def practice():
    # Randomly generate a date
    year = random.randint(1500,2500)
    is_leapyear = (year%4 == 0) and ((year%100 != 0) or (year%400 == 0))
    len_months = [31, 28+is_leapyear, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    month = random.randint(1,12)
    day = random.randint(1,len_months[month-1])

    print(eng_date(year,month,day))
    ans = day_of_the_week(year,month,day)
    # Measuring time taken for user response
    tic = time.perf_counter()
    user_ans = int(input())
    toc = time.perf_counter()
    print(f"Correct Answer: {days[ans]} ({ans})")
    print(f"Elapsed Time: {toc-tic:.1f} s")

    # Store statistics in a file
    is_correct = ans == user_ans
    N = 0
    with open("doomsday_stats.csv", "r+") as f:
        for line in f:
            N += 1
        print(f"{N}, {is_correct}, {toc-tic:.3f}", file=f)

    # Go to next page
    while True:
        next_page = input("Continue [c], Return to Main Menu [m], or Exit [e] ")
        if next_page.lower() == "c":
            practice()
        elif next_page.lower() == "m":
            main_menu()
        elif next_page.lower() == "e":
            exit_program()
        else:
            print("Invalid Option")

def exit_program():
    sys.exit("Exiting.")

main_menu()
