import doomsday_funcs as df

# Calculate statistics (percent correct, average time) for last n attempts
# Leaderboard of record times
# Code assumes existence of a doomsday_stats.csv file with header row already existing

# Consider consequences of having this always be true
while True:
    print("Begin Practice [p]")
    print("Calendar [c]")
    print("View Statistics [v]")
    print("Reset Statistics [r]")
    print("Tutorial [t]")
    print("Settings [s]")
    print("Exit [e]")
    print(f"Year Range: {df.get_min_year()}-{df.get_max_year()}")
    print(f"Saving: {df.get_saving()}")
    next_page = input()
    if next_page.lower() == "p":
        df.practice()
    elif next_page.lower() == "c":
        df.calendar()
    elif next_page.lower() == "v":
        df.view_stats()
    elif next_page.lower() == "r":
        df.reset_stats()
    elif next_page.lower() == "t":
        df.tutorial()
    elif next_page.lower() == "s":
        df.settings()
    elif next_page.lower() == "e":
        df.exit_program()
    else:
        print("Invalid Option")
