import gspread
from google.oauth2.service_account import Credentials
# import system and name for the clear screen function
from os import system, name

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ms3-event-scheduler')


# define function to clear the screen
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def show_upcoming_events():
    """
    Display details of all events in the events worksheet with a date value
    >= todays date
    """
    print("Finding data for upcoming events...\n")

    input("Press Enter to continue...")


def sub_menu(instr, add_func, cancel_func):
    """
    Display the add/cancel sub-menu until the user enters
    a valid choice then invoke requested function
    """
    while True:
        clear()
        print(f"Manage {instr}s sub-menu:")
        print(f"1. Add {instr}")
        print(f"2. Cancel {instr}")
        print("Please select an option by entering 1 or 2")
        print("Enter 'X' to return to main menu.")

        choice = input("Enter your choice here:\n")

        if choice == '1':
            add_func()
        elif choice == '2':
            cancel_func()
        elif choice.upper() == 'X':
            break
        else:
            print("Invalid selection. Please enter 1 or 2 or 'X'\n")
            input("Press Enter to continue...")


def add_event():
    print(" add event test")
    input("Press Enter to continue...")


def cancel_event():
    print(" cancel event test")
    input("Press Enter to continue...")


def add_booking():
    print(" add booking test")
    input("Press Enter to continue...")


def cancel_booking():
    print(" cancel booking test")
    input("Press Enter to continue...")


def review_past_events():
    """
    Display data on all events in the events worksheet with a date value
    < todays date
    Information to be displayed :
        a. number of events with breakdown of #cancelled and #not-cancelled
        b. % capacity filled for events that were not cancelled
            - results ordered by % filled descending
        c. list of cancelled events and reason for cancellation
    """
    print("Finding data for past events...\n")

    input("Press Enter to continue...")


def main():
    """
    Keep displaying the main choices menu until the user chooses to exit
    """
    while True:
        clear()
        print("Main Menu for Event Scheduler Application:")
        print("1. Show Upcoming Events")
        print("2. Manage Events")
        print("3. Manage Bookings")
        print("4. Review Past Events")
        print("5. Exit")
        print("Please select an option by entering a number between 1 and 5")

        choice = input("Enter your choice here:\n")

        if choice == '1':
            show_upcoming_events()
        elif choice == '2':
            sub_menu("Event", add_event, cancel_event)
        elif choice == '3':
            sub_menu("Booking", add_booking, cancel_booking)
        elif choice == '4':
            review_past_events()
        elif choice == '5':
            print("Goodbye !")
            break
        else:
            print("Invalid selection. Please enter a digit between 1 and 5\n")
            input("Press Enter to continue...")


print("Welcome to the Event Scheduler Application")
main()
