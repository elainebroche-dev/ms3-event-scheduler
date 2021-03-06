<h1 align="center">Event Scheduler</h1>

[View the live project here](https://ms3-event-scheduler.herokuapp.com/)

Event Scheduler is a command line application to manage data relating to events such as talks/lectures and bookings for those events.

The user can interact with the application to view upcoming events and bookings, review past events and see how popular they were (% seats booked), add new events, cancel upcoming events, create and delete bookings linked to upcoming events. 

The event and booking data is stored in an external Google Spreadsheet.

## Index – Table of Contents
* [User Experience (UX)](#user-experience-ux) 
* [Features](#features)
* [Design](#design)
* [Technologies Used](#technologies-used)
* [Testing](#testing)
* [Deployment](#deployment)
* [Credits](#credits)

## User Experience (UX)

-   ### User stories - as a user I want to be able to :

  1. Easily navigate between the different functions available in the application.
  2. View information on upcoming scheduled events in the events spreadsheet.
  3. Use the application to book new events and have these stored in the events spreadsheet.  
  4. Cancel events and log a reason for cancellation in the events spreadsheet.
  5. Automatically remove all bookings linked to a cancelled event from the bookings spreadsheet and return a list on screen of those details so that attendees can be notified.
  6. View information on bookings for upcoming scheduled events.
  7. Add a new booking for an upcoming event.
  8. Cancel a booking for an upcoming event.
  9. Review and analyse data for past events, this information should include :
      - details on cancelled events including the reason given for cancellation
      - details on events that went ahead including the number of seats that were available and % seats booked 
      - a total number of cancelled events
      - a total number of events that went ahead
  10. Clearly understand how to interact with the application and get feedback on updates to the underlying data.
  

## Features

### Existing Features

- ###  __F01 Main Menu__
    - The main menu is displayed when the application starts.  To keep the interface simple to use and uncluttered the menu divides the functionality into three high level areas : 1) Event related actions, 2) Booking related actions, 3) Analysis/Review of data for events in the past.  

      ![Main Menu](documentation/images/f01-main-menu-1.png)

    - The user is prompted to choose one of the menu options by entering the option number.  If the user enters an incorrect value an error message is displayed, then once the user presses Enter the screen is refreshed and the main menu is shown again.  

      ![Main Menu Message](documentation/images/f01-main-menu-2.png)

    - The main menu is repeatedly refreshed and re-displayed while inputs from the user are invalid and after each menu option 1 - 3 completes.  The application is terminated by selecting option 4 from the main menu.

- ###  __F02 Manage Events sub-menu__
    - From the main menu, when the user selects option 1 they are brought to the Manage Events sub-menu (see the below image).  Like the main menu, this menu is repeatedly refreshed and re-displayed while inputs from the user are invalid and after each menu option 1 - 3 completes.

      ![Events Menu](documentation/images/f02-manage-events-submenu.png)

    - The functions to view, add and cancel upcoming events are all accessible through this menu.  Selecting option 4 returns the user back up to the main menu (F01).

- ###  __F03 Show Active/Upcoming Events__
    - If the user selects option 1 from the Manage Events sub-menu they are shown a list of events from the events spreadsheet where the scheduled date for the event >= current date.  Cancelled events are not included in the displayed list.  
    
    - The SEATS OPEN column values are calculated by taking the Capacity value for the event from the events spreadsheet, and then deducting all seats currently booked for that event - so the SEATS OPEN value shows how many seats are still bookable for that event.  Bookings added or cancelled while using the application will be reflected in the SEAT OPEN value when the Show Active Events option is subsequently run.

      ![Active Events](documentation/images/f03-show-active-events.png)

- ###  __F04 Add Event__
    - To add a new event the user selects option 2 from the Manage Events sub-menu.  The application displays a message on screen listing the inputs it requires and displays an example input string of values (see image).

      ![Add Event](documentation/images/f04-add-event.png)

    - If the inputs entered by the user do not meet the validation requirements the user will be asked to re-enter them, or they can quit the operation and return to the Manage Events sub-menu by entering 'x'.
    
    - The rules for the input values are as follows :
      - inputs are separated by commas, all inputs must have a length > 0
      - the combination of Event Code and Date must be unique within the events spreadsheet 
      - Date should have a format of DD-MM-YYYY and must be >= current date
      - The Capacity value must be an integer > 0

    - When the user inputs valid data the application displays multiple messages to provide information on how the data is being processed and a new row is added to the events spreadsheet for the new event.  Once the operation is complete and the user presses Enter, they are returned to the Manage Events sub-menu.

      ![Add Event Success](documentation/images/f04-add-event-success.png)

    - The image below shows the new row added the end of the events spreadsheet :

      ![Add Event Row](documentation/images/f04-add-event-spreadsheet.png)

- ###  __F05 Cancel Event__
    - To cancel an event the user selects option 3 from the Manage Events sub-menu.  The application displays a message on screen listing the inputs it requires and displays an example input string of values (see image). 

      ![Cancel Event](documentation/images/f05-cancel-event.png)

    - If the inputs entered by the user do not meet the validation requirements the user will be asked to re-enter them, or they can quit the operation and return to the Manage Events sub-menu by entering 'x'.
    
    - The rules for the input values are as follows :
      - inputs are separated by commas, all inputs must have a length > 0
      - Date should have a format of DD-MM-YYYY and must be >= current date (events that have already happened cannot be cancelled)
      - The Event Code and Date combination must exist as an active (not already cancelled) event in the spreadsheet

    - When the user inputs valid data the application displays messages to provide information on how the data is being processed.  Cancelled events are not deleted from the events spreadsheet, instead they are updated to have a value of 'cancelled' in the Status column and the input Reason string provided by the user is stored in the Reason column of the spreadsheet.

    - Cancelling an event has the side-effect of deleting all associated bookings for the event from the bookings spreadsheet.   During the cancel event operation the bookings effected are listed on screen to let the user know what bookings have been removed and prompt them to contact attendees to inform them.

      ![Cancel Event Success](documentation/images/f05-cancel-event-success.png)

    - Once the operation is complete and the user presses Enter, they are returned to the Manage Events sub-menu.  

    - The image below shows a section of the events spreadsheet with the cancelled event :

      ![Cancel Event Row](documentation/images/f05-cancel-event-spreadsheet.png)

- ###  __F06 Manage Bookings sub-menu__
    - From the main menu, when the user selects option 2 they are brought to the Manage Bookings sub-menu (see the below image).  Like the main menu, this menu is repeatedly refreshed and re-displayed while inputs from the user are invalid and after each menu option 1 - 3 completes.  Selecting option 4 returns the user back up to the main menu (F01).

      ![Bookings Menu](documentation/images/f06-manage-bookings-submenu.png)

    - The functions to view, add and cancel bookings for upcoming events are all accessible through this menu.  

- ###  __F07 Show Active/Upcoming Bookings__
    - If the user selects option 1 from the Manage Bookings sub-menu they are shown a list of bookings from the bookings spreadsheet where the scheduled date for the event >= current date.   The data shows the Event Code, Date of the event, Name of person who booked, Email address and number of seats for this booking.  

      ![Active Bookings](documentation/images/f07-show-active-bookings.png)

- ###  __F08 Add Booking__
    - To add a new booking for an event the user selects option 2 from the Manage Bookings sub-menu.  The application displays a message on screen listing the inputs it requires and displays an example input string of values (see image).

      ![Add Booking](documentation/images/f08-add-booking.png)

    - If the inputs entered by the user do not meet the validation requirements the user will be asked to re-enter them, or they can quit the operation and return to the Manage Bookings sub-menu by entering 'x'.
    
    - The rules for the input values are as follows :
      - inputs are separated by commas, all inputs must have a length > 0
      - the combination of Event Code and Date must exist in the events spreadsheet and must be active (not cancelled) 
      - Date should have a format of DD-MM-YYYY and must be >= current date
      - Email address must have a valid format - e.g. contain @ with alphanumerics on either side
      - The Seats value must be an integer > 0 and must not exceed the number of seats available (calculated as the event Capacity from the events spreadsheet minus total seats reserved on all existing bookings for this event)

    - When the user inputs valid data the application displays multiple messages to provide information on how the data is being processed and a new row is added to the bookings spreadsheet for the new booking.  Once the operation is complete and the user presses Enter, they are returned to the Manage Bookings sub-menu.

    - Duplicate bookings are allowed - the same person can make multiple bookings for a single event. 

      ![Add Booking Success](documentation/images/f08-add-booking-success.png)

    - The image below shows a section of the bookings spreadsheet with the new row added :

      ![Add Booking Row](documentation/images/f08-add-booking-spreadsheet.png)

- ###  __F09 Cancel Booking__
    - To cancel a booking the user selects option 3 from the Manage Bookings sub-menu.  The application displays a message on screen listing the inputs it requires and displays an example input string of values (see image). 

      ![Cancel Booking](documentation/images/f09-cancel-booking.png)

    - If the inputs entered by the user do not meet the validation requirements the user will be asked to re-enter them, or they can quit the operation and return to the Manage Bookings sub-menu by entering 'x'.
    
    - The rules for the input values are as follows :
      - inputs are separated by commas, all inputs must have a length > 0
      - Date should have a format of DD-MM-YYYY and must be >= current date (bookings for past events cannot be cancelled)
      - The Event Code, Date and Email combination must exist in the bookings spreadsheet

    - When the user inputs valid data the application displays messages to provide information on how the data is being processed.  Cancelled bookings are deleted from the bookings spreadsheet.

    - As noted in the description of the Add Booking feature above (F08), duplicate bookings are allowed as the same person could make multiple bookings for a single event.  In this case, the Cancel Booking operation will only delete one booking - the first one it finds in the booking spreadsheet - and leave the remaining booking rows as they are.

      ![Cancel Booking Success](documentation/images/f09-cancel-booking-success.png)

    - Once the operation is complete and the user presses Enter, they are returned to the Manage Bookings sub-menu.  

- ###  __F10 Review Past Events__
    - From the main menu, when the user selects option 3 the Review Past Events functionality runs.  This feature examines all events with a Date < current date and also examines associated bookings.  On screen the following information is derived from the data and displayed to the user :

      - A table listing of all cancelled events which includes the Reason column 
      - A table listing of all events that went ahead which includes columns showing capacity of the event, the total seats booked and total seats booked as a percentage of capacity.
      - Numeric total of cancelled events
      - Numeric total of events that went ahead

      ![Review Past Events](documentation/images/f10-review-past-events.png)

- ###  __F011 User prompts and messages__ 
    - The user is given feedback regularly to let them know the status of processing and what the application is attempting to do.  To keep the terminal as uncluttered as possible, the screen is cleared after each operation (e.g. add or cancel), on each transition to a new menu and each time the user needs to re-enter data.  Functionality to pause processing and allow the user time to review the feedback before clearing the screen has been added -  the user is asked to "Press Enter to continue"  before the clear screen happens and the application moves on.

    - Examples of the messages that are displayed on successful execution of actions such as Review Past Events or Add Booking etc. are shown in the screen shots detailing the features above.   In addition, the application displays a range of error messages specific to error type when attempting data validation.  Some examples are below :

    - Example of error message displayed if the user does not enter the correct number of inputs :

      ![User Messages 1](documentation/images/f11-user-messages-1.png)

    - Example of error message displayed if the user enters an invalid date value :

      ![User Messages 2](documentation/images/f11-user-messages-2.png)

    - Example of error message displayed if the user attempts to cancel an event in the past :

      ![User Messages 3](documentation/images/f11-user-messages-3.png)

- ### __How these features support the User Stories__

    - The User Stories in the [User Experience (UX)](#user-experience-ux) part of this document are numbered 1 to 10.  The existing features are listed above as F01 to F11.  Below is a traceability matrix cross-referencing the user stories with the features, illustrating which features support which stories :

        ![User Story Feature Matrix](documentation/images/us-feat-matrix.png)

### Features which could be implemented in the future

- __Appropriate UI__

  As this application uses the command line interface it is not very user friendly for a human end-user.  An obvious future feature of this application would be to build a better user-interace layer using HTML/CSS and possibly Javascript to make it much more intuititve to use.

- __Extended Data Model__

  The data model representing the Events and Bookings is very simplistic in terms of the data elements it stores.  This could be extended to store additional data with more complex data relationship rules.  The data model and code could also be re-structured to use a better Object Oriented approach, where Events and Bookings could be handled as Object types with methods and attributes.

- __Extended Data Analysis__

  The Review Past Events feature of the application gives a breakdown of cancelled events vs events that weren't cancelled and shows % seats booked for those that went ahead.  Analysis of the data could be extended to find other information from the data, such as how frequently are certain events cancelled due to lack of bookings, which courses are most popular etc. and then this information could help the users plan ahead when trying to schedule events.  This type of information could also potentially be used to automate some tasks - e.g. automatically send an administrator an email highlighting a particular event has below a certain threshold of bookings coming up to it's scheduled date, so that the administrator has time to take action - e.g. send out a marketing email to draw attention to the event.

## Design

-   ### Flow Charts
    The diagrams below outline the high level flow of control within the application :

    <details>
       <summary>Diagrams</summary>

       ![Main Flowchart](documentation/flowcharts/ms3-main-flowchart.png)
       ![Manage Events A](documentation/flowcharts/ms3-option-1-A-manage-events.png)
       ![Manage Events B](documentation/flowcharts/ms3-option-1-B-manage-events.png)
       ![Manage Bookings A](documentation/flowcharts/ms3-option-2-A-manage-bookings.png)
       ![Manage Bookings B](documentation/flowcharts/ms3-option-2-B-manage-bookings.png)
       ![Review Past Events](documentation/flowcharts/ms3-option-3-review-past-events.png)
    </details>

    
## Technologies Used

### Languages Used

-   [Python 3.8.10](https://www.python.org/)

### Frameworks, Libraries & Programs Used

-   [Google Spreadsheets:](https://en.wikipedia.org/wiki/Google_Sheets) used as the external data store for the Events and Bookings data used by the project.
-   [Google Drive API:](https://developers.google.com/drive/api/v3/about-sdk) used to generate credentials used in the project to securely access the Google Spreadsheet. 
-   [Google Sheets API:](https://developers.google.com/sheets/api) used to support interactions (e.g. read/write functionality) between the code and data stored in the Google Spreadsheet.
-   [gspread:](https://docs.gspread.org/en/latest/) Python API for Google Sheets
-   [Google Auth:](https://google-auth.readthedocs.io/en/master/) Google authentication library for Python required to use the credentials generated for Google Drive API
-   [Google Drawings](https://en.wikipedia.org/wiki/Google_Drawings) used to create the flowcharts outlining the functionality of the project.
-   [Git:](https://git-scm.com/) was used for version control by utilising the Gitpod terminal to commit to Git and Push to GitHub.
-   [GitHub:](https://github.com/) is used as the respository for the projects code after being pushed from Git.
-   [Heroku:](https://heroku.com) is used to deploy the application and provides an enviroment in which the code can execute

## Testing

### Validator Testing

- [Python Validator](http://pep8online.com/)

    - result for `run.py`

      ![Python Validation Results](documentation/validation/python-pep8online-validation-results.png)

### Test Cases and Results

- The below table details the test cases that were used, the results and a cross-reference to the Feature ID that each test case exercised (click to open image):

  <details>
    <summary>Test Cases</summary>

    ![Test Cases](documentation/images/test-cases.png)
  </details>
  

### Known bugs

- Problem with clear screen.

    Originally the clear function was implemented using the below code snippet :
        
          if name == 'nt':
            _ = system('cls')
          else:
            _ = system('clear')

    the reference for this code is: [Clear Screen](https://www.geeksforgeeks.org/clear-screen-python/).  

    This worked fine when testing within the gitpod environment, but did not work when the application was deployed to Heroku.  No error messages or warnings were displayed when the application was run on the Heroku platform, the clear screen simply did not do anything.
    To solve this problem I replaced the above code with this code :

        print('\033c')

    the reference for this code is: [Clear Screen - ASCII sequence](https://stackoverflow.com/questions/2084508/clear-terminal-in-python/2084521).
    This appears to to work when tested in the gitpod environment and in the version deployed to Heroku.


## Deployment

### How to clone the GitHub repository
  
  <details>
    <summary>Steps to create a local clone</summary>
  
   - Go to the https://github.com/elainebroche-dev/ms3-event-scheduler repository on GitHub 
   - Click the "Code" button to the right of the screen, click HTTPs and copy the link there
   - Open a GitBash terminal and navigate to the directory where you want to locate the clone
   - On the command line, type "git clone" then paste in the copied url and press the Enter key to begin the clone process
   - Changes made to the local clone can be pushed back to the repository using the following commands :

        - git add *filenames*  (or "." to add all changed files)
        - git commit -m *"text message describing changes"*
        - git push
      
   - N.B. Any changes pushed to the master branch will take effect on the live project because automatic deployments are enabled in Heroku for this project.

   - N.B. Any data changes made through the use of the application will take effect in the live project ms3-event-scheduler Google spreadsheet.
   </details>

### How to create and configure the Google spreadsheet and APIs
  
  <details>
    <summary>Steps to setup and configure access to data</summary>

  - Create the Google Spreadsheet 

     - Log in to your Google account (create one if necessary)
     - Create a Google Spreadsheet called 'ms3-event-scheduler' on Google Drive with 2 pages/sheets, one called 'events' and one called 'bookings'.  
     - In row 1 of the events sheet, enter the headings : Event Code, Event Name, Date, Host, Capacity, Status Reason.
     - In row 1 of the bookings sheet, enter the headings : Event Code, Date, Name, Email, Seats
     - The initial sample data used in this project can be seen here, however it is not necessary to use that data : [Content](#content)

  - Set up APIs using the Google Cloud Platform

     - Access the [Google Cloud Platform](https://console.cloud.google.com/)
     - Create a new project and give it a unique name, then select the project to go to the project dashboard
     - Setup Google Drive credentials 

        - Click on the hamburger menu in the top left of the screen to access the navigation menu
        - On the left hand menu select 'APIs and Services' and then 'Library'
        - Search for Google Drive API
        - Select Google Drive API and click on 'enable' to get to the API and Services Overview page 
        - Click on the Create Credentials button near the top left of the screen
        - Select 'Google Drive' API from the dropdown for 'Credential Type'
        - Select the 'Application Data' radio button in the 'What data will you be accessing' area
        - Select the 'No, I'm not using them' for the 'Are you planning to use this API with Compute Engine, Kubernetes Engine, App Engine, or Cloud Functions?' area
        - Cick Next
        - On the Create Service Account page, step 1 is to enter a service account name in the first text box.  Any value can be entered here.
        - Click on 'Create and Continue'
        - On step 2, 'Grant this service account access to project',  select Basic -> Editor from the 'Select a Role' dropdown.
        - Click on Continue
        - On step 3, 'Grant users access to this service account', simply press Done, no input is necessary
        - On the next page, click on the service account name created (listed under the Service Accounts area) to go to the configuration page for the new service account.
        - Click on the KEYS tab at the top middle of the screen.
        - Click on the Add Key dropdown and select Create New Key.
        - Select the JSON radio button then click Create. The json file with the new API credentials will download your machine. 
        - Rename the downloaded file to creds.json.  This filename is already listed in the project .gitignore file and so no further action will be needed to prevent it being accidentally uploaded to github 
        - Copy the new creds.json file into the local clone
        - In the creds.json file, copy the value for "client email" and then on Google Drive, share the spreadsheet created above with this email address assigning a role of Editor similar to the image shown below :

          ![Share Spreadsheet](documentation/images/share-google-spreadsheet.png)

     - Enable Google Sheets API 
        
        - Go back to the dashboard for the project on Google Cloud Platform and access the navigation menu as before
        - On the left hand menu select 'APIs and Services' and then 'Library'
        - Search for Google Sheets API
        - Select Google Sheets API and click on 'enable'

  - Install gspread and google-auth libraries in the development environment using the command 'pip3 install gspread google-auth'
  
  </details>

### How this site was deployed to Heroku 
   
  <details>
    <summary>Steps followed to deploy</summary>

  - The requirements.txt file in the project was updated to include details on the project dependencies. Steps to do this are :

    -  Enter the following command at the terminal prompt : 'pip3 freeze > requirements.txt'
    -  Commit resulting changes to requirements.txt and push to github

  - Log in to [Heroku](https://heroku.com/), create an account if necessary.
  - From the Heroku dashboard, click the Create new app button.  For a new account an icon will be visible on screen to allow you to Create an app, otherwise a link to this function is located under the New dropdown menu at the top right of the screen.
  - On the Create New App page, enter a unique name for the application and select region.  Then click Create app.
  - You will then be brought to the Application Configuration page for your new app.  Changes are needed here on the Settings and Deploy tabs.
  - Click on the Settings tab and then scroll down to the Config Vars section to set up the private Environment Variables for the application - i.e. the credentials used by the application to access the spreadsheet data.
  - Click on Reveal Config Vars.  In the field for key enter 'CREDS' and paste the entire contents of the creds.json file into the VALUE field and click ADD. A description on the creation of the creds.json file is documented in  [How to create and configure the Google spreadsheet and APIs](#how-to-create-and-configure-the-google-spreadsheet-and-apis) above.
  - Next, scroll down the Settings page to Buildpacks.  Click Add buildpack, select Python from the pop up window and click on Save changes.  Click Add buildpack again, select Node.js from the pop up window and click on Save changes.  It is important that the buildpacks are listed Python first, then Node.js beneath.
  - Click on the Deploy tab on the Application Configuration page.
  - Select GitHub as the Deployment Method and if prompted, confirm that you want to connect to GitHub.  Enter the name of the github
repository (the one used for this project is https://github.com/elainebroche-dev/ms3-event-scheduler) and click on Connect to link up the Heroku app to the GitHub repository code.
  - Scroll down the page and choose to either Automatically Deploy each time changes are pushed to GitHub, or Manually deploy - for this project
Automatic Deploy was selected.
  - The application can be run from the Application Configuration page by clicking on the Open App button.
  - The live link for this project is (https://ms3-event-scheduler.herokuapp.com/)

 </details>

## Credits 

### Content 
- The Google spreadsheet (ms2-event-scheduler) that the application uses has the following fictitious initial data which was set up manually :

   <details>
     <summary>Events Sheet</summary>

     ![Events](documentation/images/initial-content-events.png)
   </details>
   <details>
     <summary>Bookings Sheet</summary>

     ![Bookings](documentation/images/initial-content-bookings.png)
   </details>
    

### Code 
- Code on how to clear the screen came from information on this website : [Clear Screen](https://www.geeksforgeeks.org/clear-screen-python/)
- Code to clear screen using an ASCII escape sequence came from this website: [Clear ASCII Escape](https://stackoverflow.com/questions/2084508/clear-terminal-in-python/2084521) 
- Code on extracting 2 digit months and days from a date came from information on this website : [2 digit month and day](https://stackoverflow.com/questions/15509345/extracting-double-digit-months-and-days-from-a-python-date)
- Code to format dates was based on information from this website : [Date Formatting](https://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/)
- Additional information on date manipulation came from this website : [Date handling](https://docs.python.org/3/library/datetime.html)
- Information on using the gspread API came from this website : [gspread API](https://docs.gspread.org/en/latest/user-guide.html#getting-all-values-from-a-worksheet-as-a-list-of-lists) 
- Code using a lambda function to sort came from information on this website: [Lambda Sort](https://stackoverflow.com/questions/4174941/how-to-sort-a-list-of-lists-by-a-specific-index-of-the-inner-list/4174955) 
- Code to format data for printing in a table on screen came from information on this website : [Table Formatting](https://stackoverflow.com/questions/61285626/print-list-of-lists-in-neat-columns-table) 
- Code on how to use gpspread API to delete rows came from this website : [gspread Delete](https://docs.gspread.org/en/latest/api.html?highlight=delete%20rows#gspread.models.Worksheet.delete_rows) 
- Information on how to use 'in' came from this website : [In](https://stackoverflow.com/questions/22304500/multiple-or-condition-in-python) 
- Code to help validate data values came from information on this website: [Date Validation](https://stackoverflow.com/questions/47547403/regular-expression-for-mm-dd-yy-date-format-not-finding-any-match-in-python)
- Code to use an RE to validate format of email address came from information on this website : [Email RE](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/)
- Code to extend a list came from information on this website: [Extend List](https://www.datacamp.com/community/tutorials/python-list-methods?utm_source=adwords_ppc&utm_campaignid=898687156&utm_adgroupid=48947256715&utm_device=c&utm_keyword=&utm_matchtype=b&utm_network=g&utm_adpostion=&utm_creative=229765585183&utm_targetid=dsa-429603003980&utm_loc_interest_ms=&utm_loc_physical_ms=9047196&gclid=CjwKCAjw_o-HBhAsEiwANqYhp7Kw0hp2dNCHcgDIIW4aLzI7CKRIUFqkaZSPoqyrk2MnuRVC7bYLbxoC3JYQAvD_BwE) 


### Acknowledgments

- Thank you to my mentor Brian Macharia for his ongoing help and feedback.  He has provided me with lots of tips and resources to help improve my coding and testing.  Thanks also to my tutor Kasia Bogucka for facilitating stand-ups and workshops which are always very useful for catching up with everyone and getting some really useful advice and support.