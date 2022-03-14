from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
url = "https://www.imdb.com"
wait = WebDriverWait(driver, 10)
driver.get("https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm")
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".lister-list > tr > td.posterColumn")))



while True:
    soup = BeautifulSoup(driver.page_source,"lxml")
    for posterColumn in soup.select('.lister-list > tr > td.posterColumn'):
        rating = posterColumn.contents[3]['data-value']
        print(rating)
        exit()
        links = url + item['href']
        print(links)

    try:
        link = driver.find_element_by_id("next")
        link.click()
        wait.until(EC.staleness_of(link))
    except Exception:
        break
driver.quit()