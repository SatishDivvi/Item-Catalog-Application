# Item Catalog Application

### Introduction:

Item Catalog Application is a Flask powered application which gives below information:
   1. Different Categories
   2. Items associated to each category
   3. Ability to add, delete, and modify **Categories** and it's **items**.
   3. Authentication and Authorization
   4. Local File Permission System
   5. API endpoints

### Installation

1. Install Vagrant and VirtualBox:
    - Install [Vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
    - Please fork the repository [VM Configuration](https://github.com/SatishDivvi/fullstack-nanodegree-vm) or download **Vagrantfile** from the repository.
    - Open terminal in *Mac* or *Linux* or GitBash in *Windows*. 

    **Note (Windows User only):** _please install [GitBash](https://git-scm.com/downloads) if not installed._

2. Configure Vagrant:
    - Open *GitBash* and `cd` to the directory where you have installed Vagrant.
    - Run command `vagrant up`. **Note:** _This step will take some time if executed for the first time._
    - Run command `vagrant ssh`
    - `cd` to folder _vagrant_ with command `cd /vagrant/catalog`.
3. How to setup Item Catalog Application:
    - Download folders `static`, `templates` and files `add_categories_and_items.py`, `database_setup.py`, `application.py`.
    - Place the downloaded folders and files into `vagrant/catalog` folder. 

    **Note:** _The folders and files structure should be same as seen in this repository._

### OAuth Setup - Google

This section is mandatory for Google+ Signin in order to restrict unauthorized users from adding, deleting or modifying restaurants and their menus. This also provides authentication making users mandatory to sign in for admin privileges:

1. Create Client ID and Client Secret:
    - Go to [Google Console](https://console.developers.google.com/apis)
    - Choose **Credentials** from the menu on the left.
    - Create an **OAuth Client ID**.
    - Click on **Configure Consent Screen**.
    - Give a valid name to the application.
    - Add appropriate javascript origins. For this project it should be `http://localhost:5000` or `http://127.0.0.1:5000`.
    - Add appropriate javascript redirects. For this project it should be `http://localhost:5000/login` and `http://localhost:5000/gconnect`.
    - After the consent screen please select **Web application** as the Application Type.
    - Click on the name of the app and **Client ID**, **Client Secret** can be viewed.
    - Download JSON file by clicking on **DOWNLOAD JSON** button and name the file as **client_secrets.json**.
    - Move **client_secrets.json** file to `/vagrant` folder.

    **Note:** *`client_secrets.json` file in this repository is only for you to check on how your json file should look. Please do not use this file as i have removed my `CLIENT_ID` and `CLIENT_SECRET`.*

### Oauth Setup - Facebook

This section is mandatory for Facebook Signin in order to restrict unauthorized users from adding, deleting or modifying restaurants and their menus. This also provides authentication making users mandatory to sign in for admin privileges:

1. Create App ID and App Secret:
    - Go to [Facebook Developers](https://developers.facebook.com/)
    - Sign in using your facebook account. **Note:** _If you don't have facebook account, you can create one at [Facebook Signup](https://www.facebook.com/)_
    - Click on **Add New App**.
    - Give App a name and click on **Create App ID**.
    - Go to `Settings\Basic`.
    - Go to **Add Platform** Section and select the app type as **website**.
    - Enter the site URL as `http://localhost:5000` and click on **Save Changes**.
    - Click on the `App Name` Dropdown on the top left pane.
    - Create Test App by clicking on **Creat Test App**. **Note:** _This step is mandatory as Facebook stopped supporting http protocol and only test apps support http protocol_
    - Your **App ID** and **App Secret** are created and can be viewed now. Create `fb_client_secrets.json` file or use the file available for reference in this repository and replace with your **App ID** and **App Secret**.
    
    Below are couple of resources i am sharing for your references:
    1. [loginbutton](https://developers.facebook.com/docs/facebook-login/web/#loginbutton)
    2. [redirecturl](https://developers.facebook.com/docs/facebook-login/web/#redirecturl)
    3. [loginsettings](https://developers.facebook.com/apps/408172529765462/fb-login/settings/)
    4. [accesstokens](https://developers.facebook.com/docs/facebook-login/web/accesstokens)
    5. [permissions](https://developers.facebook.com/docs/facebook-login/web/permissions)

### Project Execution:

 - Setup Database and feed data into the database:
    - Execute below commands in the same order and wait for each command to complete execution:

        ```python
        python database_setup.py
        python add_categories_and_items.py
        ```
    
    **Note:** _You can add more categories and items in `add_categories_and_items.py` file._

- Execute command `python application.py` and with this server is now running at **localhost 5000**.
- Open your favorite browser and enter `http://localhost:5000` or `http://localhost:127.0.0.1:5000`
- **Item Catalog Application** is now live.

    **Note:** _Currently host has been configured as `0.0.0.0` in `application.py` which means the server will be able to reach to all ipv4 addresses in your local machine._

### Screenshots:

1. Login/Registration
![Login](/images/Item-Catalog-login-Page.PNG)

2. Public Home Page
![PublicHomePage](/images/Item-Catalog-Home-Page-Non-Login.PNG)

3. Public Items page
![PublicItemsPage](/images/Item-Catalog-Items-Page-Non-Login.PNG)

4. Authenticated Home Page
![AuthenticatedHomePage](/images/Item-Catalog-Home-Page-Logged-In.PNG)

5. Authenticated Items Page
![AuthenticatedItemsPage](/images/Item-Catalog-Items-Page-Logged-In.PNG)

6. Add New Category Page
![NewCategory](/images/Add-New-Category.PNG)

7. Edit Categary Page
![EditCategory](/images/Edit-Category.PNG)

8. Delete Category Page
![DeleteCategory](/images/Delete-Category.PNG)

9. Add New Item Page
![NewItem](/images/Add-New-Item.PNG)

10. Edit Item Page
![EditItem](/images/Edit-Item.PNG)

11. Delete Item Page
![DeleteItem](/images/Delete-Item.PNG)

12. Logout
![Logout](/images/successful-disconnect.PNG)

13. Specific Category Item API Endpoint
![APIEndpoint](/images/Specific-Item-JSON-API-Endpoint.PNG)

### Author

Divvi Naga Venkata Satish - [Portfolio](https://satishdivvi.github.io)