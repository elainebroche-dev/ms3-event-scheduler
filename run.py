import gspread
from google.oauth2.service_account import Credentials
# import system and name for the clear screen function
from os import system, name
from datetime import datetime
import re
import os

SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive'
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ms3-event-scheduler')


# define function to clear the screen
def clear():
    os.system('tput reset')
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
        input('Press Enter to continue...\n')
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
            print(f'{word:{col_len[col]}}', end=' | ')
        print()


def sub_menu(instr, list_func, add_func, cancel_func):
    """
    Display the list/add/cancel sub-menu until the user enters
    a valid choice then invoke requested function
    """
    while True:
        clear()
        print(f'Manage {instr}s sub-menu:\n')
        print(f'1. Show Active {instr}s')
        print(f'2. Add {instr}')
        print(f'3. Cancel {instr}')
        print('4. Return to main menu')
        print('\nPlease select an option by entering 1, 2, 3 or 4')

        choice = input('Enter your choice here:\n')

        if choice == '1':
            list_func()
        elif choice == '2':
            add_func()
        elif choice == '3':
            cancel_func()
        elif choice == '4':
            break
        else:
            print('Invalid selection. Please enter 1, 2, 3 or 4\n')
            input('Press Enter to continue...\n')


def add_to_worksheet(worksheet, data):
    """
    Add the passed in data to the passed in worksheet name
    """
    print(f'Updating {worksheet} worksheet...\n')
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} worksheet updated successfully.\n')


def get_data(funcdesc, items, example):
    """
    Because a number of different operations (e.g. add booking,
    cancel event etc) all require input from the user, which all
    require validation and usually have data items in common, this
    generic function has been built to be usable by all of those
    operations.  The values passed in determine what the
    user is asked for and how it is validated.

    This function gets data input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of values separated by commas.
    The loop will repeatedly request data, until it is valid or
    user quits the operation.
    """
    while True:
        clear()
        print(funcdesc)
        print('Please enter data items separated by commas.  Data items are :')
        print(f'     {items}')
        print(f'     {example}')
        print('or enter "x" to quit\n')

        data_str = input('Enter your data here:\n')

        # check to see if the user wants to abort the operation
        if data_str.upper() == 'X':
            print('\nQuitting operation and returning to sub-menu\n')
            return []         # return empty list to indicate user is quitting

        datalist = data_str.split(',')
        datalist = [x.strip() for x in datalist]  # trim the input values

        itemlist = items.split(',')
        itemlist = [x.strip() for x in itemlist]  # trim the item names

        if validate_data(funcdesc, itemlist, datalist):
            break

        # getting to here means inputs were not valid
        # wait to allow user to read error message on screen
        input('\nPress Enter to continue...\n')

    return datalist


