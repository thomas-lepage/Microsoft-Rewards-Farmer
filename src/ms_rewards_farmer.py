import time
import json
from datetime import date, timedelta, datetime
import requests
import random
import schedule
import urllib.parse
import os
import sys
import urllib.request
import logging

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from simplejson import JSONDecodeError

# Define user-agents
PC_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63'
MOBILE_USER_AGENT = 'Mozilla/5.0 (Linux; Android 12; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.50 Mobile Safari/537.36'

POINTS_COUNTER = 0
STREAK_DATA = 0

# Define browser setup function
def browserSetup(headless_mode: bool = False, user_agent: str = PC_USER_AGENT) -> WebDriver:
    # Create Chrome browser
    from selenium.webdriver.chrome.options import Options
    options = Options()
    if "SUPERVISOR_TOKEN" in os.environ:
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=" + user_agent)
    options.add_argument('lang=' + LANG.split("-")[0])
    if headless_mode :
        options.add_argument("--headless")
    options.add_argument('log-level=3')
    chrome_browser_obj = webdriver.Chrome(options=options)
    return chrome_browser_obj

# Define login function
def login(browser: WebDriver, email: str, pwd: str, isMobile: bool = False):
    # Access to bing.com
    browser.get('https://login.live.com/')
    try:
        # Wait complete loading
        waitUntilVisible(browser, By.ID, 'loginHeader', 10)
        # Enter email
        pr('[LOGIN]', 'Writing email...')
        waitForElement(browser, By.NAME, "loginfmt").send_keys(email)
        # Click next
        waitForElement(browser, By.ID, 'idSIButton9').click()
        # Wait 2 seconds
        time.sleep(2)
        # Wait complete loading
        waitUntilVisible(browser, By.ID, 'loginHeader', 10)
        # Enter password
        browser.execute_script("document.getElementById('i0118').value = '" + pwd + "';")
        pr('[LOGIN]', 'Writing password...')
        # Click next
        waitForElement(browser, By.ID, 'idSIButton9').click()
    except (TimeoutException) as e:
        raise Exception('Timeout while login')

    # Wait 5 seconds
    time.sleep(5)
    # Click Security Check
    pr('[LOGIN]', 'Passing security checks...')
    try:
        browser.find_element(By.ID, 'iLandingViewAction').click()
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    # Wait complete loading
    try:
        waitUntilVisible(browser, By.ID, 'KmsiCheckboxField', 10)
    except (TimeoutException) as e:
        pass
    # Click next
    try:
        browser.find_element(By.ID, 'idSIButton9').click()
        # Wait 5 seconds
        time.sleep(5)
    except (NoSuchElementException, ElementNotInteractableException) as e:
        pass
    pr('[LOGIN]', 'Logged-in !')
    # Check Login
    pr('[LOGIN]', 'Ensuring login on Bing...')
    checkBingLogin(browser, isMobile)

def checkBingLogin(browser: WebDriver, isMobile: bool = False):
    global POINTS_COUNTER
    #Access Bing.com
    browser.get('https://bing.com/')
    # Wait 8 seconds
    time.sleep(8)
    #Accept Cookies
    try:
        waitForElement(browser, By.ID, 'bnp_btn_accept').click()
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
        waitForElement(browser, By.ID, 'bnp_close_link').click()
    except:
        pass
    if isMobile:
        try:
            time.sleep(1)
            waitForElement(browser, By.ID, 'mHamburger').click()
        except:
            try:
                waitForElement(browser, By.ID, 'bnp_btn_accept').click()
            except:
                pass
            time.sleep(1)
            try:
                waitForElement(browser, By.ID, 'mHamburger').click()
            except:
                pass
        try:
            time.sleep(1)
            waitForElement(browser, By.ID, 'HBSignIn').click()
        except:
            pass
        try:
            time.sleep(2)
            waitForElement(browser, By.ID, 'iShowSkip').click()
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
            POINTS_COUNTER = int(waitForElement(browser, By.ID, 'id_rc').get_attribute('innerHTML'))
        else:
            try:
                waitForElement(browser, By.ID, 'mHamburger').click()
            except:
                try:
                    browser.waitForElement(browser, By.ID, 'bnp_btn_accept').click()
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
                    waitForElement(browser, By.ID, 'bnp_close_link').click()
                except:
                    pass
                time.sleep(1)
                waitForElement(browser, By.ID, 'mHamburger').click()
            time.sleep(1)
            POINTS_COUNTER = int(waitForElement(browser, By.ID, 'fly_id_rc').get_attribute('innerHTML'))
    except:
        checkBingLogin(browser, isMobile)

