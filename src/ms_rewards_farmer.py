import time
import json
from datetime import date, timedelta, datetime
import random
import schedule
import os
import sys
from logs.Logger import *
from Utilities import *
from tasks.Searches import Searches
from tasks.DailySets import DailySets
from tasks.Promotions import Promotions
from tasks.PunchCards import PunchCards
import settings

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

from HookLoader import *

# Define user-agents
DEFAULT_PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44'
DEFAULT_MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 12; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'

STREAK_DATA = 0
MAX_JOB_ATTEMPTS = 5
MAX_ACCOUNT_ATTEMPTS = 3
MAX_INTERNET_ATTEMPTS = 10

# Define login function
def login(browser: WebDriver, email: str, pwd: str, isMobile: bool = False):
    # Access to bing.com
    browser.get('https://login.live.com/')
    try:
        # Wait complete loading
        Utilities.waitUntilVisible(browser, By.ID, 'loginHeader', 10)
        # Enter email
        settings.logger.log('[LOGIN]', 'Writing email...')
        Utilities.waitForElement(browser, By.NAME, "loginfmt").send_keys(email)
        # Click next
        Utilities.waitForElement(browser, By.ID, 'idSIButton9').click()
        # Wait 2 seconds
        time.sleep(2)
        # Wait complete loading
        Utilities.waitUntilVisible(browser, By.ID, 'loginHeader', 10)
        # Enter password
        browser.execute_script("document.getElementById('i0118').value = '" + pwd + "';")
        settings.logger.log('[LOGIN]', 'Writing password...')
        # Click next
        Utilities.waitForElement(browser, By.ID, 'idSIButton9').click()
    except (TimeoutException) as e:
        raise Exception('Timeout while login')

    # Wait 5 seconds
    time.sleep(5)
    # Click Security Check
    settings.logger.log('[LOGIN]', 'Passing security checks...')
    try:
        browser.find_element(By.ID, 'iLandingViewAction').click()
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    # Wait complete loading
    try:
        Utilities.waitUntilVisible(browser, By.ID, 'KmsiCheckboxField', 10)
    except (TimeoutException) as e:
        pass
    # Click next
    try:
        browser.find_element(By.ID, 'idSIButton9').click()
        # Wait 5 seconds
        time.sleep(5)
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    settings.logger.log('[LOGIN]', 'Logged-in !')
    # Check Login
    settings.logger.log('[LOGIN]', 'Ensuring login on Bing...')
    checkBingLogin(browser, isMobile)

def checkBingLogin(browser: WebDriver, isMobile: bool = False):
    #Access Bing.com
    browser.get('https://bing.com/')
    # Wait 8 seconds
    time.sleep(8)
    #Accept Cookies
    try:
        Utilities.waitForElement(browser, By.ID, 'bnp_btn_accept').click()
    except:
        pass
    try:
        script = 'document.getElementById("bnp_ttc_div").style.display = "none"'
        browser.execute_script(script)
    except:
        pass
    try:
        script = 'document.getElementById("bnp_rich_div").style.display = "none"'
        browser.execute_script(script)
    except:
        pass
    try:
        Utilities.waitForElement(browser, By.ID, 'bnp_close_link').click()
    except:
        pass
    if isMobile:
        try:
            time.sleep(1)
            Utilities.waitForElement(browser, By.ID, 'mHamburger').click()
        except:
            try:
                Utilities.waitForElement(browser, By.ID, 'bnp_btn_accept').click()
            except:
                pass
            time.sleep(1)
            try:
                Utilities.waitForElement(browser, By.ID, 'mHamburger').click()
            except:
                pass
        try:
            time.sleep(1)
            Utilities.waitForElement(browser, By.ID, 'HBSignIn').click()
        except:
            pass
        try:
            time.sleep(2)
            Utilities.waitForElement(browser, By.ID, 'iShowSkip').click()
            time.sleep(3)
        except:
            if str(browser.current_url).split('?')[0] == "https://account.live.com/proofs/Add":
                input('[LOGIN] Please complete the Security Check on ' + browser.current_url)
                exit()
    #Wait 2 seconds
    time.sleep(2)
    # Refresh page
    browser.get('https://bing.com/')
    # Wait 10 seconds
    time.sleep(10)
    #Update Counter
    try:
        if not isMobile:
            settings.pointsCounter = int(Utilities.waitForElement(browser, By.ID, 'id_rc').get_attribute('innerHTML'))
        else:
            try:
                Utilities.waitForElement(browser, By.ID, 'mHamburger').click()
            except:
                try:
                    browser.Utilities.waitForElement(browser, By.ID, 'bnp_btn_accept').click()
                except:
                    pass
                try:
                    script = 'document.getElementById("bnp_ttc_div").style.display = "none"'
                    browser.execute_script(script)
                except:
                    pass
                try:
                    script = 'document.getElementById("bnp_rich_div").style.display = "none"'
                    browser.execute_script(script)
                except:
                    pass
                try:
                    Utilities.waitForElement(browser, By.ID, 'bnp_close_link').click()
                except:
                    pass
                time.sleep(1)
                Utilities.waitForElement(browser, By.ID, 'mHamburger').click()
            time.sleep(1)
            settings.pointsCounter = int(Utilities.waitForElement(browser, By.ID, 'fly_id_rc').get_attribute('innerHTML'))
    except:
        raise ValueError('Login check failed: invalid credentials')

