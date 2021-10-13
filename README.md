# btc_pub
This is the repository with the implementation of both the WebApp and MailSender, which has been dockerized as btc_pub image.
The container has been uploaded in a private docker repo, please refer to : mithatsinan.ergen@studenti.unitn.it to access it. 
This part of the project is split int two different parts: 

### For the web application  :
- `app.py` : 
  - it contains the API written in Python with Flask to build the WebApp available at [https://bdt2021.azurewebsites.net/](https://bdt2021.azurewebsites.net/), as well as its entry and end points.
  - it queries emails from subscribers from the Web Application itself 
  - if there is an unsubscription, it checks whether the email is present in the DB. If it is, it successfully deletes it, otherwise it sends and error. 
- `redisOperations.py` : 
  - contains the principal functions used to retrieve the last predictions from Redis, or to delete them in App.py
- `Templates` contains a separate html file for the WebApp:
  - `index.html` : a table with the last ten predictions, a separate widget available at [https://www.tradingview.com/widget/advanced-chart/](https://www.tradingview.com/widget/advanced-chart/), and a box to subscribe
- `Static`: main folder defining the webpage responsive layout and its logo.
  - `CSS`: 
    -  `main.css`: webpage layout, introduction of a repsponsive layout. 
   - `bitcoin-btc-logo` and `favicon.ico` : resizing layout elements, website logo. 
### Email Sender : 
- `MailSender`: Azure function folder for both reading redis' last insertions and updating the webapp, and sending mails daily.
  - `__init__.py`: Azure function definition, triggered daily at UTC midnight. It contains the entry and end point of the DB and connects to select the emails. Reading last 24 predictions from redis and sending them to each email address in the subscription list.
    Runs <b> automatically </b>. 
   - `function.json`: function time trigger 
   - `redisOperations.py` : contains the principal functions used on Redis, namely get the last n predictions, key-values, or delete key.
   
### How to start
Access via VisualStudio by downloading the necessary extentions for Microsoft Azure, available [here](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) and run this repo locally on your machine.

#### - Once in Visual Studio :
Run `pip install -r requirements.txt`, if an older version of pip is used, please consider running `pip install --upgrade pip` first (if any issues are encountered, please run the same command as: `pip install --upgrade pip --user`. 
Next, the process is the following.
  1. Azure functions are attached to two relevant files:
    1. `__init__.py` is the main file taken into account. Thus, if run, the function is run locally. 
    2. `function.json` is the main configuration of the function 
   Go to the Azure extension and check for the local project.Then, run the `__init__.py` locally for MailSender. Please note, that doing so is going to update both the WebApp and  send emails to all subscribers, while eventually blocking the process. The best idea to access this project is listed below. 
2. Go to the WebApp and enroll to the Mailing system, attend confirmation and wait for your Midnight Mail :). Being a live system, the main access is from the output itself. Refresh the page hourly, you might get lucky !  
3. Try to unsubscribe and refresh the page, and check the success and error signal. 
 

For further questions please contact: annamaria.fetz@studenti.unitn.it  or mithatsinan.ergen@studenti.unitn.it
