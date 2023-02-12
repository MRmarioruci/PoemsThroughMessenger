import random
from datetime import datetime
import selenium as sel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import requests

options = Options()
options.add_argument('--headless')


class MessengerHandler:
    def __init__(self, username, password, recipient, message) -> None:
        self.username = username
        self.password = password
        self.message = message
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.recipient = recipient

    def start(self):
        self.driver.maximize_window()
        self.driver.minimize_window()
        self.driver.maximize_window()
        self.driver.switch_to.window(self.driver.current_window_handle)
        self.driver.implicitly_wait(10)

        # Enter to the site
        self.driver.get('https://www.messenger.com/login/');
        self.driver.implicitly_wait(2)
        self.acceptCookies()

    def acceptCookies(self):
        # Accept cookies
        self.driver.find_element('xpath', "/html/body/div[2]/div[2]/div/div/div/div/div[3]/button[2]").click()
        print('Opened page...')
        self.fillCredentials()

    def fillCredentials(self):
        # User Credentials
        self.driver.find_element('xpath', '//*[@id="email"]').send_keys(self.username)
        self.driver.find_element('xpath', '//*[@id="pass"]').send_keys(self.password)
        print('Filled inputs')
        self.driver.implicitly_wait(1)
        # Login button
        self.driver.find_element('xpath', '//*[@id="loginbutton"]').click()
        print('Clicked submit')
        self.driver.implicitly_wait(20)
        self.waitLoadAndFindUser()

    def waitLoadAndFindUser(self):
        chat_block = self.driver.find_element('xpath', '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div/div/div/div/div[3]/div/div/div')
        if chat_block:
            print('Found chat block')
            chat_items = chat_block.find_elements(By.TAG_NAME,'a')
            for chat in chat_items:
                print(str(chat.get_attribute('href')))
                if str(chat.get_attribute('href')) == self.recipient:
                    print('Found user')
                    chat.click()
                    self.driver.implicitly_wait(6)
                    self.sendMessage()
                    break
        else:
            print('Could not find the chat sidebar.')

    def sendMessage(self):
        chat_input = self.driver.find_element('xpath', '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div[1]/div/div/div[1]/div[2]/div/div/div[2]/div/div/div[4]/div[2]/div/div/div/p')
        if chat_input:
            print('Found chat input')
            chat_input.send_keys(self.message)
            self.driver.implicitly_wait(1)
            submit = self.driver.find_element('xpath', '/html/body/div[1]/div/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div/span[2]/div')
            if submit:
                print('Submitting')
                submit.click()
            else:
                print('Did not find submit element')

class Poems:
    def __init__(self, recipient) -> None:
        self.authors = ['Ernest Dowson', 'Percy Bysshe Shelley', 'Alan Seeger', 'Adam Lindsay Gordon']
        self.recipient = recipient
        self.poems = requests.get(f'https://poetrydb.org/author/{self.authors[random.randint(0, len(self.authors)-1)]}').json()

    def getPoemMessage(self):
        randomPoem = self.poems[random.randint(0, len(self.poems)-1)]
        fullMessage = f"Hey {self.recipient}... i wanted to tell you that i love you today at: {datetime.today().strftime('%Y-%m-%d %H:%M:%S')} with the following poem: \n\n"
        lines = randomPoem['lines']
        for line in lines:
            fullMessage += f"{line}\n"

        return fullMessage


if __name__ == '__main__':
    #Edit these variables in order to customize to your needs
    RECIPIENT = '' #The name of your loved one. Whatever you want to call them it doesn't have to align with their Messenger name.
    USERNAME = '' # Your Messenger username/email
    PASSWORD = '' # Your Messenger password
    RECIPIENT_URL = '' # Open messenger, click on the recipient and get the url. E.g: https://www.messenger.com/t/100003227365235/

    if not RECIPIENT or not USERNAME or not PASSWORD or not RECIPIENT_URL:
        print('Please provide me with the credentials...')
        quit()

    poems = Poems(RECIPIENT)
    message = poems.getPoemMessage()
    messenger = MessengerHandler(USERNAME, PASSWORD, RECIPIENT_URL, message)
    messenger.start()
