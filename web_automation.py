
from time import sleep
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd


driver = Firefox()
driver.get('https://www.mercadolibre.com.co/')

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'nav-search-input'))
    )
    element.send_keys('computador portatil')
except:
    print('Error')
driver.find_element_by_class_name('nav-search-btn').click()

try:
    items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-search-layout__item'))
    )
except:
    print('Error')   

# items = driver.find_elements_by_class_name('ui-search-layout__item')

specs = []
for item in items:
    url = item.find_element_by_class_name('ui-search-result__image').find_element_by_css_selector('a').get_attribute('href')
    driver.execute_script(f"window.open('{url}', 'new_window')")
    driver.switch_to_window(driver.window_handles[-1])
 
    try:
        tables = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'ui-vpp-striped-specs__table'))
        )
    except:
        print('Error')   
    
    # tables = driver.find_elements_by_class_name('ui-vpp-striped-specs__table')
    frames = []
    for table in tables:
        frames.append(pd.read_html(table.get_attribute('innerHTML'),index_col=0)[0])
    item_specs = pd.concat(frames).T
    item_specs['URL'] = url
    specs.append(item_specs)

    driver.close()
    driver.switch_to_window(driver.window_handles[0])
specs = pd.concat(specs)
specs.to_csv('specs.csv')