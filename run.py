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


def manage_events():
    """
    Display the manage events sub-menu and invoke the appropriate
    event function (add or cancel) based on the user input
    """
    while True:
        clear()
        print("Manage Events sub-menu:")
        print("1. Add Event")
        print("2. Cancel Event")
        print("Please select an option by entering 1 or 2")
        print("Enter 'X' to return to main menu.")

        choice = input("Enter your choice here:\n")

        if choice == '1':
            print("to be written - add event")
            break
        elif choice == '2':
            print("to be written - cancel event")
            break
        elif choice.upper() == 'X':
            break
        else:
            print("Invalid selection. Please enter 1 or 2 or 'X'\n")
            input("Press Enter to continue...")


def manage_bookings():
    """
    Display the manage bookings sub-menu and invoke the appropriate
    booking function (add or cancel) based on the user input
    """
    while True:
        clear()
        print("Manage Bookings sub-menu:")
        print("1. Add Booking")
        print("2. Cancel Booking")
        print("Please select an option by entering 1 or 2")
        print("Enter 'X' to return to main menu.")

        choice = input("Enter your choice here:\n")

        if choice == '1':
            print("to be written - add booking")
            break
        elif choice == '2':
            print("to be written - cancel booking")
            break
        elif choice.upper() == 'X':
            break
        else:
            print("Invalid selection. Please enter 1 or 2 or 'X'\n")
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
            manage_events()
        elif choice == '3':
            manage_bookings()
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
