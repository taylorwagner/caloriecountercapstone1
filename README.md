# Calorie Counter
API: https://developer.nutritionix.com/

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
