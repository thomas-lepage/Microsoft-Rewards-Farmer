import time
import json
import urllib.request
import requests
import os
from datetime import date, timedelta, datetime
from selenium.webdriver.support.ui import WebDriverWait
from logs.Logger import LogColor
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from simplejson import JSONDecodeError
from selenium.common.exceptions import *
import settings

# use ENV IS_RUNNING_IN_DOCKER=true in the Dockerfile
IS_RUNNING_IN_DOCKER = os.environ.get("IS_RUNNING_IN_DOCKER", "false").lower() == 'true'

class Utilities:
    # Define browser setup function
    def browserSetup(user_agent: str, lang: str) -> WebDriver:
        # Create Chrome browser
        options = Options()
        if IS_RUNNING_IN_DOCKER:
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument("--headless")
        options.add_argument("user-agent=" + user_agent)
        options.add_argument('lang=' + lang.split("-")[0])
        options.add_argument('log-level=3')
        if IS_RUNNING_IN_DOCKER:
            # Chrome Driver should be installed by the Dockerfile
            chrome_browser_obj = webdriver.Chrome(options=options)
        else:
            # for Desktops it's more practical to use ChromeDriverManager
            service = Service(ChromeDriverManager().install())
            chrome_browser_obj = webdriver.Chrome(service=service, options=options)
        return chrome_browser_obj
    
    def getDashboardData(browser: WebDriver) -> dict:
        dashboard = Utilities.findBetween(Utilities.waitForElement(browser, By.XPATH, '/html/body').get_attribute('innerHTML'), "var dashboard = ", ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
        try:
            dashboard = json.loads(dashboard)
        except (TimeoutException, JSONDecodeError) as err:
            try:
                browser.find_element(By.ID, "start-earning-rewards-link").click()
                time.sleep(5)
                dashboard = Utilities.findBetween(Utilities.waitForElement(browser, By.XPATH, '/html/body').get_attribute('innerHTML'), "var dashboard = ", ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
                dashboard = json.loads(dashboard)
            except (TimeoutException, JSONDecodeError, NoSuchElementException) as err:
                raise Exception('Error getting the dashboard', err)
        return dashboard

    def getStreakData(browser):
        browser.get('https://rewards.bing.com/')
        try:
            time.sleep(16)
            return browser.find_element(By.ID, 'streak').get_attribute('aria-label')
        except (Exception, NoSuchElementException) as err:
            settings.logger.log('[ERROR]', str(err), LogColor.RED)
            raise Exception('Error while getting the streak', err)
        
    def getActivitiesToComplete(browser: WebDriver) -> dict:
        browser.get('https://rewards.bing.com/')
        time.sleep(10)

        dashboard = Utilities.getDashboardData(browser)
        toComplete = {}

        #DAILYSETPROMOTIONS
        dailySet = dashboard['dailySetPromotions']
        todayDate = datetime.today().strftime('%m/%d/%Y')
        todayPack = []
        for date, data in dailySet.items():
            if date == todayDate:
                todayPack = data
        toComplete['dailySetPromotions'] = []
        for activity in todayPack:
            if activity['complete'] == False:
                toComplete['dailySetPromotions'].append(activity['offerId'])

        #PUNCHCARDS
        punchCards = dashboard['punchCards']
        toComplete['punchCards'] = []
        for promotion in punchCards:
            for childPromotion in promotion['childPromotions']:
                if childPromotion['complete'] == False and childPromotion['promotionType'] != 'appstore':
                    toComplete['punchCards'].append(childPromotion['offerId'] + ' Type: ' + childPromotion['promotionType'])

        #MOREPROMOTIONS
        morePromotions = dashboard['morePromotions']
        toComplete['morePromotions'] = []
        for promotion in morePromotions:
            if promotion['complete'] == False and promotion['promotionType'] != 'appstore' and promotion['offerId'] != 'ENCA_lifecycle_rewardsca_Got_to_Level_2' and promotion['offerId'] != 'ENCA_lifecycle_rewardsca_Onboarding_100_bonus_points':
                if promotion['pointProgressMax'] > 0 and promotion['pointProgress'] < promotion['pointProgressMax']:
                    if not 'ShopAndEarn' in promotion['offerId']:
                        toComplete['morePromotions'].append(promotion['offerId'] + ' Type: ' + promotion['promotionType'])
        
        #SEARCH
        remainingSearches, remainingSearchesM = Utilities.getRemainingSearches(browser)

        toComplete['desktopSearch'] = []
        toComplete['mobileSearch'] = []

        if remainingSearches != 0:
            toComplete['desktopSearch'] = remainingSearches

        toComplete = {k:v for k,v in toComplete.items() if v}
        return toComplete


    def internetAccess(host="https://google.com"):
        try:
            urllib.request.urlopen(host)
            return True
        except:
            return False
        
    def sendToIFTTT(message, iftttUrl):
        data = json.dumps({"value1": message}).encode()
        req = urllib.request.Request(iftttUrl)
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, data) as opened_req:
            result = opened_req.read().decode()
        settings.logger.log('[PUSH NOTIFICATIONS]', result, LogColor.GREEN)
    
    def waitForElement(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
        return WebDriverWait(browser, time_to_wait).until(ec.presence_of_element_located((by_, selector)))

    def waitUntilVisible(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
        WebDriverWait(browser, time_to_wait).until(ec.visibility_of_element_located((by_, selector)))

    def findBetween(s: str, first: str, last: str) -> str:
        try:
            start = s.index(first) + len(first)
            end = s.index(last, start)
            return s[start:end]
        except ValueError:
            return ""
        
    def getGoogleTrends(numberOfwords: int, lang: str, geo: str) -> list:
        search_terms = []
        i = 0
        while len(search_terms) < numberOfwords :
            i += 1
            r = requests.get('https://trends.google.com/trends/api/dailytrends?hl=' + lang + '&ed=' + str((date.today() - timedelta(days = i)).strftime('%Y%m%d')) + '&geo=' + geo + '&ns=15')
            google_trends = json.loads(r.text[6:])
            for topic in google_trends['default']['trendingSearchesDays'][0]['trendingSearches']:
                search_terms.append(topic['title']['query'].lower())
                for related_topic in topic['relatedQueries']:
                    search_terms.append(related_topic['query'].lower())
            search_terms = list(set(search_terms))
        del search_terms[numberOfwords:(len(search_terms)+1)]
        return search_terms

    def getRelatedTerms(browser: WebDriver, word: str) -> list:
        try:
            current_user_agent = browser.execute_script("return navigator.userAgent")
            r = requests.get('https://api.bing.com/osjson.aspx?query=' + word, headers = {'User-agent': current_user_agent})
            return r.json()[1]
        except:
            return []
        
    def getRemainingSearches(browser: WebDriver, mobileOnly: bool = False):
        browser.get('https://rewards.bing.com/')
        time.sleep(5)

        dashboard = Utilities.getDashboardData(browser)
        searchPoints = 1
        counters = dashboard['userStatus']['counters']
        if not 'pcSearch' in counters:
            return 0, 0
        progressDesktop = counters['pcSearch'][0]['pointProgress'] + counters['pcSearch'][1]['pointProgress']
        targetDesktop = counters['pcSearch'][0]['pointProgressMax'] + counters['pcSearch'][1]['pointProgressMax']
        if targetDesktop == 33 :
            #Level 1 EU
            searchPoints = 3
        elif targetDesktop == 55 :
            #Level 1 US
            searchPoints = 5
        elif targetDesktop == 102 :
            #Level 2 EU
            searchPoints = 3
        elif targetDesktop >= 170 :
            #Level 2 US
            searchPoints = 5
        remainingDesktop = int((targetDesktop - progressDesktop) / searchPoints)
        remainingMobile = 0
        if dashboard['userStatus']['levelInfo']['activeLevel'] != "Level1":
            progressMobile = counters['mobileSearch'][0]['pointProgress']
            targetMobile = counters['mobileSearch'][0]['pointProgressMax']
            remainingMobile = int((targetMobile - progressMobile) / searchPoints)
        if mobileOnly:
            return remainingMobile
        return remainingDesktop, remainingMobile
    
    def waitUntilQuestionRefresh(browser: WebDriver):
        tries = 0
        refreshCount = 0
        while True:
            try:
                browser.find_elements(By.CLASS_NAME, 'rqECredits')[0]
                return True
            except:
                if tries < 10:
                    tries += 1
                    time.sleep(0.5)
                else:
                    if refreshCount < 5:
                        browser.refresh()
                        refreshCount += 1
                        tries = 0
                        time.sleep(5)
                    else:
                        return False

    def waitUntilQuizLoads(browser: WebDriver):
        tries = 0
        refreshCount = 0
        while True:
            try:
                browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]')
                return True
            except:
                if tries < 10:
                    tries += 1
                    time.sleep(0.5)
                else:
                    if refreshCount < 5:
                        browser.refresh()
                        refreshCount += 1
                        tries = 0
                        time.sleep(5)
                    else:
                        return False

    def resetTabs(browser: WebDriver):
        try:
            curr = browser.current_window_handle

            for handle in browser.window_handles:
                if handle != curr:
                    browser.switch_to.window(handle)
                    time.sleep(0.5)
                    browser.close()
                    time.sleep(0.5)

            browser.switch_to.window(curr)
            time.sleep(0.5)
            browser.get('https://account.microsoft.com/rewards/')
        except:
            browser.get('https://account.microsoft.com/rewards/')

    def getAnswerCode(key: str, string: str) -> str:
        t = 0
        for i in range(len(string)):
            t += ord(string[i])
        t += int(key[-2:], 16)
        return str(t)
