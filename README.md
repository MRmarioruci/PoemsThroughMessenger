# PoemsThroughMessenger
This is a script that uses Selenium to automate the process of sending a message to a recipient on Facebook's Messenger. The recipient's profile is searched for based on a URL and the message is sent using the Facebook Messenger web interface. Additionally, the script makes use of the Poems class to retrieve a random poem from the poetrydb API and use it as the message to send. The script is headless, meaning that it runs in the background without the need for a visible browser window(You can disable the headless option by commenting out options.add_argument('--headless')).


# Install the required packages listed in requirements.txt
$ sudo pip3 install -r requirements.txt
# Open main.py and edit 
  RECIPIENT
  USERNAME
  PASSWORD
  RECIPIENT_URL

# Run the application
$ python3 main.py