def schedule_next_run(pc_user_agent: str, mobile_user_agent: str): # set next run for random hour and minute each day
   time_str = '{:02d}:{:02d}'.format(random.randint(7, 10), random.randint(0, 59))
   schedule.clear()
   settings.logger.log('[SCHEDULE]', "Next run scheduled for tomorrow, {}, at {}".format((date.today() + timedelta(days=1)).strftime("%B %d"),time_str), LogColor.PURPLE)
   time.sleep(14400) #sleep so job will not happen twice in a day
   schedule.every().day.at(time_str).do(run, pc_user_agent=pc_user_agent, mobile_user_agent=mobile_user_agent)

def doAccount(account, pc_user_agent, mobile_user_agent):
    browser = Utilities.browserSetup(pc_user_agent, settings.config['languageCode'])
    settings.logger.log('[LOGIN]', 'Logging-in...')
    login(browser, account['username'], account['password'])
    settings.logger.log('[LOGIN]', 'Logged-in successfully!', LogColor.GREEN)
    startingPoints = settings.pointsCounter
    settings.logger.log('[POINTS]', 'You have ' + str(settings.pointsCounter) + ' points on your account!', LogColor.GREEN)
    STREAK_DATA = Utilities.getStreakData(browser)

    # Check if there's things to do.
    desktopJobAttempts = 1
    toComplete = Utilities.getActivitiesToComplete(browser)
    while bool(toComplete) and desktopJobAttempts <= MAX_JOB_ATTEMPTS:
        settings.logger.log('[INFO]', 'Desktop Attempt #' + str(desktopJobAttempts), LogColor.YELLOW)
        time.sleep(5)

        if 'dailySetPromotions' in toComplete:
            settings.logger.log('[DAILY SET]', 'Trying to complete the Daily Set...')
            try:
                DailySets.completeDailySet(browser)
                settings.logger.log('[DAILY SET]', 'Completed the Daily Set successfully!', LogColor.GREEN)
            except (Exception, SessionNotCreatedException) as err:
                settings.logger.log('[DAILY SET]',  'Did not complet Daily Set !', LogColor.RED)
                pass
        if 'punchCards' in toComplete:
            settings.logger.log('[PUNCH CARDS]', 'Trying to complete the Punch Cards...')
            try:
                PunchCards.completePunchCards(browser)
                settings.logger.log('[PUNCH CARDS]', 'Completed the Punch Cards successfully!', LogColor.GREEN)
            except (Exception, SessionNotCreatedException) as err:
                settings.logger.log('[PUNCH CARDS]',  'Did not complet Punch Cards !', LogColor.RED)
                settings.logger.log('[ERROR]', str(err), LogColor.RED)
                pass
        if 'morePromotions' in toComplete:
            settings.logger.log('[MORE PROMO]', 'Trying to complete More Promotions...')
            try:
                Promotions.completeMorePromotions(browser)
                settings.logger.log('[MORE PROMO]', 'Completed More Promotions successfully!', LogColor.GREEN)
            except (Exception, SessionNotCreatedException) as err:
                settings.logger.log('[MORE PROMO]', 'Did not complet More Promotions !', LogColor.RED)
                settings.logger.log('[ERROR]', str(err), LogColor.RED)
                pass
        if 'desktopSearch' in toComplete:
            settings.logger.log('[BING]', 'Starting Desktop and Edge Bing searches...')
            try:
                Searches.bingSearches(browser, toComplete['desktopSearch'], settings.config)
                settings.logger.log('[BING]', 'Finished Desktop and Edge Bing searches!', LogColor.GREEN)
            except (Exception, SessionNotCreatedException) as err:
                settings.logger.log('[BING]', 'Did not complet Desktop search !', LogColor.RED)
                settings.logger.log('[ERROR]', str(err), LogColor.RED)
                pass

        desktopJobAttempts += 1
        settings.logger.log('[INFO]', 'Checking if everything in desktop is done...', LogColor.YELLOW)
        toComplete = Utilities.getActivitiesToComplete(browser)
        browser.get('https://rewards.bing.com/')
        STREAK_DATA = Utilities.getStreakData(browser)
        time.sleep(30)

    browser.quit()
    browser = None
    browser = Utilities.browserSetup(mobile_user_agent, settings.config['languageCode'])
    settings.logger.log('[LOGIN]', 'Mobile logging-in...')
    login(browser, account['username'], account['password'], True)
    settings.logger.log('[LOGIN]', 'Mobile logged-in successfully !')
    remainingSearchesM = Utilities.getRemainingSearches(browser, True)
    mobileJobAttempts = 1
    while remainingSearchesM > 0 and mobileJobAttempts <= MAX_JOB_ATTEMPTS:
        time.sleep(5)
        settings.logger.log('[INFO]', 'Mobile Attempt #' + str(mobileJobAttempts), LogColor.YELLOW)
        if remainingSearchesM > 0:
            settings.logger.log('[BING]', 'Starting Mobile Bing searches...')
            Searches.bingSearches(browser, remainingSearchesM, settings.config, True)
            settings.logger.log('[BING]', 'Finished Mobile Bing searches!', LogColor.GREEN)
            remainingSearchesM = Utilities.getRemainingSearches(browser, True)
            mobileJobAttempts += 1

    browser.quit()
    account['completed'] = True
    settings.logger.log('[POINTS]', 'You have earned ' + str(settings.pointsCounter - startingPoints) + ' this run!', LogColor.GREEN)
    settings.logger.log('[POINTS]', 'You are now at ' + str(settings.pointsCounter) + ' points!', LogColor.GREEN)
    settings.logger.log('[STREAK]', STREAK_DATA.split(',')[0] + (' day.' if STREAK_DATA.split(',')[0] == '1' else ' days!') + STREAK_DATA.split(',')[2], LogColor.GREEN)
    for h in hooks.account_completed:
        h(account, startingPoints, STREAK_DATA, settings)  

