Inventory POS Django Application

Overview
This application is developed in Django, and is a complete system to handle the inventory of a company oprating on Logistics. The Problem Statement is attached in problemStatement.txt

Installation
    1. Clone the Directory from Github
    2. Its basic dependency is python 2.7 and pip
        1. sudo apt-get install python-pip (install python also if not present)
    3. Install the Dependencies from requirements.txt
        1. sudo pip install -r requirements.txt
    4. run the django server
        1. python manage.py runserver
    5. Go to the browser, login and enjoy the funcitonality
        1. https://127.0.0.1:8000/inventory/login

Functionality
There are 3 basic tables used in this project (as specified in the problem). Their models have been defined in the ‘models.py’ file in the inventory app.  The functionality by urls are as follows:
API Endpoint
Functionality
/inventory/allItems
Lists all the Items present in the Database. You can do the following operations:
    1. Add Another item
    2. Edit an Existing Item
    3. Delete an Item
    4. View an item in detail 
        1. Click on the Item Row
/inventory/item/{item_id}
You can reach by clicking on an item row. This page basically displays item Details and all Variants associated with this item. You can:
    1. Add Another variant
    2. Edit and Existing Variant
    3. Delete a Variant
    4. View the Variant in Detail
        1. Click  anywhere on the Variant Row
/inventory/item/{item_id}/{variant_id/
This Page displays all feature associated with item and this variant. Also displayed are all the properties associated with this variant. You can:
    1. Delete a Property
    2. Edit an Existing Property
    3. Add Another Property to the Variant
/inventory/report/?user_id=1,2,3,4&startTime=2018-09-27T07:56:57&endTime=2018-09-27T010:10:57
This API call renders a page with all Logs associated with the users, within the given time range, in a table grouped by each user.
/Inventory/login
For Logging the User in
/inventory/logout
For Logging the User Out


Logs
/inventory/report/?user_id=1,2,3,4&startTime=2018-09-27T07:56:57&endTime=2018-09-27T010:10:57

This Endpoint is used to generate Logs for the operations. All of the supported user operations generate detailed logs, which are stored along with time and user, in the ‘InventoryLogs’ Table. These Logs are quite deatiled and specific to the operation being performed. For eg:
    1. Modifying a Variant
       Sept. 27, 2018, 9:36 a.m. Modified ['SellingPrice', 'Quantity'] of Variant:(4-Check Shirt) of the Item:(1-T-Shirt)
       Explanation: A User modified ‘SellingPrice’ and ‘Quantity’ of the Variant (Check Shirt with id 4) of the Item(T-Shirt with id 1) at the given time.
    2. Adding a property
       Sept. 27, 2018, 8:57 a.m. Added Property:(12-Size) of the Variant:(4-Check Shirt)
       Explanation: A User added this property(Property-Id, Property-Name) to the Variant(Id, Name).
A Sample Log of all user operations are already present in sqlite database, and can be accessed by ‘/inventory/report’ endpoint.
The Parameters:
Parameter Name
Necessity
Value
Default(if not specified)
user_id
Non-Necessary
Comma-seperated user_ids (Integers)
default=all Users present in system
startTime
Non-Necessary
018-09-27T07:56:57
Default=2000-09-27 10:44:00
endTime
Non-Necessary
2018-09-27T010:10:57
Default=datetime.datetime.now()

You can modify the API call in your browser to get different log feeds.
Usage

    1. Create your own user
        1. python manage.py createsuperuser
    2. Login in to system with your new credentails
    3. Do all the operations sepcified above
    4. Go to the reports section on the navbar.

Features
    1. The projects’ frontend has been implemented with the help of Bootstrap and Jquery, hence has a passable UI. (The aim is to demnstrate the APIs)
    2. All of the Endpoints require the user to login first, to prevent unuthorised access. Hence you need to create a user and login.
    3. The Default superuser is:
        1. username: apoorva
        2. password: apoorva123
