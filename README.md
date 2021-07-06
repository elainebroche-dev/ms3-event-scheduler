<h1 align="center">Event Scheduler</h1>

[View the live project here](https:// to be written)

To be written

![Mockup](documentation/images/resp-mockup.png)

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

1. To be written

## Features

### Existing Features

how do I want dates to work ? - this needs to go into the readme to clarify
upcoming should show today and the future for both bookings and events
Can cancel events or bookings for >= today
Can create events or bookings for >= today
review events should show data < todays date


-   __F01 To be written__
    - To be written

      ![To be written](documentation/images/f01-to be written)

- __How these features support the User Stories__

    - The User Stories in the [User Experience (UX)](#user-experience-ux) part of this document are numbered ??????.  The existing features are listed above as F01 to F?????.  Below is a traceability matrix cross-referencing the user stories with the features, illustrating which features support which stories :

        ![User Story Feature Matrix](documentation/images/to be written)

### Features which could be implemented in the future

- __To be written__


## Design
- REVIEW RULES AROUNT >= <=> dates and - explain business rules and check code and diagrams match
-   ### Flow Charts
     ![Main Flowchart](documentation/flowcharts/ms3-main-flowchart.png)
     ![View Upcoming Events](documentation/flowcharts/ms3-option-1-view-upcoming-events.png)
     ![Manage Events](documentation/flowcharts/ms3-option-2-manage-events.png)
     ![Manage Bookings](documentation/flowcharts/ms3-option-3-manage-bookings.png)
     ![Review Past Events](documentation/flowcharts/ms3-option-4-review-past-events.png)
    
## Technologies Used

### Languages Used

-   [?????](to be written)

### Frameworks, Libraries & Programs Used

-   [Google Spreadsheets](https://en.wikipedia.org/wiki/Google_Sheets) used as the external data store for the Events and Bookings data used by the project.
-   [Google Drive API](https://developers.google.com/drive/api/v3/about-sdk) used to generate credentials used in the project to securely access the Google Spreadsheet. 
-   [Google Sheets API](https://developers.google.com/sheets/api) used to support interactions (e.g. read/write functionality) between the code and data stored in the Google Spreadsheet.
-   [gspread](https://docs.gspread.org/en/latest/) Python API for Google Sheets
-   [Google Auth](https://google-auth.readthedocs.io/en/master/) Google authentication library for Python required to use the credentials generated for Google Drive API
-   [Google Drawings](https://en.wikipedia.org/wiki/Google_Drawings) used to create the flowcharts outlining the functionality of the project.
-   [Git:](https://git-scm.com/) was used for version control by utilising the Gitpod terminal to commit to Git and Push to GitHub.
-   [GitHub:](https://github.com/) is used as the respository for the projects code after being pushed from Git.

## Testing

### Validator Testing


- [????](to be written)

    - result for ?????
      ![??????](documentation/validation/to be written)

      need to use http://pep8online.com/
    
### Test Cases and Results

- The below table details the test cases that were used, the results and a cross-reference to the Feature ID that each test case exercised (click to open image):

  <details>
    <summary>Test Cases</summary>

    ![Test Cases](documentation/images/to be written)
  </details>
  

### Known bugs

- to be written

## Deployment

### How this site was deployed - to be written

- to be written

  The live link can be found here - [???????](to be written) 


  notes on deployment :
  usual git stuff needed

The Code Institute Python Essentials template was used to build the project Gitpod workspace.  This template
includes files and code to support deployment in a mock terminal on a web page.

A newline character was added to the end of each string used with the input function because due to how the
software to create the mock terminal works, the newline is needed so that the text for the input request shows
on screen.

The requirements.txt file in the project was updated to include details on the project dependencies.
Steps to do this are :

1. Enter the following command at the terminal prompt : 'pip3 freeze > requirements.txt'
2. Commit resulting changes to requirements.txt and push to github

Login to your Heroku account.  If you don't have one, create one on www.heroku.com.  Enter your name, email and 'Student' can be selected for the Role value.  Choose a value for Country based on your location and select "Python" as the Primary development language.  

Once the Create button has been clicked, Heroku will send a confirmation email, to complete account creation click on
the link in this email.

Heroku will then bring you to a page to set up your password and log in.

Accept the Heroku terms of service and then you will be brought to the dashboard for your account.

If this is a new account an icon will be visible on screen to allow you to Create an app, alternatively you can find a link to this function under the New dropdown menu at the top right of the screen.

From the Heroku dashboard, click the Create new app button.

On the Create New App page, enter a unique name for the application and select your region.  Then click Create app.

You will then be brought to the application configuration page for your new app.  The important tabs on this page are Deploy and Settings.

Click on the Settings tab and then scroll down to the Config Vars section to set up the private Environment Variables for the application - i.e. the credentials used by our application to access the spreadsheet data.

*** Be careful here !!! we need details on how exactly to create the creds.json file as this is not something that is available
to someone other than ourselves - so need to back up here on this *****
Click on Reveal Config Vars.  In the field for key enter 'CREDS' and paste the entire contents of the creds.json file into the VALUE field

Next, scroll down the Settings page to Buildpacks.  Click Add buildpack, select Python from the pop up window and click on Save changes.  Click Add buildpack again, select Node.js from the pop up window and click on Save changes.  It is important that the buildpacks are listed on the page in the order shown in the diagram.

Now go to the Deploy tab for the application configuration.

Select GitHub as the Deployment Method and if prompted, confirm that you want to connect to GitHub.  Enter the name of the github
repository (ms3-event-scheduler) and click on Connect to link up the Heroku app to the GitHub repository code.

Scroll down the page and decide if you want to Automatically Deploy each time changes are pushed to GitHub, or Manually deploy - for this project, Automatically Deploy was selected.









### How to clone the repository - to be written

- Go to the https://github.com/elainebroche-dev/ms2-anagram repository on GitHub 
- Click the "Code" button to the right of the screen, click HTTPs and copy the link there
- Open a GitBash terminal and navigate to the directory where you want to locate the clone
- On the command line, type "git clone" then paste in the copied url and press the Enter key to begin the clone process
- Changes made to the local clone can be pushed back to the repository using the following commands :

  - git add *filenames*  (or "." to add all changed files)
  - git commit -m *"text message describing changes"*
  - git push

- N.B. Any changes pushed to the master branch will take effect on the live project

## Credits 

### Content 
- (https://www.geeksforgeeks.org/clear-screen-python/) code to clear the screen - to be written

### Code 
- To be written
- (https://stackoverflow.com/questions/15509345/extracting-double-digit-months-and-days-from-a-python-date) code to return 2 digit month/day - to be written
- (https://www.cyberciti.biz/faq/howto-get-current-date-time-in-python/) - might use this to help format
- (https://docs.python.org/3/library/datetime.html) - help with dates
- (https://docs.gspread.org/en/latest/user-guide.html#getting-all-values-from-a-worksheet-as-a-list-of-lists) - doc on api
- (https://stackoverflow.com/questions/4174941/how-to-sort-a-list-of-lists-by-a-specific-index-of-the-inner-list/4174955) - information on sort using lambda
- (https://stackoverflow.com/questions/61285626/print-list-of-lists-in-neat-columns-table) - code to format list for printing
- (https://docs.gspread.org/en/latest/api.html?highlight=delete%20rows#gspread.models.Worksheet.delete_rows) - referred to for gspread delete
- (https://stackoverflow.com/questions/22304500/multiple-or-condition-in-python) - usage of 'in'
- (https://stackoverflow.com/questions/47547403/regular-expression-for-mm-dd-yy-date-format-not-finding-any-match-in-python) - ideas on how to verify date
- (https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/) regular expression to validate email address
- (https://www.datacamp.com/community/tutorials/python-list-methods?utm_source=adwords_ppc&utm_campaignid=898687156&utm_adgroupid=48947256715&utm_device=c&utm_keyword=&utm_matchtype=b&utm_network=g&utm_adpostion=&utm_creative=229765585183&utm_targetid=dsa-429603003980&utm_loc_interest_ms=&utm_loc_physical_ms=9047196&gclid=CjwKCAjw_o-HBhAsEiwANqYhp7Kw0hp2dNCHcgDIIW4aLzI7CKRIUFqkaZSPoqyrk2MnuRVC7bYLbxoC3JYQAvD_BwE) - information on extend


### Media 
- To be written

### Acknowledgments

- To be written