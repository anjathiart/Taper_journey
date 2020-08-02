# CS50x 2019 Final Project: TAPER JOURNEY
This document briefly explains my final project web application, called Taper Journey. It is a mental health tracking app that allows you to track daily psychiatric medications, dosages, mood, side-effects. It also has a journal feuture where one can write in on a daily basis.

Here is a very short video link: https://www.youtube.com/watch?v=gRXK-b9SqEg

## Motivation for this project
I came up with this idea as I am a mental health patient and, at the time, was on various medications, some of which I wanted to discontinue using. As most mental health patients know, tapering off of these drugs are not easy, and stopping cold-turkey can cause major withdrawals and relapses. It is thus very important to taper off medications slowly, with care, and under strict medical supervision. This made me think of creating an app that helps one to keep track of such a tapering-off journey to see progress when times are tough, or to flag issues with the process. The bigger idea is to have this app integrate with healthcare practitioners and services, but this is beyond the scope of this first version, call it Beta, call it MVP, of Taper Journey.

And so the name "Taper Journey" was born. However, I soon realized that such an app can be used for tracking the tapering onto drugs, as well as for any mental health patient who wants to keep track / keep a record of their mental health. Think of it like a pain-log, calorie-log, etc. I decided to stick with the name Taper Journey, even though the app can be used whether tapering or not. The whole mental health process is a taper in some way or form; tapering up to a better outlook, tapering down from a manic episode, and so on.


## Technologies used
I have used the technologies as learnt in the course for web application development.

- Front-end: Jinja, HTML, javascript, JQuery, JQuery UI, CSS, Ajax, Bootstrap 4, Font Awesome
- Back-end: Python, Flask, SQLlite
- Templating engine: Jinja
- IDE: CS50 IDE (online version)
- Debugging: CS50 IDE terminal, Chrome developer tools, Python / Flask logs
- DevOps: Git, Github
- Submission: CS50 IDE (online version), YouTube, Git, Github, Markdown


## Taper Journey Beta version / MVP
The project submission is based on the Minimum Viable Product (MVP) model. It provides very basic signup and signin functionality with backend validation. Once signed in, the user is redirected to the home page which is similar to a user dashboard, showing the latest statistics tracked, or a welcome message if they are a new user. The navigation bar also contains a link to the "History" page, the "Journal" page and a link to logout.


### The Journey Status Dashboard / Home Page
For a user that has already started tracking information, the dashboard (home page) shows various statistics for the latest date that was tracked. It also shows the last journal entry that was made. From here, the user can select the update / edit button which opens a modal where various tasks can be performed:

- Add / remove medications
- Add / remove side-effects
- Set / update mood
- Select different dates from the calendar drop down to either track data in hindsight, or edit previous entries.
- Open the journal dialogue to edit / delete / create a journal entry for the chosen date.

The dashbaord and data tracking inputs have both front-end and back-end validation built in. When data is entered incorrectly, an alert is used to give the user some advise on what to do to move forward. There are also popovers for various buttons / icon buttons to explain their functionality to the user.


### History Page
This page displays a table, in chronological order, detailing every entry, for every day, and every medication respectively. The table currently has a filter feauture which allows the user to filter the table based on a specified medication that they have tracked throughout their journey. In future, the idea is to show plots / visualizations of dosages and mood over time, and that is why I decided to add this filter in: so that one can see the data over time for just one medication. The plots are not implemented in the MVP / Beta version, but the history table and filter is fully functional.


### Journal Page
The journal page is a simple page that outputs all the journal entries in chronological order, similar to a blog page. It contains no data statistics, but only the date followed by the journal entry for that day, keeping it clean and readable. In future it would be nice to have a edit button for direct editing of the entry, a delete button, as well as a side-bar with a list of links for all the entry-dates.


### API endpionts
The information shown on the pages mentioned above, as well as the information that is entered / updated / deleted via the user, is all dependent on the backend "api endpoints", or "routes". The backend calls contain the logic, database queries and client-side responses in one "layer", or in one "route function". In more complex applications it is better to split the database models, logic, and api responses into separate layers.

Here are a list of some / most of my routes / endpoints / API calls, with a brief discription of each ones main function:

- Signup a user, and save / POST their credentials in the database, if successful redirect them to the signin page, otherwise reload the signup page.
- Sign a user in and start their session and redirect them to the home page / index route if they enter the correct credetials, otherwise reload the signin page.
- The entry route ('/') serves the data for the last date tracked by the user to the front-end to set / render the initial state of the application. If no data has been captured for the user, the data object served contians this information.
- Get a users data for a specified date from the database and serve it to the front-end for rendering / updating the HTML.
- Post / update a users data based on client-side inputs / selections for a specified date, and store it in the database if it is valid data. If not, redirect to an error page.
- Get a users latest journal entry from the database and serve it to the front-end for rendering / updating the HTML. If no such entry exists, the data object served contains this information.
- Post / update a users journal entry for a specified date, storing it in the database.
- Get a list of all the medications supported by the app. In future I would like to implement an external API call to pull in all psychiatric / insomnia / anxiety type medications.
- Get a list of all side-effects supported by the app. In future I would like to implement an external API call to pull in the most commorn side-effects of the medications supported.
- Log out the user and kill their session. Redirect to the login page.

The above "routes" / "endpoints" have fallbacks if there is a server side error, mostly redirecting the user to an apology / error page.

### Future considerations
This is just a proof of concept, MVP type demo application. At some stage one has to stop working on the project, and I think I have done enough, learnt enough, struggled through enough bugs, and researched enough to feel like I have really gotten the most out of this final project.

There is a lot of scope to expand this project, and I can list at least 50 additional features I would want to implement in the Beta version. I have mentioned a few of these in this document, but I will leave the rest up to your imagination for now.

## Conclusion
Thank you for reading my brief description / implementation of my final project, a Beta / MVP / Demo version of Taper_Journey, a mental health tracking app. There are a lot of feuatures that can still be added. but I think the big picture end-goal is to integrate this tool with primary healthcare facilities / professionals. I think this can really add value on both sides of the situation, and save money and time, and also maybe lives, in the long run.

## Thank you
Thank you to Prof. Malan and all his colleugues who created and facilitated this great course. Thank you also to the community of students who helped me along the way. I have learnt a lot from this course, and have already applied a lot of the knowledge in my new career as a Software Engineer. Even though we use a different stack, the concepts tought has been stack-independent for me. I have grasped so much new knowledge and also gained more appreciation for modern frontend frameworks like Vue.JS, CSS flexbox, and CSS preprocessors. The backend is still a huge learning curve for me, and I've enjoyed it a lot.










