from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import numpy as np

class InstaBot():
    """This class creates a bot for istagram
    """    
    def __init__(self, user, password):
        """Init method of the class

        Arguments:
            user {string} -- [your instagram user]
            password {string} -- [your instagram password]
        """
        #set browser to english language
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)
        #other attributes
        self.user = user
        self.password = password
        self.signIn()
        

    def signIn(self):
        """This function signs into an account on instagram"""   
        
        self.browser.get('https://www.instagram.com/accounts/login/')

        # check if there is another acouunt previusly created, 
        # becouse instagram login page get the option to enter directly with that account
        # and we dont want that
        continueButton = self.browser.find_element_by_css_selector('button')
        if (continueButton.text != 'Login'):
            print(continueButton.text)
            #Click on otra cuenta
            time.sleep(2)
        
        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.user)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)
    
    def followWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text == 'Follow'):
            followButton.click()
            time.sleep(2)
        else:
            print("You are already following this user")
    
    def hashtagCount(self, hashtag):
        """This function search for a hashtag
         and count how many posts are in

        Arguments:
            hashtag {string} -- '#' + hashtag

        Returns:
            [string] -- hashtag count
        """
        self.browser.get('https://www.instagram.com/explore/tags/' + hashtag[1:] + '/') 
        time.sleep(2)
        hastag_count = self.browser.find_element_by_css_selector('.g47SY')
        return hastag_count.text
    

class Instaengagement(InstaBot):
    """Defines an Instabot children for engagement, 
    needs a list

    """
    def __init__(self, user, password, engagefile="posts_list"):        
        #other attributes
        self.egagefile = engagefile
        # Invoque constructor
        InstaBot.__init__(self, user, password)
    
    def flash(self, send=None):
        """This function is do the dinamic in the engadment group

        Keyword Arguments:
            send {string} -- instagram account to send the post (default: {None})
        """        
        count = 1
        link_list = self.get_list()
        posts_liked = {}

        #start dinamic
        for link in link_list:
            self.browser.get(link)
            time.sleep(2)
           
            #chek if is an account or a post, if not click on a post
            if '/p/' not in link:
                #Verify if a post exists
                post = self.browser.find_elements_by_css_selector('._9AhH0')
                if len(post) < 3: 
                    if len(post) == 0:
                        print(str(count) + "----" + link + "----Errorrrrrr----")
                        count +=1
                        continue
                    else: #if there is just one or two posts
                        post[0].click()
                        posts_liked[str(count) + "--" + link] = self.browser.current_url
                        time.sleep(2)
                else:
                    #postn = np.random.randint(0,2)
                    post[0].click()
                    posts_liked[str(count) + "--" + link] = self.browser.current_url
                    time.sleep(2)

            #find heart and like
            try:
                heart = self.browser.find_element_by_css_selector('._8-yf5[aria-label="Like"]')
                heart.click()
            except:
                print("already liked")
        
            #find save and save
            try:
                save = self.browser.find_element_by_css_selector('._8-yf5[aria-label="Save"]')
                save.click()
            except:
                print("already save")

            #send
            if send:
                self.sendto(send)
            
            #increase count
            print(str(count) + "----" + link)
            count += 1
            #save post
            self.liked_posts(lista = posts_liked)
        print('__________________FIN________________________')
        print("He interactuado con {} publicaciones".format(count))
        save_liked_posts(lista = posts_liked)
    
    
    def get_list(self, file='posts_list.txt'):
        link_list = []
        with open(file) as f:
            text = f.read()
            href_regex = "[Ii]nstagram\.com\S*"
            links = re.findall(href_regex, text)
            
            for i, line in enumerate(links):
                # add http
                url = "https://www." + line
                link_list.append(url.rstrip())
                #print(str(i)+" "+url)
        return link_list

    def save_liked_posts(self, lista):
        print(lista)
        with open("liked.txt","w+") as file:
            file.truncate(0)
            for page, p in lista.items():
                file.write(page + "--" + p + "\n")

    def liked_posts(self, lista):
        with open("temp_liked.txt","w+") as file:
            for page, p in lista.items():
                file.write(page + "--" + p + "\n")
    
    def sendto(self, account):
        #find send and send to someone
        share = self.browser.find_element_by_css_selector('._8-yf5[aria-label="Share Post"]')
        share.click()
        time.sleep(2)
        #find direct
        direct = self.browser.find_elements_by_xpath("//*[contains(text(), 'Share to Direct')]")
        direct[0].click()
        time.sleep(2)
        #find input
        inp = self.browser.find_element_by_css_selector('input[name="queryBox"]')
        inp.send_keys(account)
        time.sleep(2)
        #find destinity
        dest = self.browser.find_element_by_css_selector('._7UhW9.xLCgt.qyrsm.KV-D4.uL8Hv')
        dest.click()
        #find send_button
        send_b = self.browser.find_element_by_css_selector('.sqdOP.yWX7d.y3zKF.cB_4K')
        send_b.click()

    
    
