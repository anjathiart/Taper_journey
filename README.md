# Taper_jourey
An app where you can track your journey of being on psychiatric / psychoactive medications

## Notes as taken from my perosnal website readme:

### Finish up Taper Journey in various versions (1. MVP and CS50 final project, 2. Added funcitonality XX, etc.
+ Fix errors with new signups
+ Add interaciton to the history table
+ Add graphs and visulizations. start with canvas frontend js implementation
+ Password reset
+ Share your information with a third party such as your psychologist / friend / what ever
  + They will be able to comment and the thread will be private, just for you and them to see
  + They can't edit anything, just view contnet.
+ Change login and signup to be a single page so that there are two tabs one for sign in and one for signup
+ automatically log users in once registerd
+ Account page to manage details such as password, email and people who can view your profile.
+ Authorizatino
+ Front end validation
+ Back end validation
+ Maybe learn how to include a linting rules
+ Maybe learn how to write and run tests
+ Write models (?? i think this is what models are) standardised functionf for SQLlite queries that makes the code cleaner and is reusable
+ Comment the code
+ Add sorting of table, search, sort by date
+ For the progress plots, allow users to specify time periods (week, month, year, inception
+ Try to automate a way to add fake data to the database for better proof-of-concept highligthing
+ Add a Coming soon page with a table of all the feutures and functinoality that still has to be added to the site.
+ revisit all the html and css to incorporate flexbox and grid
+ revisit all the css and html to ensure the website renders well on tablets and smartphones
+ add markdown capability to the text input for the journal
+ use the drugs.com api to get medication lists
+ Add a page where users can explore medication information, especially side effects and withdrawal effects using an API
+ Use pills to add / remove drugs that are being tracked instead of checkboxes
+ revisit code to make better use of Jinja templating and html requests to render the tempaltes. My code is probably way too complicted right now as I call jquery get/post methods to get new data and this is causing me problems when i want to dynamically update the inforamtino of the pagge and not have to refresh the page. requesting html and data would mabye overcome this?
+ Add title to journal posts. Multiple journals per day?
+ Add a smoking tracker option - or use an API to get this information from other apps -- don't reinvent a smoking app.
+ What about illegal drug tapering and logging for addicts. This can be shared with psychologist and psychiatrist
+ What about the option for daily medication reminders? This allows me to incorporate a mobile notification functionality which is useful. 
+ Create screencast 
  + this screencast should probably be done once the app is working for the CS50 course to speed up getting that certificate and moving on to CS50W.
  + Can do another screencast once the full app is done
+ Determine MVP
+ Look at the above and choose what is enough as a MVP and deploy using Heroku
+ Allow users to add custom medications that are not in the list
+ How to have a dropdown with data from a huge API source that shows only certain amoount of options at a time and incorporates searcg fitering and loads the data as the user scrolls the dropdown / searches.
+ Work on mock data for the application that can be imported using some kind of automated scripting
  + Json knowledge ?
  
#### Technologies and tools:
+ Front end: Jinja, HTML, javascript, Jquery, CSS, Ajax, Bootstrap, Font Awesome
+ Backend: Python, Flask, SQLlite
+ IDE: CS50 IDE
+ Debugging: terminal, chrome dev, CS50 ide
+ DevOps: Git github
+ Deployment: Heroku
