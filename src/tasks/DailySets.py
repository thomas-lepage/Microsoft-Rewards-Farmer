from Utilities import *
from logs.Logger import *
import urllib.parse
import urllib.request
import random
import settings

class DailySets:

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
            if not Utilities.waitUntilQuizLoads(browser):
                Utilities.resetTabs(browser)
                return
            browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
            Utilities.waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
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
                    if not Utilities.waitUntilQuestionRefresh(browser):
                        return
                time.sleep(10)
            elif numberOfOptions == 4:
                correctOption = browser.execute_script("return _w.rewardsQuizRenderInfo.correctAnswer")
                for i in range(4):
                    if browser.find_element(By.ID, "rqAnswerOption" + str(i)).get_attribute("data-option") == correctOption:
                        browser.find_element(By.ID, "rqAnswerOption" + str(i)).click()
                        time.sleep(5)
                        if not Utilities.waitUntilQuestionRefresh(browser):
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
        Utilities.waitForElement(browser, By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        time.sleep(1)
        browser.switch_to.window(window_name = browser.window_handles[1])
        time.sleep(8)
        try :
            browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
            Utilities.waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 3)
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
        Utilities.waitForElement(browser, By.XPATH, '//*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[' + str(cardNumber) + ']/div/card-content/mee-rewards-daily-set-item-content/div/a').click()
        time.sleep(1)
        browser.switch_to.window(window_name=browser.window_handles[1])
        time.sleep(8)
        if not Utilities.waitUntilQuizLoads(browser):
            Utilities.resetTabs(browser)
            return
        if progress == 0:
            browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
            Utilities.waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
        time.sleep(3)
        for question in range(10):
            answerEncodeKey = browser.execute_script("return _G.IG")

            answer1 = browser.find_element(By.ID, "rqAnswerOption0")
            answer1Title = answer1.get_attribute('data-option')
            answer1Code = Utilities.getAnswerCode(answerEncodeKey, answer1Title)

            answer2 = browser.find_element(By.ID, "rqAnswerOption1")
            answer2Title = answer2.get_attribute('data-option')
            answer2Code = Utilities.getAnswerCode(answerEncodeKey, answer2Title)

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

    def completeDailySet(browser: WebDriver):
        d = Utilities.getDashboardData(browser)['dailySetPromotions']
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
                        settings.logger.log('[DAILY SET]', 'Completing search of card ' + str(cardNumber))
                        DailySets.completeDailySetSearch(browser, cardNumber)
                    if activity['promotionType'] == "quiz":
                        if activity['pointProgressMax'] == 50:
                            settings.logger.log('[DAILY SET]', 'Completing This or That of card ' + str(cardNumber))
                            DailySets.completeDailySetThisOrThat(browser, cardNumber, activity['pointProgress'])
                        elif (activity['pointProgressMax'] == 40 or activity['pointProgressMax'] == 30):
                            settings.logger.log('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                            DailySets.completeDailySetQuiz(browser, cardNumber, activity['pointProgress'])
                        elif activity['pointProgressMax'] == 10 and activity['pointProgress'] == 0:
                            searchUrl = urllib.parse.unquote(urllib.parse.parse_qs(urllib.parse.urlparse(activity['destinationUrl']).query)['ru'][0])
                            searchUrlQueries = urllib.parse.parse_qs(urllib.parse.urlparse(searchUrl).query)
                            filters = {}
                            for filter in searchUrlQueries['filters'][0].split(" "):
                                filter = filter.split(':', 1)
                                filters[filter[0]] = filter[1]
                            if "PollScenarioId" in filters:
                                settings.logger.log('[DAILY SET]', 'Completing poll of card ' + str(cardNumber))
                                DailySets.completeDailySetSurvey(browser, cardNumber)
                            else:
                                settings.logger.log('[DAILY SET]', 'Completing quiz of card ' + str(cardNumber))
                                DailySets.completeDailySetVariableActivity(browser, cardNumber)
            except:
                Utilities.resetTabs(browser)
