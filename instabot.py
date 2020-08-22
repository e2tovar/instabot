from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import random

class Botsito():
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
        self.browserProfile.add_argument("--incognito")

        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome('chromedriver.exe', chrome_options=self.browserProfile)
        self.browser.implicitly_wait(5)
        self.browser.get('https://www.instagram.com/accounts/login/')
        
        #sign
        self.user = user
        self.password = password
        self.signIn()
        self.browser.get('https://www.instagram.com/' + self.user)

    def signIn(self):
        """This function signs into an account on instagram"""          
        

        # check if there is another acouunt previusly created, 
        # becouse instagram login page get the option to enter directly with that account
        # and we dont want that
        continueButton = self.browser.find_element_by_css_selector('button')
        if (continueButton.text != 'Login'):
            print(continueButton.text)
            #Click on otra cuenta
            time.sleep(random.randint(2,4))
        
        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.user)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(random.randint(2,4))
    
    def followWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(random.randint(2,4))
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text == 'Follow'):
            followButton.click()
            time.sleep(random.randint(2,4))
        else:
            print("You are already following this user")
    
    def unfollowWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(random.randint(2,4))
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text == 'Unfollow'):
            followButton.click()
            time.sleep(random.randint(2,4))
        else:
            print("You are not following this user")
    

class Instaengagement(Botsito):
    """Defines an Instabot children for engagement, 
    needs a list

    """
    def __init__(self, user, password, engagefile="posts_list"):        
        #other attributes
        self.egagefile = engagefile
        # Invoque constructor
        Botsito.__init__(self, user, password)
    
    def autoengage(self, send=None):
        """This function is do the dinamic in the engadment group

        Keyword Arguments:
            send {string} -- instagram account to send the post (default: {None})
        """        
        count = 1
        link_list = self.get_list()
        posts_liked = {}

        #start dinamic
        for link in link_list:
            #print("test "+link) --- debug
            self.browser.get(link)
            time.sleep(random.randint(2,4))

            #increase count
            print(str(count) + "----" + link)
            count += 1
           
            #chek if is an account or a post, if not click on a post
            if '/p/' not in link:
                #Verify if a post exists
                post = self.browser.find_elements_by_css_selector('._9AhH0')
                #Check if there is a post.
                if len(post) == 0:
                    print(str(count) + "----" + link + "----Error no Posts----")
                    count +=1
                    continue
                else: 
                    post[0].click()
                    posts_liked[str(count) + "--" + link] = self.browser.current_url
                    time.sleep(random.randint(2,4))

            #find heart and like
            try:
                heart = self.browser.find_elements_by_xpath("//section/span/button/div/span[*[local-name()='svg']/@aria-label='Like']")
                if len(heart) > 0:
                    heart[0].click() 
                    status = 'Done'                                               
                else:
                    status = 'It Was Liked before'
                #status print
                print('like --> ', status)
                time.sleep(random.randint(2,4))
            except:
                print("There was a problem while liking")
            
            #find save and save
            try:              
                check_save = self.browser.find_elements_by_xpath("//section/span/div/div/button/div[*[local-name()='svg']/@aria-label='Save']")
                if len(check_save) > 0 :
                    save = self.browser.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[3]/div/div/button')
                    save.click()
                    status = 'Done'
                    time.sleep(random.randint(2,4))
                else:
                    status = 'It Was Saved before'
                #status print
                print('save --> ', status)
            except:
                print("There was a problem saving")

            #send
            if send:
                self.sendto(send)
                print('send --> Done')
                time.sleep(random.randint(3,5))
            
            
            #save post to txt
            self.liked_posts(lista = posts_liked)
        print('__________________FIN________________________')
        print("He interactuado con {} publicaciones".format(count))
        self.save_liked_posts(lista = posts_liked)
    
    
    def get_list(self, file='posts_list.txt'):
        link_list = []
        with open(file, errors='ignore') as f:
            text = f.read()
            href_regex = r"[Ii]nstagram\.com\S*"
            links = re.findall(href_regex, text)
            
            for line in links:
                # add http
                url = "https://www." + line
                link_list.append(url.rstrip())
        return link_list

    def sendto(self, account):
        #find share button and click
        share = self.browser.find_element_by_css_selector('._8-yf5[aria-label="Share Post"]')
        share.click()
        time.sleep(random.randint(2,4))
        #find direct message
        direct = self.browser.find_elements_by_xpath("//*[contains(text(), 'Share to Direct')]")
        direct[0].click()
        time.sleep(random.randint(2,4))
        #find input and se account name
        inp = self.browser.find_element_by_css_selector('input[name="queryBox"]')
        inp.send_keys(account)
        time.sleep(random.randint(2,4))
        #find destiny account
        dest = self.browser.find_element_by_css_selector('._7UhW9.xLCgt.qyrsm.KV-D4.uL8Hv')
        dest.click()
        #find send_button
        send_b = self.browser.find_element_by_css_selector('.sqdOP.yWX7d.y3zKF.cB_4K')
        send_b.click()

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