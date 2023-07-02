from Utilities import *
from logs.Logger import *
import random
import settings

class PunchCards:
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
                        Utilities.waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
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
                                    if not Utilities.waitUntilQuestionRefresh(browser):
                                        return
                                time.sleep(5)
                            elif numberOfOptions == 4:
                                correctOption = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
                                for i in range(4):
                                    if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("data-option") == correctOption:
                                        browser.find_element(By.ID, "rqAnswerOption" + str(i)).click()
                                        time.sleep(5)
                                        if not Utilities.waitUntilQuestionRefresh(browser):
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
        punchCards = Utilities.getDashboardData(browser)['punchCards']
        for punchCard in punchCards:
            try:
                if punchCard['parentPromotion'] != None and punchCard['childPromotions'] != None and punchCard['parentPromotion']['complete'] == False and punchCard['parentPromotion']['pointProgressMax'] != 0 and punchCard['parentPromotion']['promotionType'] != 'appstore':
                    url = punchCard['parentPromotion']['attributes']['destination']
                    PunchCards.completePunchCard(browser, url, punchCard['childPromotions'])
            except Exception as err:
                settings.logger.log('[ERROR]', str(err))
                Utilities.resetTabs(browser)
        time.sleep(2)
        browser.get('https://rewards.bing.com/')
        time.sleep(2)