def validate_data(funcdesc, items, values):
    """
    Validate a list of user inputs based on a list of data items
    """
    print('\nValidating input values...\n')
    try:

        # check the number of user inputs matches the number required
        if len(items) != len(values):
            raise ValueError('Incorrect number of input values,'
                             f' {len(items)} expected')

        # check no 0 length values in the input
        if (len(min(values, key=len))) == 0:
            raise ValueError('All inputs must have a length > 0')

        # loop through each expected input and check syntax based on name
        for x in range(len(items)):
            if items[x].upper() == 'EVENT CODE':
                tmpcode = values[x]     # capture the event code for use later
            elif items[x].upper() == 'DATE(DD-MM-YYYY)':
                tmpdate = values[x]
                datetime.strptime(tmpdate, '%d-%m-%Y')    # ? ValueError
                # using a regex to check 2 digit day and month entered
                if not re.search(r'^\d{2}-\d{2}-\d{4}$', tmpdate):
                    raise ValueError('2 digit day and month required in Date')
            elif items[x].upper() in ('CAPACITY', 'SEATS'):
                tmpnum = int(values[x])                   # ? ValueError
                # check value is > 0
                if (tmpnum <= 0):
                    raise ValueError(f'{items[x]} must have a value > 0')
            elif items[x].upper() == 'EMAIL':
                patt = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                if not re.search(patt, values[x]):
                    raise ValueError('Email address is not valid')

        # once all syntax checks have been passed, next the semantic checks/
        # business rules for the data need to run - these are specific to the
        # operation being requested

        if (funcdesc == 'ADD A NEW EVENT'):
            # a. date must be in the future
            # b. event code/date combination must be unique
            if (datetime.strptime(tmpdate, '%d-%m-%Y') < datetime.now()):
                raise ValueError('Event dates must be >= current date')
            elif event_exists(tmpdate, tmpcode):
                raise ValueError('Duplicate Event Code and Date found')

        elif (funcdesc == 'CANCEL EVENT'):
            # a. date must not be in the past
            if (datetime.strptime(tmpdate, '%d-%m-%Y') < datetime.now()):
                raise ValueError('Events in the past cannot be cancelled')

        elif (funcdesc == 'ADD A NEW BOOKING'):
            # a. date must not be in the past
            # b. event must exist in events sheet
            # c. seats requested must be <= seats available2
            if (datetime.strptime(tmpdate, '%d-%m-%Y') < datetime.now()):
                raise ValueError('Booking dates must be >= current date')
            elif not event_exists(tmpcode, tmpdate):
                raise ValueError('Booking cannot be added. '
                                 'Event does not exist')
            elif (num_seats_available(tmpcode, tmpdate) < tmpnum):
                raise ValueError('Booking cannot be added. '
                                 'Not enough seats available')

        elif (funcdesc == 'CANCEL BOOKING'):
            # a. date must not be in the past
            if (datetime.strptime(tmpdate, '%d-%m-%Y') < datetime.now()):
                raise ValueError('Bookings in the past cannot be cancelled')

    except ValueError as e:
        print(f'Invalid data: {e}, please try again.')
        return False

    print('Input values are valid...\n')
    return True


def event_exists(event_code, event_date):
    """
    Return True if the input event code and date exist as an
    entry in the events spreadsheet and this event is not
    cancelled.  Otherwise return False
    """
    events = SHEET.worksheet('events').get_all_values()
    for x in events:
        if (x[0].upper() == event_code.upper() and
           x[2] == event_date and x[5].upper() != 'CANCELLED'):
            return True
    return False


def num_seats_available(event_code, event_date):
    """
    Calculate number of seats available for an event and
    return this number as an int
    """
    total = 0
    # get capacity
    events = SHEET.worksheet('events').get_all_values()
    for x in events:
        if (x[0].upper() == event_code.upper() and x[2] == event_date):
            total = int(x[4])
            break

    # deduct seats booked
    bookings = SHEET.worksheet('bookings').get_all_values()
    for y in bookings:
        if (y[0].upper() == event_code.upper() and y[1] == event_date):
            total = total - int(y[4])

    print(f'\nNumber of seats available for {event_code} - '
          f'{event_date} is {total}\n')
    return total


@pause
def show_active_events():
    """
    Display details of all events in the events worksheet with a date value
    >= todays date and which are not cancelled
    """
    print('Finding data for upcoming events...\n')
    events = get_active_events()

    # add headers for the output columns
    events.insert(0, ['CODE', 'TITLE', 'DATE',
                  'HOST', 'SEATS OPEN'])

    table_print(events)

    print('\nEnd of data for upcoming events...\n')


def get_active_events():
    """
    Get the data in the events spreadsheet, eliminate data where the
    event date < current date, remove un-needed columns, calculate
    number of seats available for each event and return the data back
    to caller
    """
    events = SHEET.worksheet('events').get_all_values()
    events.pop(0)   # remove the header line

    # restrict the list to just events that are >= current date
    # and not cancelled
    events = [x for x in events
              if (datetime.strptime(x[2], '%d-%m-%Y') >= datetime.now()) and
                 (x[5].upper() != 'CANCELLED')]

    # sort the events into chronological order
    events.sort(key=lambda x: datetime.strptime(x[2], '%d-%m-%Y'))

    # remove the Status and Reason elements from the lists
    for x in events:
        x.pop()
        x.pop()

    # deduct booked seats from capacity to give available seat totals
    bookings = SHEET.worksheet('bookings').get_all_values()
    for x in events:
        for y in bookings:
            # check for matching Event Code and Date values
            if x[0].upper() == y[0].upper() and x[2] == y[1]:
                x[4] = str(int(x[4]) - int(y[4]))

    return events


