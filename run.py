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


def table_print(list):
    """
    Format the input list based on max width of each column and print as
    a table with dividers between each column
    """
    # transpose the list, get the max of each column and
    # store in col_lens as dict[column]=legnth
    col_len = {i: max(map(len, inner)) for i, inner in enumerate(zip(*list))}

    # print using the column index from enumerate to lookup this columns length
    for inner in list:
        for col, word in enumerate(inner):
            print(f"{word:{col_len[col]}}", end=" | ")
        print()


def sub_menu(instr, list_func, add_func, cancel_func):
    """
    Display the list/add/cancel sub-menu until the user enters
    a valid choice then invoke requested function
    """
    while True:
        clear()
        print(f"Manage {instr}s sub-menu:\n")
        print(f"1. Show Active {instr}s")
        print(f"2. Add {instr}")
        print(f"3. Cancel {instr}")
        print("4. Return to main menu")
        print("\nPlease select an option by entering 1, 2, 3 or 4")

        choice = input("Enter your choice here:\n")

        if choice == '1':
            list_func()
        elif choice == '2':
            add_func()
        elif choice == '3':
            cancel_func()
        elif choice == '4':
            break
        else:
            print("Invalid selection. Please enter 1, 2, 3 or 4\n")
            input("Press Enter to continue...")


def add_to_worksheet(worksheet, data):
    """
    Add the passed in data to the passed in worksheet name
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")


@pause
def show_active_events():
    """
    Display details of all events in the events worksheet with a date value
    >= todays date and which are not cancelled
    """
    print("Finding data for upcoming events...\n")
    events = get_active_events()

    print("Formatting data for output...\n")

    # add headers for the output columns
    events.insert(0, ['EVENT CODE', 'TITLE', 'DATE',
                  'SPEAKER', 'SEATS AVAILABLE'])

    table_print(events)

    print("\nEnd of data for upcoming events...\n")


def get_active_events():
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
              if (datetime.strptime(x[2], '%d-%m-%Y') >= datetime.now())
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
                x[4] = str(int(x[4]) - int(y[4]))

    return events


@pause
def add_event():
    """
    Capture and validate Event Code, Title, Date, Speaker, Capacity data
    and store in the Events Spreadsheet
    """
    print(" to be written add event")

    event = get_new_event_data()

    add_to_worksheet('events', event)


def get_new_event_data():
    """
    Get event data input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of the following values
    separated by commas :
    Event Code, Title, Date, Speaker, Capacity
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        clear()
        print("ADD A NEW EVENT")
        print("Please enter data items separated by commas.  Data items are :")
        print("Event Code, Title, Date(DD-MM-YYY), Speaker, Capacity")
        print("Example: EC01, Economics 101, 29-04-2022, John Smith, 15\n")

        data_str = input("Enter your data here:\n")
        event = data_str.split(",")

        if validate_new_event_data(event):
            break

    return event


def validate_new_event_data(values):
    """
    The rules for new event data values are :
        a. 5 values must be provided
                - Event Code, Title, Date, Speaker, Capacity
        b. each value must have a length > 0
        c. Title must contain at least 1 alpha character
        d. Date must have format DD-MM-YYYY and > current date
        e. The combination of Date and Event Code must be unique in
                the event spreadsheet
        f. Speaker must contain at least 1 alpha character
        g. Capacity must be in the range 1 - 50
    """
    print("validate new event data to be written")

    return True


@pause
def cancel_event():
    """
    Capture Event Code, Date and Reason for event to be cancelled.
    Record cancellation in the Events Spreadsheet.  Return list of
    bookings for cancelled event.
    """
    print(" to be written cancel event")

    # event = get_rem_event_data()

    print(" to be written - update the spreadsheet")


@pause
def show_active_bookings():
    """
    Display details of all bookings in the bookings worksheet
    with a date value >= todays date
    """
    print("Finding data for active bookings...\n")
    bookings = get_active_bookings()

    print("Formatting data for output...\n")

    # add headers for the output columns
    bookings.insert(0, ['EVENT CODE', 'DATE', 'NAME',
                    'EMAIL', 'SEATS RESERVED'])

    table_print(bookings)

    print("\nEnd of data for active bookings...\n")


def get_active_bookings():
    """
    Get the data in the events spreadsheet, eliminate data where the
    event date <= current date, remove un-needed columns, calculate
    number of seats available for each event and return the data back
    to caller
    """
    bookings = SHEET.worksheet("bookings").get_all_values()
    bookings.pop(0)   # remove the header line

    # restrict the list to just bookings that are in the future
    bookings = [x for x in bookings
                if (datetime.strptime(x[1], '%d-%m-%Y') >= datetime.now())]

    # sort the bookings into chronological order of event
    bookings.sort(key=lambda x: datetime.strptime(x[1], '%d-%m-%Y'))

    return bookings


