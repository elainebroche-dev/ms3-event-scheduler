import gspread
from google.oauth2.service_account import Credentials
# import system and name for the clear screen function
from os import system, name
from datetime import datetime

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


def pause(function):
    """
    decorator to give the user an opportunity to review feedback on screen
    before moving on by pressing Enter
    """
    def wrapper():
        function()
        input("Press Enter to continue...")
    return wrapper


@pause
def show_upcoming_events():
    """
    Display details of all events in the events worksheet with a date value
    >= todays date and which are not cancelled
    """
    print("Finding data for upcoming events...\n")
    events = get_upcoming_events()

    print("Formatting data for output...\n")

    # add headers for the output columns
    events.insert(0, ['EVENT CODE', 'TITLE', 'DATE', 'TIME',
                  'SPEAKER', 'SEATS AVAILABLE'])

    # transpose the list, get the max of each column and
    # store in col_lens as dict[column]=legnth
    col_lens = {i: max(map(len, inner)) for i, inner in enumerate(zip(*events))}

    # print using the column index from enumerate to lookup this columns length
    for inner in events:
        for col, word in enumerate(inner):
            print(f"{word:{col_lens[col]}}", end=" | ")
        print()

    print("\nEnd of data for upcoming events...\n")


def get_upcoming_events():
    """
    Get the data in the events spreadsheet, eliminate data where the
    event date <= current date, remove un-needed columns, calculate
    number of seats available for each event and return the data back
    to caller
    """
    events = SHEET.worksheet("events").get_all_values()
    events.pop(0)   # remove the header line

    # restrict the list to just events that are in the future
    events = [x for x in events
              if (datetime.strptime(x[2], '%d-%m-%Y') > datetime.now())
              and (x[6].upper() != 'CANCELLED')]

    # sort the events into chronological order
    events.sort(key=lambda x: datetime.strptime(x[2], '%d-%m-%Y'))

    # remove the Status and Reason elements from the lists
    for x in events:
        x.pop()
        x.pop()

    # deduct booked seats from capacity to give available seat totals
    bookings = SHEET.worksheet("bookings").get_all_values()
    for x in events:
        for y in bookings:
            # check for matching Event Code and Date values
            if x[0] == y[0] and x[2] == y[1]:
                x[5] = str(int(x[5]) - int(y[4]))

    return events


def sub_menu(instr, add_func, cancel_func):
    """
    Display the add/cancel sub-menu until the user enters
    a valid choice then invoke requested function
    """
    while True:
        clear()
        print(f"Manage {instr}s sub-menu:\n")
        print(f"1. Add {instr}")
        print(f"2. Cancel {instr}")
        print("\nPlease select an option by entering 1 or 2")
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


@pause
def add_event():
    """
    Capture and Validate Event Code, Title, Date, Time, Speaker, Capacity data
    and store in the Events Spreadsheet
    """
    print(" to be written add event")


def validate_new_event_data(values):
    """
    The rules for new event data values are :
        a. 6 values must be provided
                - Event Code, Title, Date, Time, Speaker, Capacity
        b. each value must have a length > 0
        c. Title must contain at least 1 alpha character
        d. Date must have format DD-MM-YYYY and > current date
        e. The combination of Date and Event Code must be unique in
                the event spreadsheet
        d. Time must have format HH:MM and within valid 24hr clock range
        e. Speaker must contain at least 1 alpha character
        f. Capacity must be in the range 1 - 50
    """
    print("validate new event data to be written")


@pause
def cancel_event():
    """
    Capture Event Code and Date for event to be cancelled.  Record cancellation
    in the Events Spreadsheet.  Return list of bookings for cancelled event.
    """
    print(" to be written cancel event")


@pause
def add_booking():
    """
    Capture and Validate Event Code, Date, Name, Email, Seats data
    and store in the Bookings Spreadsheet
    """
    print(" to be written add booking")


@pause
def cancel_booking():
    print(" to be written cancel booking")


@pause
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


def main():
    """
    Keep displaying the main choices menu until the user chooses to exit
    """
    while True:
        clear()
        print("Main Menu for Event Scheduler Application:\n")
        print("1. Show Upcoming Events")
        print("2. Manage Events")
        print("3. Manage Bookings")
        print("4. Review Past Events")
        print("5. Exit")
        print("\nPlease select an option by entering a number between 1 and 5")

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


main()