@pause
def add_event():
    """
    Capture and validate Event Code, Title, Date, Host, Capacity data
    and store in the Events Spreadsheet
    """
    # event = get_new_event_data()
    event = get_data('ADD A NEW EVENT',
                     'Event Code, Title, Date(DD-MM-YYYY), Host, Capacity',
                     'Example: HS01, History, 29-04-2022, Joe, 15')

    if (len(event)):
        add_to_worksheet('events', event)
        print('New event added...\n')


@pause
def cancel_event():
    """
    Capture Event Code, Date and Reason for event to be cancelled.
    Record cancellation in the Events Spreadsheet.  Return list of
    bookings for cancelled event.
    """
    event = get_data('CANCEL EVENT',
                     'Event Code, Date(DD-MM-YYYY), Reason',
                     'Example: HS01, 29-04-2022, Host not available')

    if (len(event)):
        cancel_event_in_worksheet(event)


def cancel_event_in_worksheet(data):
    """
    Attempt to update row in events spreadsheet where Event Code and
    Date match the input data. Remove associated bookings from bookings
    spreadsheet.
    """
    print(f'Attempting to cancel event {data} in events spreadsheet\n')

    events = SHEET.worksheet('events').get_all_values()
    for x in range(len(events)):
        if (events[x][0].upper() == data[0].upper() and
           events[x][2] == data[1] and events[x][5].upper() != 'CANCELLED'):
            SHEET.worksheet('events').update_cell(x+1, 6, 'cancelled')
            SHEET.worksheet('events').update_cell(x+1, 7, data[2])
            print('Event cancelled in spreadsheet...\n')

            # show any bookings linked to the cancelled event
            print('Bookings removed for cancelled event - '
                  'please notify attendees :\n')
            bookings = SHEET.worksheet('bookings').get_all_values()

            # add headers for the output columns
            removed_bookings = [['CODE', 'DATE', 'NAME',
                                'EMAIL', 'SEATS']]

            # go largest number to smallest because if rows are
            # to be deleted they need to be taken from the bottom
            # of the sheet and move up to avoid missing rows when
            # the remaining rows get moved up
            for y in range(len(bookings)-1, 0, -1):
                if (bookings[y][0].upper() == data[0].upper() and
                   bookings[y][1] == data[1]):
                    removed_bookings.append(bookings[y])
                    SHEET.worksheet('bookings').delete_rows(y+1)

            table_print(removed_bookings)
            print('\nEnd of bookings list\n')
            return

    print('Event could not be found in events spreadsheet\n')


@pause
def show_active_bookings():
    """
    Display details of all bookings in the bookings worksheet
    with a date value >= todays date
    """
    print('Finding data for active bookings...\n')
    bookings = get_active_bookings()

    # add headers for the output columns
    bookings.insert(0, ['CODE', 'DATE', 'NAME',
                    'EMAIL', 'SEATS'])

    table_print(bookings)

    print('\nEnd of data for active bookings...\n')


def get_active_bookings():
    """
    Get the data in the events spreadsheet, eliminate data where the
    booking date < current date. Return the data back to caller
    """
    bookings = SHEET.worksheet('bookings').get_all_values()
    bookings.pop(0)   # remove the header line

    # restrict the list to just bookings that are >= current date
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
    booking = get_data('ADD A NEW BOOKING',
                       'Event Code, Date(DD-MM-YYYY), Name, Email, Seats',
                       'Example: HS01, 29-04-2022, Jo Ryan, '
                       'jo.ryan@anemail.com, 3')

    if len(booking):
        add_to_worksheet('bookings', booking)
        print('New booking added...\n')


@pause
def cancel_booking():
    """
    Capture and validate Event Code, Date, Email data
    and remove corresponding row from the Bookings Spreadsheet
    If multiple bookings exist for the input Event Code, Date, Email
    combination, then only the first matching row in the spreadsheet
    will be removed.
    """
    booking = get_data('CANCEL BOOKING',
                       'Event Code, Date(DD-MM-YYYY), Email',
                       'Example: HS01, 29-04-2022, jo.ryan@anemail.com')

    if len(booking):
        remove_booking_from_worksheet(booking)


