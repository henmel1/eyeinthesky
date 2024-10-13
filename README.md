# Eye In The Sky

## Inspiration
Our team was initially inspired to create this project by the concerningly high number of insecure cameras around the world. We wanted to raise awareness on how easily accessible these cameras are and their prevalence globally.

## What it does
Eye In The Sky is an interactive world map that geolocates and provides links to insecure cameras around the world. It utilizes OSINT techniques such as Google Dorking and an Open Source Shodan.io script to find vulnerable security cameras, laptops, personal cameras and more. Additionally, we have a counter to keep track of the number of cameras found, with around 300 currently mapped.

## How we built it
For the frontend, our team used React, JavaScript, and HTML/CSS, and for the backend we used Python and Flask. The project is hosted in an AWS environment using Defang. The Shodan API was used to scrape web cameras and the IP2Location API was used to get locations from the IPs. Coordinate data and the URLs were put on a REST API using Flask-RestX. We used MapLibre to display camera markers on an interactive map.

## Challenges we ran into
Our biggest challenge was making the user interface smooth and efficient while also intuitive and quick-loading. We spent a lot of time working with the React front end to ensure maximum user friendliness and performance. These issues were resolved using memorization and debouncing.

## Accomplishments that we're proud of
Our team is proud that we were able to efficiently visualize the hundreds of unsecured cameras we found online. We believe that this project provides a new perspective to just how widespread unsecure cameras are on almost every continent of the world.

## What we learned
While working on Eye In The Sky, we learned how to efficiently delegate tasks to each individual member of the team based on their individual strengths and prior technical background. This project also practiced our team's problem-solving abilities with unfamiliar technology such as Defang and MapLibre.

## What's next for Eye In The Sky
In the future, we plan on improving the user interface of the application and creating an authentication system for individual users. On the backend we will implement more precise Google Dorking techniques through the usage of LLMs and enhanced web scraping techniques.