@pause
def add_booking():
    """
    Capture and validate Event Code, Date, Name, Email, Seats data
    and store in the Bookings Spreadsheet
    """
    print(" to be written add booking")

    booking = get_new_booking_data()

    add_to_worksheet('bookings', booking)


def get_new_booking_data():
    """
    Get booking data input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of the following values
    separated by commas :
    Event Code, Date, Name, Email, Seats
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        clear()
        print("ADD A NEW BOOKING")
        print("Please enter data items separated by commas.  Data items are :")
        print("Event Code, Date(DD-MM-YYY), Name, Email, Seats")
        print("Example: EC01, 29-04-2022, Jo Ryan, jo.ryan@anemail.com, 3\n")

        data_str = input("Enter your data here:\n")
        booking = data_str.split(",")

        if validate_new_booking_data(booking):
            break

    return booking


def validate_new_booking_data(values):
    """
    The rules for new booking data values are :
        a. 5 values must be provided
                - Event Code, Date, Name, Email, Seats
        b. each value must have a length > 0
        c. Date must have format DD-MM-YYYY and >= current date
        d. Name and Email must contain at least 1 alpha character
        e. Email must contain '@' with strings before and after
        f. Seats must be an integer and <= seats available for event
    """
    print("validate new booking data to be written")

    return True


@pause
def cancel_booking():
    """
    Prompt the user for email address of booking, display all current
    bookings for that email address - i.e. where booking Date >= current date
    Prompt the user to select booking to cancel, remove booking
    from bookings spreadsheet
    """
    clear()
    print("CANCEL A BOOKING")
    print("Please enter booking email address :")
    print("Example: jo.ryan@anemail.com")

    email = input("Enter your data here:\n")

    # get all bookings for the email where Date >= current date
    # to be written

    # if bookings found display the list and prompt user

    return email


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

    # build list of events with date < current date
    past_events = get_past_events()
    past_events.insert(0, ['EVENT CODE', 'TITLE', 'DATE', 'SPEAKER',
                           'CAPACITY', 'SEATS BOOKED', '% CAPACITY USED',
                           'STATUS', 'REASON'])

    # divide the list into cancelled events and events that went ahead
    # display cancelled events and reasons for cancellation
    cancelled_events = [x for x in past_events if (x[7] != '')]
    print("List of cancelled events...\n")
    table_print(cancelled_events)

    # display events that went ahead
    delivered_events = [x for x in past_events if (x[7] != 'cancelled')]

    # remove the Status and Reason elements from the lists
    for x in delivered_events:
        x.pop()
        x.pop()

    print("\nList of delivered events...\n")
    table_print(delivered_events)

    # display number cancelled events vs number not cancelled
    print(f"\nNumber of cancelled events : {len(cancelled_events)-1}")
    print(f"Number of events that went ahead : {len(delivered_events)-1}\n")

    print("\nEnd of data for past events...\n")


def get_past_events():
    """
    Get the data in the events spreadsheet, eliminate data where the
    event date > current date and pass data back to caller
    """
    events = SHEET.worksheet("events").get_all_values()
    events.pop(0)   # remove the header line

    # restrict the list to just events that are in the past or for today
    events = [x for x in events
              if (datetime.strptime(x[2], '%d-%m-%Y') <= datetime.now())]

    # sort the events into chronological order
    events.sort(key=lambda x: datetime.strptime(x[2], '%d-%m-%Y'))

    # calculate capacity booked as a number and a %
    bookings = SHEET.worksheet("bookings").get_all_values()
    for x in events:
        # add 2 items to the list - one for booked seats,
        # one for calculated % capacity used
        # store as strings to make printing easier later
        x.insert(5, '0')
        x.insert(5, '0')
        for y in bookings:
            # check for matching Event Code and Date values
            if x[0] == y[0] and x[2] == y[1]:
                x[5] = str(int(x[5]) + int(y[4]))   # add to seats_booked
                x[6] = str(round((int(x[5]) / int(x[4]) * 100), 2))   # calc %

    return events


def main():
    """
    Keep displaying the main choices menu until the user chooses to exit
    """
    while True:
        clear()
        print("Main Menu for Event Scheduler Application:\n")
        print("1. Manage Events")
        print("2. Manage Bookings")
        print("3. Review Past Events")
        print("4. Exit")
        print("\nPlease select an option by entering a number between 1 and 5")

        choice = input("Enter your choice here:\n")

        if choice == '1':
            sub_menu("Event", show_active_events, add_event, cancel_event)
        elif choice == '2':
            sub_menu("Booking", show_active_bookings, add_booking,
                     cancel_booking)
        elif choice == '3':
            review_past_events()
        elif choice == '4':
            print("Goodbye !")
            break
        else:
            print("Invalid selection. Please enter a digit between 1 and 4\n")
            input("Press Enter to continue...")


main()
