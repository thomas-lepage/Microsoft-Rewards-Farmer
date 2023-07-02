from Utilities import *
from logs.Logger import *
import random

class Promotions:
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
        if not Utilities.waitUntilQuizLoads(browser):
            Utilities.resetTabs(browser)
            return
        browser.find_element(By.XPATH, '//*[@id="rqStartQuiz"]').click()
        Utilities.waitUntilVisible(browser, By.XPATH, '//*[@id="currentQuestionContainer"]/div/div[1]', 10)
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
        if not Utilities.waitUntilQuizLoads(browser):
            Utilities.resetTabs(browser)
            return
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
        morePromotions = Utilities.getDashboardData(browser)['morePromotions']
        i = 0
        for promotion in morePromotions:
            try:
                i += 1
                if promotion['complete'] == False and promotion['pointProgressMax'] != 0:
                    if promotion['promotionType'] == "urlreward":
                        Promotions.completeMorePromotionSearch(browser, i)
                    elif promotion['promotionType'] == "quiz" and promotion['pointProgress'] == 0:
                        if promotion['pointProgressMax'] == 10:
                            Promotions.completeMorePromotionABC(browser, i)
                        elif promotion['pointProgressMax'] == 30 or promotion['pointProgressMax'] == 40:
                            Promotions.completeMorePromotionQuiz(browser, i)
                        elif promotion['pointProgressMax'] == 50:
                            Promotions.completeMorePromotionThisOrThat(browser, i)
                    else:
                        if promotion['pointProgressMax'] == 10:
                            Promotions.completeMorePromotionClick(browser, i)
                        if promotion['pointProgressMax'] == 100 or promotion['pointProgressMax'] == 200:
                            Promotions.completeMorePromotionSearch(browser, i)
            except:
                Utilities.resetTabs(browser)
