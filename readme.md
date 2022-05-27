# Project Title: Typist
## Introduction
The Typist website is a web application that allows users to test their typing speed, publish quotes, and keep records of their progress.
Similar to other TouchTyping websites (specially KeyHero.com), the website will have a page named Practice that allows registered users to retrieve a random quote and practice on it.
Each quote will have its own statistics, such as the fastest WPM (words per minute) globally and locally, the user's score, and other information.
Users are also allowed to interact with the quote by liking it or disliking it.
Each user will have a profile that shows all their records, such as their best WPM, the quotes they encountered, and other information.
Each quote will have its own page that acts as a quote profile where users are allowed to see information about the quote.
Finally, users are allowed to search for a particular quote or other users on the website.
## Project Files
### Templates and Views
* **layout.html:** This is the main template for the application's UI and all other HTML files in the folder will extend it.
Also, this page will contain a write quote button the will display a **Bootstrap Modal.** 
* **index.html:**   This is the default route the user will see and will contain general statistics about users, quotes, and countries, such as their ranking on the site and it will render from the **index function** in the **views.py** file that is responsible to query the necessary data from the database.
*  **login.html and registration.html:** self-explanatory and will render from the **login and registration functions.**
*  **players.html:** will show a list of random players (users) and allow the user to ***search*** for other players as well and it will render from the **players function** for database queries.
*  **practice.html:** This page will use mostly **Javascript** for both UI elements (HTML tags) and querying data from the database using APIs.
 Users will be asked to press the ***Enter*** button to start the game (writing the quote) and immediately the page will be filled with a new quote and all the necessary information about that quote by making an **API request** to the database from the **index.js** file.
Inside the index.js there is an **Event Listener** that detects the user's keyboard presses, converts each press to a character, and determines whether the user has ***finished*** writing, ***skipped*** to the next random quote, or ***made a mistake*** while writing.
All events on this page are handled by Javascript such as liking or disliking a quote, updating and querying from the database and ***play sounds.***
* **view_quote.html and quotes.html:** both responsible for searching for a quote and displaying a quote with all its statistics in the view_quote.html.
### Models.py
* **User:** This model will inherit from the AbstractUser and add two additional fields (country and date of join).
* **Quote:** This Will contain information about the quotes.
* **Like:** Will contain information about user's interaction with each quote.
* **Records:** Will contain information about each game played (quote practice).
This model will be used to generate graphs and display information about both user records and quote records.

### Utils.py
The file contains two functions, one to generate a graph for a quote and the other to generate a graph for the user using the **matplotlib** library.

### Static Folder
Will contain all the assets such as the graphs generated and other icons used to display in the application in addition to the **index.js** and **styles.css** files.
## Distinctiveness and Complexity
The project is distinctive from other projects during CS50W since it is not similar to other projects in the implementation I had to take my approach to implement the features in this project.\
To ensure that the project is not similar to other projects, I avoided social networks applications because they are similar in implementation, also I tried to minimize the adoption of functionalities and UI behaviors that are used in the previous projects.\
In order for the project to meet the complexity requirements, I decided to implement most of what I learned during CS50W in this project, as a result, the project make use of Javascript, Python, CSS, Bootstrap, Database Models, and JSON APIs.\
The project uses JavaScript to update the content of the page dynamically as the user interacts with the page in addition to handling a broad range of user events from keyboard presess and making API calls at the same time.\
Also, making use of Bootstrap Grid System and Flexbox the project meet the requirement of mobile responsiveness.\
Finally, The project makes use of database mode by storing and manipulating data such as users information, quotes, quotes interactions, and rankings.
