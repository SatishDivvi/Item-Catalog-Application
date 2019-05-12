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

### Screenshots:

### Author