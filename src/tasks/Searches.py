import time
import random
from selenium.common.exceptions import *
from Utilities import *
from logs.Logger import *
import settings

class Searches:
    def bingSearches(browser: WebDriver, numberOfSearches: int, config, isMobile: bool = False):
        i = 0
        search_terms = Utilities.getGoogleTrends(numberOfSearches, config["languageCode"], config["geoCode"])
        for word in search_terms :
            i += 1
            settings.logger.log('[BING]', str(i) + "/" + str(numberOfSearches))
            points = Searches.bingSearch(browser, word, isMobile)
            if points <= settings.pointsCounter :
                relatedTerms = Utilities.getRelatedTerms(browser, word)
                for term in relatedTerms :
                    points = Searches.bingSearch(browser, term, isMobile)
                    if not points <= settings.pointsCounter :
                        break
            if points > 0:
                settings.pointsCounter = points
            else:
                break

    def bingSearch(browser: WebDriver, word: str, isMobile: bool):
        browser.get('https://bing.com')
        time.sleep(2)
        searchbar = Utilities.waitForElement(browser, By.ID, 'sb_form_q')
        searchbar.send_keys(word)
        searchbar.submit()
        time.sleep(random.randint(10, 15))
        points = 0
        try:
            if not isMobile:
                points = int(Utilities.waitForElement(browser, By.ID, 'id_rc').get_attribute('innerHTML'))
            else:
                try :
                    browser.find_element(By.ID, 'mHamburger').click()
                except UnexpectedAlertPresentException:
                    try :
                        browser.switch_to.alert.accept()
                        time.sleep(1)
                        Utilities.waitForElement(browser, By.ID, 'mHamburger').click()
                    except NoAlertPresentException :
                        pass
                time.sleep(1)
                points = int(Utilities.waitForElement(browser, By.ID, 'fly_id_rc').get_attribute('innerHTML'))
        except:
            pass
        return points