def waitForElement(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    return WebDriverWait(browser, time_to_wait).until(ec.presence_of_element_located((by_, selector)))

def waitUntilVisible(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    WebDriverWait(browser, time_to_wait).until(ec.visibility_of_element_located((by_, selector)))

def waitUntilClickable(browser: WebDriver, by_: By, selector: str, time_to_wait: int = 10):
    WebDriverWait(browser, time_to_wait).until(ec.element_to_be_clickable((by_, selector)))

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

def findBetween(s: str, first: str, last: str) -> str:
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def getCCodeLangAndOffset() -> tuple:
    lang = 'en-CA'
    geo = 'CA'
    tz = '-300'
    return(lang, geo, tz)

def getGoogleTrends(numberOfwords: int) -> list:
    search_terms = []
    i = 0
    while len(search_terms) < numberOfwords :
        i += 1
        r = requests.get('https://trends.google.com/trends/api/dailytrends?hl=' + LANG + '&ed=' + str((date.today() - timedelta(days = i)).strftime('%Y%m%d')) + '&geo=' + GEO + '&ns=15')
        google_trends = json.loads(r.text[6:])
        for topic in google_trends['default']['trendingSearchesDays'][0]['trendingSearches']:
            search_terms.append(topic['title']['query'].lower())
            for related_topic in topic['relatedQueries']:
                search_terms.append(related_topic['query'].lower())
        search_terms = list(set(search_terms))
    del search_terms[numberOfwords:(len(search_terms)+1)]
    return search_terms

def getRelatedTerms(word: str) -> list:
    try:
        r = requests.get('https://api.bing.com/osjson.aspx?query=' + word, headers = {'User-agent': PC_USER_AGENT})
        return r.json()[1]
    except:
        return []

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

def bingSearches(browser: WebDriver, numberOfSearches: int, isMobile: bool = False):
    global POINTS_COUNTER
    i = 0
    search_terms = getGoogleTrends(numberOfSearches)
    for word in search_terms :
        i += 1
        pr('[BING]', str(i) + "/" + str(numberOfSearches))
        points = bingSearch(browser, word, isMobile)
        if points <= POINTS_COUNTER :
            relatedTerms = getRelatedTerms(word)
            for term in relatedTerms :
                points = bingSearch(browser, term, isMobile)
                if not points <= POINTS_COUNTER :
                    break
        if points > 0:
            POINTS_COUNTER = points
        else:
            break

def bingSearch(browser: WebDriver, word: str, isMobile: bool):
    browser.get('https://bing.com')
    time.sleep(2)
    searchbar = waitForElement(browser, By.ID, 'sb_form_q')
    searchbar.send_keys(word)
    searchbar.submit()
    time.sleep(random.randint(10, 15))
    points = 0
    try:
        if not isMobile:
            points = int(waitForElement(browser, By.ID, 'id_rc').get_attribute('innerHTML'))
        else:
            try :
                browser.find_element(By.ID, 'mHamburger').click()
            except UnexpectedAlertPresentException:
                try :
                    browser.switch_to.alert.accept()
                    time.sleep(1)
                    waitForElement(browser, By.ID, 'mHamburger').click()
                except NoAlertPresentException :
                    pass
            time.sleep(1)
            points = int(waitForElement(browser, By.ID, 'fly_id_rc').get_attribute('innerHTML'))
    except:
        pass
    return points

def completePromotionalItems(browser: WebDriver):
    try:
        item = getDashboardData(browser)["promotionalItem"]
        if (item["pointProgressMax"] == 100 or item["pointProgressMax"] == 200) and item["complete"] == False and item["destinationUrl"] == "https://account.microsoft.com/rewards":
            browser.find_element(By.XPATH, '//*[@id="promo-item"]/section/div/div/div/a').click()
            time.sleep(1)
            browser.switch_to.window(window_name = browser.window_handles[1])
            time.sleep(8)
            browser.close()
            time.sleep(2)
            browser.switch_to.window(window_name = browser.window_handles[0])
            time.sleep(2)
    except:
        pass

def completeDailySetSearch(browser: WebDriver, cardNumber: int):
    time.sleep(5)
    browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(random.randint(13, 17))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetSurvey(browser: WebDriver, cardNumber: int):
    time.sleep(5)
    browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    browser.find_element(By.ID, "btoption" + str(random.randint(0, 1))).click()
    time.sleep(random.randint(10, 15))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetQuiz(browser: WebDriver, cardNumber: int, progress: int):
    time.sleep(2)
    browser.find_element(By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    if progress == 0:
        if not waitUntilQuizLoads(browser):
            resetTabs(browser)
            return
        browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(5)
    numberOfQuestions = browser.execute_script("return _w.rewardsQuizRenderInfo.maxQuestions")
    numberOfQuestionsCompleted = int(browser.execute_script("return _w.rewardsQuizRenderInfo.currentQuestionNumber")) - 1
    numberOfOptions = browser.execute_script("return _w.rewardsQuizRenderInfo.numberOfOptions")
    for question in range(numberOfQuestions - numberOfQuestionsCompleted):
        if numberOfOptions == 8:
            answers = []
            for i in range(8):
                if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("iscorrectoption").lower() == "true":
                    answers.append("rqAnswerOption" + str(i))
            for answer in answers:
                browser.find_element(By.ID, answer).click()
                time.sleep(10)
                if not waitUntilQuestionRefresh(browser):
                    return
            time.sleep(10)
        elif numberOfOptions == 4:
            correctOption = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
            for i in range(4):
                if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("data-option") == correctOption:
                    browser.find_element(By.ID, "rqAnswerOption" + str(i)).click()
                    time.sleep(5)
                    if not waitUntilQuestionRefresh(browser):
                        return
                    break
            time.sleep(10)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetVariableActivity(browser: WebDriver, cardNumber: int):
    time.sleep(2)
    waitForElement(browser, By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(8)
    try :
        browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 3)
    except (NoSuchElementException, TimeoutException):
        try:
            counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
            numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
            for question in range(numberOfQuestions):
                browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                time.sleep(5)
                browser.find_element(By.XPATH, '//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                time.sleep(3)
            time.sleep(5)
            browser.close()
            time.sleep(2)
            browser.switch_to.window(window_name=browser.window_handles[0])
            time.sleep(2)
            return
        except NoSuchElementException:
            time.sleep(random.randint(5, 9))
            browser.close()
            time.sleep(2)
            browser.switch_to.window(window_name = browser.window_handles[0])
            time.sleep(2)
            return
    time.sleep(3)
    correctAnswer = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
    if browser.find_element(By.ID, "rqAnswerOption0").get_attribute("data-option") == correctAnswer:
        browser.find_element(By.ID, "rqAnswerOption0").click()
    else :
        browser.find_element(By.ID, "rqAnswerOption1").click()
    time.sleep(10)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeDailySetThisOrThat(browser: WebDriver, cardNumber: int, progress: int):
    time.sleep(2)
    waitForElement(browser, By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    if not waitUntilQuizLoads(browser):
        resetTabs(browser)
        return
    if progress == 0:
        browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for question in range(10):
        answerEncodeKey = browser.execute_script("return _G.IG")

        answer1 = browser.find_element(By.ID, "rqAnswerOption0")
        answer1Title = answer1.get_attribute('data-option')
        answer1Code = getAnswerCode(answerEncodeKey, answer1Title)

        answer2 = browser.find_element(By.ID, "rqAnswerOption1")
        answer2Title = answer2.get_attribute('data-option')
        answer2Code = getAnswerCode(answerEncodeKey, answer2Title)

        correctAnswerCode = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")

        if (answer1Code == correctAnswerCode):
            answer1.click()
            time.sleep(8)
        elif (answer2Code == correctAnswerCode):
            answer2.click()
            time.sleep(8)

    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

def getDashboardData(browser: WebDriver) -> dict:
    dashboard = findBetween(waitForElement(browser, By.XPATH, '/html/body').get_attribute('innerHTML'), "var dashboard = ", ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
    try:
        dashboard = json.loads(dashboard)
    except (TimeoutException, JSONDecodeError) as err:
        try:
            browser.find_element(By.ID, "start-earning-rewards-link").click()
            time.sleep(5)
            dashboard = findBetween(waitForElement(browser, By.XPATH, '/html/body').get_attribute('innerHTML'), "var dashboard = ", ";\n        appDataModule.constant(\"prefetchedDashboard\", dashboard);")
            dashboard = json.loads(dashboard)
        except (TimeoutException, JSONDecodeError, NoSuchElementException) as err:
            raise Exception('Error getting the dashboard', err)
    return dashboard

def completeDailySet(browser: WebDriver):
    d = getDashboardData(browser)['dailySetPromotions']
    todayDate = datetime.today().strftime('%m/%d/%Y')
    todayPack = []
    for date, data in d.items():
        if date == todayDate:
            todayPack = data
    for activity in todayPack:
        try:
            if activity['complete'] == False:
                cardNumber = int(activity['offerId'][-1:])
                if activity['promotionType'] == "urlreward":
                    pr('[DAILY SET]', 'Completing search of card ' + str(cardNumber))
                    completeDailySetSearch(browser, cardNumber)
                if activity['promotionType'] == "quiz":
                    if activity['pointProgressMax'] == 50:
                        pr('[DAILY SET]', 'Completing This or That of card ' + str(cardNumber))
                        completeDailySetThisOrThat(browser, cardNumber, activity['pointProgress'])
                    elif (activity['pointProgressMax'] == 40 or activity['pointProgressMax'] == 30):
                        pr('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                        completeDailySetQuiz(browser, cardNumber, activity['pointProgress'])
                    elif activity['pointProgressMax'] == 10 and activity['pointProgress'] == 0:
                        searchUrl = urllib.parse.unquote(urllib.parse.parse_qs(urllib.parse.urlparse(activity['destinationUrl']).query)['ru'][0])
                        searchUrlQueries = urllib.parse.parse_qs(urllib.parse.urlparse(searchUrl).query)
                        filters = {}
                        for filter in searchUrlQueries['filters'][0].split(" "):
                            filter = filter.split(':', 1)
                            filters[filter[0]] = filter[1]
                        if "PollScenarioId" in filters:
                            pr('[DAILY SET]', 'Completing poll of card ' + str(cardNumber))
                            completeDailySetSurvey(browser, cardNumber)
                        else:
                            pr('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                            completeDailySetVariableActivity(browser, cardNumber)
        except:
            resetTabs(browser)

def getAccountPoints(browser: WebDriver) -> int:
    return getDashboardData(browser)['userStatus']['availablePoints']

def completePunchCard(browser: WebDriver, url: str, childPromotions: dict):
    browser.get(url)
    for child in childPromotions:
        if child['complete'] == False:
            if child['promotionType'] == "urlreward":
                time.sleep(5)
                browser.find_element(By.PARTIAL_LINK_TEXT, child['attributes']['title']).click()
                time.sleep(random.randint(13, 17))
                browser.switch_to.window(window_name = browser.window_handles[0])
                time.sleep(2)
            if child['promotionType'] == "quiz":
                browser.execute_script("window.open('%s');" % child['attributes']['destination'])
                time.sleep(5)
                browser.switch_to.window(window_name = browser.window_handles[1])
                time.sleep(8)
                if child['pointProgress'] == 0:
                    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
                    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
                try:
                    counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
                    numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
                    for question in range(numberOfQuestions):
                        browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
                        time.sleep(5)
                        browser.find_element(By.XPATH, '//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
                        time.sleep(7)
                except NoSuchElementException as err:
                    numberOfQuestions = browser.execute_script("return _w.rewardsQuizRenderInfo.maxQuestions")
                    numberOfOptions = browser.execute_script("return _w.rewardsQuizRenderInfo.numberOfOptions")
                    for question in range(numberOfQuestions):
                        if numberOfOptions == 8:
                            answers = []
                            for i in range(8):
                                if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("iscorrectoption").lower() == "true":
                                    answers.append("rqAnswerOption" + str(i))
                            for answer in answers:
                                browser.find_element(By.ID, answer).click()
                                time.sleep(5)
                                if not waitUntilQuestionRefresh(browser):
                                    return
                            time.sleep(5)
                        elif numberOfOptions == 4:
                            correctOption = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
                            for i in range(4):
                                if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("data-option") == correctOption:
                                    browser.find_element(By.ID, "rqAnswerOption" + str(i)).click()
                                    time.sleep(5)
                                    if not waitUntilQuestionRefresh(browser):
                                        return
                                    break
                            time.sleep(5)
                    pass
                time.sleep(5)
                browser.switch_to.window(window_name = browser.window_handles[0])
            time.sleep(2)
            browser.get(url)
            time.sleep(2)

def completePunchCards(browser: WebDriver):
    global STREAK_DATA
    punchCards = getDashboardData(browser)['punchCards']
    for punchCard in punchCards:
        try:
            if punchCard['parentPromotion'] != None and punchCard['childPromotions'] != None and punchCard['parentPromotion']['complete'] == False and punchCard['parentPromotion']['pointProgressMax'] != 0 and punchCard['parentPromotion']['promotionType'] != 'appstore':
                url = punchCard['parentPromotion']['attributes']['destination']
                completePunchCard(browser, url, punchCard['childPromotions'])
        except Exception as err:
            pr(err)
            resetTabs(browser)
    time.sleep(2)
    browser.get('https://rewards.microsoft.com/')
    time.sleep(2)

def completeMorePromotionSearch(browser: WebDriver, cardNumber: int):
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name = browser.window_handles[1])
    time.sleep(random.randint(13, 17))
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name = browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionQuiz(browser: WebDriver, cardNumber: int):
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    if not waitUntilQuizLoads(browser):
        resetTabs(browser)
        return
    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    numberOfQuestions = browser.execute_script("return _w.rewardsQuizRenderInfo.maxQuestions")
    numberOfOptions = browser.execute_script("return _w.rewardsQuizRenderInfo.numberOfOptions")
    for question in range(numberOfQuestions):
        if numberOfOptions == 8:
            answers = []
            for i in range(8):
                if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("iscorrectoption").lower() == "true":
                    answers.append("rqAnswerOption" + str(i))
            for answer in answers:
                browser.find_element(By.ID, answer).click()
                time.sleep(5)
                if not waitUntilQuestionRefresh(browser):
                    return
            time.sleep(5)
        elif numberOfOptions == 4:
            correctOption = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
            for i in range(4):
                if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("data-option") == correctOption:
                    browser.find_element(By.ID, "rqAnswerOption" + str(i)).click()
                    time.sleep(5)
                    if not waitUntilQuestionRefresh(browser):
                        return
                    break
            time.sleep(5)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionABC(browser: WebDriver, cardNumber: int):
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    counter = str(browser.find_element(By.XPATH, '//*[@id="QuestionPane0"]/div[2]').get_attribute('innerHTML'))[:-1][1:]
    numberOfQuestions = max([int(s) for s in counter.split() if s.isdigit()])
    for question in range(numberOfQuestions):
        browser.execute_script('document.evaluate("//*[@id=\'QuestionPane' + str(question) + '\']/div[1]/div[2]/a[' + str(random.randint(1, 3)) + ']/div", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        time.sleep(5)
        browser.find_element(By.XPATH, '//*[@id="AnswerPane' + str(question) + '"]/div[1]/div[2]/div[4]/a/div/span/input').click()
        time.sleep(3)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionThisOrThat(browser: WebDriver, cardNumber: int):
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    if not waitUntilQuizLoads(browser):
        resetTabs(browser)
        return
    browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
    waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
    time.sleep(3)
    for question in range(10):
        answerEncodeKey = browser.execute_script("return _G.IG")

        answer1 = browser.find_element(By.ID, "rqAnswerOption0")
        answer1Title = answer1.get_attribute('data-option')
        answer1Code = getAnswerCode(answerEncodeKey, answer1Title)

        answer2 = browser.find_element(By.ID, "rqAnswerOption1")
        answer2Title = answer2.get_attribute('data-option')
        answer2Code = getAnswerCode(answerEncodeKey, answer2Title)

        correctAnswerCode = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")

        if (answer1Code == correctAnswerCode):
            answer1.click()
            time.sleep(8)
        elif (answer2Code == correctAnswerCode):
            answer2.click()
            time.sleep(8)

    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])
    time.sleep(2)

def completeMorePromotionClick(browser: WebDriver, cardNumber: int):
    browser.find_element(By.XPATH, '//*[@id="more-activities"]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-more-activities-card-item/div/a').click()
    time.sleep(1)
    browser.switch_to.window(window_name=browser.window_handles[1])
    time.sleep(8)
    time.sleep(5)
    browser.close()
    time.sleep(2)
    browser.switch_to.window(window_name=browser.window_handles[0])

def completeMorePromotions(browser: WebDriver):
    morePromotions = getDashboardData(browser)['morePromotions']
    i = 0
    for promotion in morePromotions:
        try:
            i += 1
            if promotion['complete'] == False and promotion['pointProgressMax'] != 0:
                if promotion['promotionType'] == "urlreward":
                    completeMorePromotionSearch(browser, i)
                elif promotion['promotionType'] == "quiz" and promotion['pointProgress'] == 0:
                    if promotion['pointProgressMax'] == 10:
                        completeMorePromotionABC(browser, i)
                    elif promotion['pointProgressMax'] == 30 or promotion['pointProgressMax'] == 40:
                        completeMorePromotionQuiz(browser, i)
                    elif promotion['pointProgressMax'] == 50:
                        completeMorePromotionThisOrThat(browser, i)
                else:
                    if promotion['pointProgressMax'] == 10:
                        completeMorePromotionClick(browser, i)
                    if promotion['pointProgressMax'] == 100 or promotion['pointProgressMax'] == 200:
                        completeMorePromotionSearch(browser, i)
        except:
            resetTabs(browser)

def getRemainingSearches(browser: WebDriver, mobileOnly: bool = False):
    browser.get('https://rewards.microsoft.com/')
    time.sleep(5)

    dashboard = getDashboardData(browser)
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
        return remainingMobile;
    return remainingDesktop, remainingMobile

def schedule_next_run(): # set next run for random hour and minute each day
   time_str = '{:02d}:{:02d}'.format(random.randint(7, 10), random.randint(0, 59))
   schedule.clear()
   prPurple("Next run scheduled for tomorrow, {}, at {}".format((date.today() + timedelta(days=1)).strftime("%B %d"),time_str))
   time.sleep(14400) #sleep so job will not happen twice in a day
   schedule.every().day.at(time_str).do(run)

def sendToIFTTT(message, iftttUrl):
    data = json.dumps({"value1": message}).encode()
    req = urllib.request.Request(iftttUrl)
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, data) as opened_req:
        result = opened_req.read().decode()
    prGreen('[PUSH NOTIFICATIONS]' + result)

def prRed(prt):
    print("\033[31m{}\033[00m".format(prt))
    logger.trace("\033[31m{}\033[00m".format(prt))
def prGreen(prt):
    print("\033[32m{}\033[00m".format(prt))
    logger.trace("\033[32m{}\033[00m".format(prt))
def prPurple(prt):
    print("\033[35m{}\033[00m".format(prt))
    logger.trace("\033[35m{}\033[00m".format(prt))
def prYellow(prt):
    print("\033[33m{}\033[00m".format(prt))
    logger.trace("\033[33m{}\033[00m".format(prt))
def pr(*prt: object):
    print(' '.join(prt))
    logger.trace(' '.join(prt))

def getActivitiesToComplete(browser: WebDriver) -> dict:
    browser.get('https://rewards.microsoft.com/')
    time.sleep(10)

    dashboard = getDashboardData(browser)
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
                if childPromotion['pointProgressMax'] > 0 and childPromotion['pointProgress'] < childPromotion['pointProgressMax']:
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
    remainingSearches, remainingSearchesM = getRemainingSearches(browser)

    toComplete['desktopSearch'] = []
    toComplete['mobileSearch'] = []

    if remainingSearches != 0:
        toComplete['desktopSearch'] = remainingSearches

    toComplete = {k:v for k,v in toComplete.items() if v}
    return toComplete

def getStreakData(browser):
    browser.get('https://rewards.microsoft.com/')
    try:
        time.sleep(8)
        return browser.find_element(By.ID, 'streak').get_attribute('aria-label')
    except (Exception, NoSuchElementException) as err:
        prRed(err)
        raise Exception('Error while getting the streak', err)

def doAccount(account):
    browser = browserSetup(True, PC_USER_AGENT)
    pr('[LOGIN]', 'Logging-in...')
    login(browser, account['username'], account['password'])
    prGreen('[LOGIN] Logged-in successfully !')
    startingPoints = POINTS_COUNTER
    prGreen('[POINTS] You have ' + str(POINTS_COUNTER) + ' points on your account !')
    STREAK_DATA = getStreakData(browser)

    # Check if there's things to do.
    attempts = 0
    toComplete = getActivitiesToComplete(browser)
    while bool(toComplete) and attempts < 5:
        prYellow("[INFO] Desktop Attempt #" + str(attempts))
        time.sleep(5)

        if 'dailySetPromotions' in toComplete:
            pr('[DAILY SET]', 'Trying to complete the Daily Set...')
            try:
                completeDailySet(browser)
                prGreen('[DAILY SET] Completed the Daily Set successfully !')
            except (Exception, SessionNotCreatedException) as err:
                prRed('[DAILY SET] Did not complet Daily Set !')
                prRed(err)
                pass
        if 'punchCards' in toComplete:
            pr('[PUNCH CARDS]', 'Trying to complete the Punch Cards...')
            try:
                completePunchCards(browser)
                prGreen('[PUNCH CARDS] Completed the Punch Cards successfully !')
            except (Exception, SessionNotCreatedException) as err:
                prRed('[PUNCH CARDS] Did not complet Punch Cards !')
                prRed(err)
                pass
        if 'morePromotions' in toComplete:
            pr('[MORE PROMO]', 'Trying to complete More Promotions...')
            try:
                completeMorePromotions(browser)
                prGreen('[MORE PROMO] Completed More Promotions successfully !')
            except (Exception, SessionNotCreatedException) as err:
                prRed('[MORE PROMO] Did not complet More Promotions !')
                prRed(err)
                pass
        if 'desktopSearch' in toComplete:
            pr('[BING]', 'Starting Desktop and Edge Bing searches...')
            try:
                bingSearches(browser, toComplete['desktopSearch'])
                prGreen('[BING] Finished Desktop and Edge Bing searches !')
            except (Exception, SessionNotCreatedException) as err:
                prRed('[BING] Did not complet Desktop search !')
                prRed(err)
                pass

        attempts = attempts + 1
        prYellow('[INFO] Checking if everything in desktop is done...')
        toComplete = getActivitiesToComplete(browser)
        browser.get('https://rewards.microsoft.com/')
        STREAK_DATA = getStreakData(browser)
        time.sleep(30)

    browser.quit()
    browser = None
    browser = browserSetup(True, MOBILE_USER_AGENT)
    pr('[LOGIN]', 'Mobile logging-in...')
    login(browser, account['username'], account['password'], True)
    pr('[LOGIN]', 'Mobile logged-in successfully !')
    remainingSearchesM = getRemainingSearches(browser, True)
    attempts = 0
    while remainingSearchesM > 0 and attempts < 5:
        time.sleep(5)
        prYellow("[INFO] Mobile Attempt #" + str(attempts))
        if remainingSearchesM > 0:
            pr('[BING]', 'Starting Mobile Bing searches...')
            bingSearches(browser, remainingSearchesM, True)
            prGreen('[BING] Finished Mobile Bing searches !')
            remainingSearchesM = getRemainingSearches(browser, True)
            attempts = attempts + 1

    account['completed'] = True
    prGreen('[POINTS] You have earned ' + str(POINTS_COUNTER - startingPoints) + ' this run !')
    prGreen('[POINTS] You are now at ' + str(POINTS_COUNTER) + ' points !')
    prGreen('[STREAK] ' + STREAK_DATA.split(',')[0] + (' day.' if STREAK_DATA.split(',')[0] == '1' else ' days!') + STREAK_DATA.split(',')[2])
    if account['iftttAppletUrl']:
        message = account['name'] + '\'s account completed. Today : ' + str(POINTS_COUNTER - startingPoints) + ' Total : ' + str(POINTS_COUNTER) + ' Streak : ' + STREAK_DATA.split(',')[0] + (' day.' if STREAK_DATA.split(',')[0] == '1' else ' days!')
        sendToIFTTT(message, account['iftttAppletUrl'])
    
def run():
    prRed("""
    ███╗   ███╗███████╗    ███████╗ █████╗ ██████╗ ███╗   ███╗███████╗██████╗
    ████╗ ████║██╔════╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗
    ██╔████╔██║███████╗    █████╗  ███████║██████╔╝██╔████╔██║█████╗  ██████╔╝
    ██║╚██╔╝██║╚════██║    ██╔══╝  ██╔══██║██╔══██╗██║╚██╔╝██║██╔══╝  ██╔══██╗
    ██║ ╚═╝ ██║███████║    ██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║
    ╚═╝     ╚═╝╚══════╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝""")
    prPurple("        by Thomas Lepage                           version 2.1\n")

    random.shuffle(ACCOUNTS)
    for index, account in enumerate(ACCOUNTS, start=1):
        account['completed'] = False
        attempts = 1
        prYellow('********************' + account['username'] + '********************')
        while not account['completed'] and attempts <= 5:
            prYellow("[INFO] Attempting account for " + str(attempts) + " time")
            try:
                doAccount(account)
            except (Exception, SessionNotCreatedException) as err:
                prRed(err)
                pass

        if len(ACCOUNTS) > 1:
            if index < len(ACCOUNTS):
                randomTime = random.randint(1200, 5400)
                prRed("Current time {}".format(datetime.now().strftime("%H:%M")))
                time_str = (datetime.now() + timedelta(seconds=randomTime)).strftime("%H:%M")
                prRed("Next account run at {}".format(time_str))
                time.sleep(randomTime)
    schedule_next_run() #set a new hour and minute for the next day
    return schedule.CancelJob #cancel current time schedule

LANG, GEO, TZ = getCCodeLangAndOffset()

try:
    account_path = os.path.dirname(os.path.abspath(__file__)) + '/accounts.json'
    ACCOUNTS = json.load(open(account_path, "r"))
except FileNotFoundError:
    with open(account_path, 'w') as f:
        f.write(json.dumps([{
            "username": "Your Email",
            "password": "Your Password",
            "name": "Name of the account",
            "iftttAppletUrl": "Applet url"
        }], indent=4))
    prPurple("""
[ACCOUNT] Accounts credential file "accounts.json" created.
[ACCOUNT] Edit with your credentials and save, then press any key to continue...
    """)
    input()
    ACCOUNTS = json.load(open(account_path, "r"))

logging.TRACE = 51
logging.addLevelName(logging.TRACE, "TRACE")

def _trace(logger, message, *args, **kwargs):
    if logger.isEnabledFor(logging.TRACE):
        logger._log(logging.TRACE, message, args, **kwargs)

logging.Logger.trace = _trace 

#now we will Create and configure logger 
logPath = os.path.dirname(os.path.abspath(__file__)) + '/ms-rewards.log'
logging.basicConfig(filename=logPath, 
					format='%(asctime)s %(message)s', 
					filemode='a+') 
#Let us Create an object 
logger=logging.getLogger() 
logger.setLevel(logging.TRACE)

schedule.every().day.at("00:00").do(run) #Start scheduling to be replaced by random ints after first run is over

try:
    run() #Run for First time and set schedule for the next run

    while True:
        schedule.run_pending()
        time.sleep(60)
except KeyboardInterrupt:
    pr('Interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)