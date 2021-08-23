# Calorie Counter

## Link to deployed site via Heroku:

Across almost all demographics of people, health and wellness is an overall priority and concern; however, many people struggle with maintaining a healthy diet and active lifestyle even when they set goals for themselves. An attainable way to either begin or keep up with a health and wellness journey is to set a daily caloric intake goal. A daily caloric intake goal can be kept track of by having the number of calories per food item ate in a day be added to the daily count, while the number of calories burned in an exercise participated in be subtracted from the total to equal a net amount for the day. Unfortunately, the amount of calories for food items and exercise types aren't common knowledge for most people. In addition, many people struggle with their goals when they feel like they are alone so knowing other people are on a similar journey can be comforting and beneficial to goal success.

Calorie Counter was designed to meet the needs of people looking to keep themselves accountable for their daily caloric intake goals and provide a space to gain a network of support from likeminded individuals all in one application. At the homepage of the application, users are able to learn more about the application, sign up for an account, or log in to an already registered account. After registration and/or logging in, users are redirected to their profile page, where they can view their journal and past entries, register new food items or exercise types for their journals, view and join support groups with similar users, and follow or be followed by different individual users in order to see other people's journals.

API Info

The Nutritionix API (https://developer.nutritionix.com/) is used to search up the different food items or exercise types that are inputted by the user to receive the caloric count for that input.

Database Models



Technologies



Installation and Testing

To run this code locally, clone this repository to your computer, set up a virtual environment, and install the requirements. Create a local database and test database in PostgreSQL, and update the app config database variables in app.py and various test files. The Nutritionix API is free (https://developer.nutritionix.com/) but in order to use, acquisition of an ID and Key are required. May set the required API ID and API Key in the secret.py file.

To run tests, use Python: run all tests in VSCode, or use the terminal command "python -m unittest" to run all tests. To run test files individually, use the terminal command "python -m unittest <filename>".