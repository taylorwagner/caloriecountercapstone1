# Calorie Counter

## Link to deployed site via Heroku:

Across almost all demographics of people, health and wellness is an overall priority and concern; however, many people struggle with maintaining a healthy diet and active lifestyle even when they set goals for themselves. An attainable way to either begin or keep up with a health and wellness journey is to set a daily caloric intake goal. A daily caloric intake goal can be kept track of by having the number of calories per food item ate in a day be added to the daily count, while the number of calories burned in an exercise participated in be subtracted from the total to equal a net amount for the day. Unfortunately, the amount of calories for food items and exercise types aren't common knowledge for most people. In addition, many people struggle with their goals when they feel like they are alone so knowing other people are on a similar journey can be comforting and beneficial to goal success.

Calorie Counter was designed to meet the needs of people looking to keep themselves accountable for their daily caloric intake goals and provide a space to gain a network of support from likeminded individuals all in one application. At the homepage of the application, users are able to learn more about the application, sign up for an account, or log in to an already registered account. After registration and/or logging in, users are redirected to their profile page, where they can view their journal and past entries, register new food items or exercise types for their journals, view and join support groups with similar users, and follow or be followed by different individual users in order to see other people's journals.

API Info

The Nutritionix API (https://developer.nutritionix.com/) is used to search up the different food items or exercise types that are inputted by the user to receive the caloric count for the input.

User Flow
1. Users are at the homepage of the application, where they are given three options: navigate to the about page to learn more, sign up for an acccount, or log in

2a. About page tells the users more details about the application
2b. Sign up page, users complete a registration form with the following valid information: username, password, email, daily caloric goal number, city, and state
2c. Log in page, users complete a form to authenticate their credentials with the app via username and password

3. Once successfully signed up or logged in, users will have access to their profile page -- navbar while a user is logged in has the "about" page option still but no longer sign up/log in options -- along with the about page option, there are also options to go to profile page, groups page, and logout
   
4. The "Groups" link on the profile page will render another page to show all of the groups that the user is in -- can click on group name and learn more about the group or return to profile page

4a. Clicking on a group name will take the user to a page that shows the group name, description, and all of the users in the group -- options to join/delete/edit group or go to a page that displays all groups in the application
4b. The all Groups page explains the purpose of the groups, lists all of the groups in the application, and provides the option to start a group
4c. Clicking on "start a group" will render a form to create a new group in the application -- can fill out the form successfully and be taken back to the all groups page to see the group added to the list or just cancel and return to the all groups page

5. The "Following" link on the profile page will render another page to show all of the users that the logged in user is following -- can click on users and view their profiles (or click follow/unfollow to specific users) or return to profile page

6. The "Followers" link on the profile page will render another page to show all of the users that the logged in user is followed by -- can click on users and view their profiles (or click follow/unfollow to specific users) or return to profile page

7. The "Account" link on the profile page will render another page to show all of the account details of the logged in user -- can edit or delete account from this page or return to the profile page

7a. If the user chooses to edit the account, users will be given a form to edit account information and then be taken back to account after edit is successful -- can also just cancel the edit request and return to account page

8. Journal is at the bottom of the profile page -- can view recorded journal entries as cards with all food and exercises (with calorie count) listed -- users can either navigate to record food or record exercise

8a. The "Record Food" button will render a page with a form to record a food and apply the accurate date -- upon successful completion of the form, will be taken back to the profile page to see the inclusion of this food in the journal section or can cancel food log and just return back to the profile page
8b. The "Record Exercise" button will render a page with a form to record an exercise and apply the accurate date -- upon successful completion of the form, will be taken back to the profile page to see the inclusion of this exercise in the journal section or can cancel exercise log and just return back to the profile page

9. "Logout" from the navbar will take the user back to the home page to either go to the "about" page or sign up/log in