def run(pc_user_agent: str, mobile_user_agent: str):
    settings.logger.log('[INIT]', 'MS FARMER by Thomas Lepage version 3.1.0', LogColor.RED)

    settings.logger.log('[INIT]', 'Checking internet connection...', LogColor.RED)
    internetTry = 1
    internetOK = False
    while internetTry <= MAX_INTERNET_ATTEMPTS:
        settings.logger.log('[INIT]', 'Trying internet attemps: ' + str(internetTry), LogColor.RED)
        internetOK = Utilities.internetAccess()
        if (internetOK):
            break
        internetTry += 1
        time.sleep(5*internetTry)

    if (internetOK):
        random.shuffle(settings.config["accounts"])
        for index, account in enumerate(settings.config["accounts"], start=1):
            account['completed'] = False
            attempts = 1
            settings.logger.log('[INFO]', '********************' + account['username'] + '********************', LogColor.YELLOW)
            while not account['completed'] and attempts <= MAX_ACCOUNT_ATTEMPTS:
                settings.logger.log('[INFO]', "Attempting account for #" + str(attempts) + " time", LogColor.YELLOW)
                try:
                    doAccount(account, pc_user_agent, mobile_user_agent)
                except (Exception, SessionNotCreatedException) as err:
                    for h in hooks.account_error:
                        h(account, err, settings)  
                    settings.logger.log('[ERROR]', str(err), LogColor.RED)
                    attempts += 1
                    pass

            if len(settings.config["accounts"]) > 1:
                if index < len(settings.config["accounts"]):
                    randomTime = random.randint(1200, 5400)
                    settings.logger.log('[SCHEDULE]', "Current time {}".format(datetime.now().strftime("%H:%M")), LogColor.RED)
                    time_str = (datetime.now() + timedelta(seconds=randomTime)).strftime("%H:%M")
                    settings.logger.log('[SCHEDULE]', "Next account run at {}".format(time_str), LogColor.RED)
                    time.sleep(randomTime)
    schedule_next_run(pc_user_agent, mobile_user_agent) #set a new hour and minute for the next day
    return schedule.CancelJob #cancel current time schedule

if __name__ == '__main__':
    hooks = discover_hooks(paths)
    settings.initialize()
    try:
        config_path = os.path.dirname(os.path.abspath(__file__)) + '/config.json'
        settings.config = json.load(open(config_path, "r"))
    except FileNotFoundError:
        settings.logger.log("[ACCOUNT]", 'Create "config.json" from "config.json.sample" and re-run the script.', LogColor.PURPLE)
        sys.exit(1)

    PC_USER_AGENT = settings.config["customEdgeUserAgent"]
    if not PC_USER_AGENT:
        PC_USER_AGENT = DEFAULT_PC_USER_AGENT
    MOBILE_USER_AGENT = settings.config["customMobileUserAgent"]
    if not MOBILE_USER_AGENT:
        MOBILE_USER_AGENT = DEFAULT_MOBILE_USER_AGENT

    schedule.every().day.at("00:00").do(run) #Start scheduling to be replaced by random ints after first run is over

    try:
        run(PC_USER_AGENT, MOBILE_USER_AGENT) #Run for First time and set schedule for the next run

        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        settings.logger.log('[INFO]', 'Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