def remove_booking_from_worksheet(data):
    """
    Attempt to remove row from bookings spreadsheet where Event Code,
    Date and Email match the input booking - print result to screen
    If multiple bookings exist for the input Event Code, Date, Email
    combination, then only the first matching row in the spreadsheet
    will be removed.
    """
    print(f'Attempting to remove booking {data} from bookings spreadsheet\n')

    bookings = SHEET.worksheet('bookings').get_all_values()
    for x in range(len(bookings)):
        if (bookings[x][0].upper() == data[0].upper() and
           bookings[x][1] == data[1] and
           bookings[x][3].upper() == data[2].upper()):
            SHEET.worksheet('bookings').delete_rows(x+1)
            print('Booking removed from spreadsheet...\n')
            return

    print('Booking could not be found in bookings spreadsheet\n')


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
    print('Finding data for past events...\n')

    # build list of events with date < current date
    past_events = get_past_events()
    past_events.insert(0, ['CODE', 'TITLE', 'DATE', 'HOST',
                           'CPTY', 'STATUS', 'REASON',
                           'BKD', '% FILL'])

    # divide the list into cancelled events and events that went ahead
    # display cancelled events and reasons for cancellation
    # discard the status, seats booked and % capacity used elements from
    # the cancelled events list as they are not applicable
    cancelled_events = [x[0:5] + x[6:7] for x in past_events
                        if (x[5].upper() != '')]

    print('List of cancelled events...\n')
    table_print(cancelled_events)

    # display events that went ahead
    # remove the Status and Reason elements from the delivered events list
    delivered_events = [x[0:5] + x[7:9] for x in past_events
                        if (x[5].upper() != 'CANCELLED')]

    print('\nList of delivered events...\n')
    table_print(delivered_events)

    # display number cancelled events vs number not cancelled
    print(f'\nNumber of cancelled events : {len(cancelled_events)-1}')
    print(f'Number of events that went ahead : {len(delivered_events)-1}\n')

    print('End of data for past events...\n')


def get_past_events():
    """
    Get the data in the events spreadsheet, eliminate data where the
    event date > current date and pass data back to caller
    """
    events = SHEET.worksheet('events').get_all_values()
    events.pop(0)   # remove the header line

    # restrict the list to just events that are in the past
    events = [x for x in events
              if (datetime.strptime(x[2], '%d-%m-%Y') < datetime.now())]

    # sort the events into chronological order
    events.sort(key=lambda x: datetime.strptime(x[2], '%d-%m-%Y'))

    # calculate capacity booked as a number and a %
    bookings = SHEET.worksheet('bookings').get_all_values()
    for x in events:
        # add 2 items to the list - one for booked seats,
        # one for calculated % capacity used
        # store as strings to make printing easier later
        x.extend(['0', '0'])
        for y in bookings:
            # check for matching Event Code and Date values
            if x[0].upper() == y[0].upper() and x[2] == y[1]:
                x[7] = str(int(x[7]) + int(y[4]))   # add to seats_booked
                x[8] = str(round((int(x[7]) / int(x[4]) * 100), 2))   # calc %

    return events


def main():
    """
    Keep displaying the main choices menu until the user chooses to exit
    """
    while True:
        clear()
        print('Main Menu for Event Scheduler Application:\n')
        print('1. Manage Events')
        print('2. Manage Bookings')
        print('3. Review Past Events')
        print('4. Exit')
        print('\nPlease select an option by entering a number between 1 and 4')

        choice = input('Enter your choice here:\n')

        if choice == '1':
            sub_menu('Event', show_active_events, add_event, cancel_event)
        elif choice == '2':
            sub_menu('Booking', show_active_bookings, add_booking,
                     cancel_booking)
        elif choice == '3':
            review_past_events()
        elif choice == '4':
            print('Goodbye !')
            break
        else:
            print('Invalid selection. Please enter a digit between 1 and 4\n')
            input('Press Enter to continue...\n')


main()
