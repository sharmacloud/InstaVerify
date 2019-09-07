#Author: Piyush Sharma
#Date: August 30, 2019
#Version 1

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains




class InstaBot:

    def __init__(self, profile_url, writ, username, driver_path):


        try:
            self.profile_url = profile_url
            self.writ = writ
            self.username = username
            self.driver = webdriver.Chrome(driver_path)
        except:
            print("[+]Error: Please check your parameters")


        print("Instagram Bot v1 by SharmaCloud\n")
        self.url = 'https://www.instagram.com/accounts/login/'

        self.action = ActionChains(self.driver)

        #These lists store the usernames
        self.followers = []
        self.following = []


    def login(self):
        self.driver.get('https://www.instagram.com/accounts/login/')

        #WARNING: DO NOT CHANGE THESE
        user_path = 'username'
        pass_path = 'password'

        print("[+] Fetching username and password fields...\n")
        usr = self.driver.find_element_by_name(user_path)
        pas = self.driver.find_element_by_name(pass_path)

        print("[+] Sending User Info to site...\n")
        usr.send_keys(self.username)
        time.sleep(3)
        pas.send_keys(self.writ)
        time.sleep(3)
        pas.send_keys(Keys.ENTER)
        print("[+] Login Successful\n")


        time.sleep(3)

        not_now_path = '/html/body/div[3]/div/div/div[3]/button[2]'
        not_now_btn = self.driver.find_element_by_class_name("HoLwm")

        #Login with provided credentials
        not_now_btn.click()


    def get_followers(self):
        time.sleep(1)

        print("[+] Proceeding to get followers list")
        self.driver.get(self.profile_url)
        follower_btn_path = '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a '
        followers_btn= self.driver.find_element_by_xpath(follower_btn_path)
        print(followers_btn.text)
        followers_btn.click()
        time.sleep(3)


        followersList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))

        followersList.click()
        actionChain = webdriver.ActionChains(self.driver)

        while (numberOfFollowersInList < 60):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()

            # print(numberOfFollowersInList)
            numberOfFollowersInList+=1


        follower_link = followersList.find_elements_by_css_selector('a')



        for f in follower_link:
                #This solves the empty string issue from earlier
                if not f.text == '':
                    self.followers.append(f.text)

        print(len(self.followers))
        print(self.followers)


    def get_following(self):

        time.sleep(1)
        print("\n[+] Proceeding to get following list\n")
        self.driver.get(self.profile_url)
        following_btn_path = '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a '
        following_btn = self.driver.find_element_by_xpath(following_btn_path)
        following_btn.click()

        time.sleep(2)
        following_list = self.driver.find_element_by_css_selector('div[role=\"dialog\"] ul')

        numberOfFollowersInList = len(following_list.find_elements_by_css_selector('li'))

        time.sleep(2)
        following_list.click()
        actionChain = webdriver.ActionChains(self.driver)

        while (numberOfFollowersInList < 60):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()

            numberOfFollowersInList+=1

        time.sleep(1)

        following_link = following_list.find_elements_by_css_selector('a')

        for f in following_link:
            if not f == '':
                self.following.append(f.text)

    def get_following_file(self):

        following_file = 'following.txt'
        with open(following_file,'w') as f:
            for following in self.following:
                f.write(following+'\n')

            f.close()

    def get_followers_file(self):
        #followers file name is arbitrary and can be changed accordingly

        followers_file = 'followers.txt'
        #w mode provides the advantage of automatically creating the file if non-existent
        with open(followers_file,'w') as f:
            #write all usernames to the followers file

            for follower in self.followers:
                f.write(follower+'\n')

            #saving resources
            f.close()

    def not_a_follower(self):

        not_followers = []

        for following in self.following:

            if following not in self.followers:
                not_followers.append(following)

        print('[+] Following users are not following you:\n')
        print(set(not_followers))

    def not_following(self):
        not_following = []
        for follower in self.followers:
            if follower not in self.following:
                not_following.append(follower)
        print('[+] You are not following these users: \n')
        print(not_following)

    def main(self):
        #Call the following functions according to your requirements
        self.login()
        self.get_followers()
        self.get_followers_file()
        self.get_followers()
        self.get_following()
        self.get_following_file()
        self.not_a_follower()
        self.not_following()



inst = InstaBot()
inst.main()
