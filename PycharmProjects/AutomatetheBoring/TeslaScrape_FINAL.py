## Future Versions: Add in detail about the vehicle to the notification. For Example: ' New Long-Range AWD listed @ price XXXXXX'

import os, bs4, shutil, re, requests, webbrowser, shelve
from selenium import webdriver

os.chdir('/Users/BeNz/Library/Mobile Documents/com~apple~CloudDocs/PycharmProjects/AutomatetheBoring')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
path_to_chromedriver = '/Users/BeNz/PycharmProjects/venv/lib/python3.7/site-packages/selenium/webdriver/chrome/chromedriver'  # change path as needed
browser = webdriver.Chrome(executable_path=path_to_chromedriver)

for i in [90029,95042,85001,75001,89118,97214,84044]:
    print(str(i))

## Establishing Selenium
    url = 'https://www.tesla.com/inventory/new/m3?distance=200&arrangeby=plh&zip=' + str(i) + '&range=0'
    browser.get(url)
    browser.set_window_size(1120, 550)

## Looping through all possible vehicles by associated VINS on the page
    loop = 0
    newinventory = []
    vinsnotified = shelve.open('oldinventory')

    for k in range(1,20):
        xpath = "//*[@id='iso-container']/div/div[1]/div[2]/div[2]/span/div/div[" + str(k) + "]"

        try:
            browser.find_element_by_xpath(xpath) ## this statement is incorrect. It should check for an error
        except:
            break

        path = browser.find_element_by_xpath(xpath)  ## this statement is incorrect. It should check for an error
        class1 = path.get_attribute('class')
        regex1 = re.compile(r'\w{17}')
        almostVIN = regex1.search(class1)

        if almostVIN == None:
            break
        else:
            VIN = almostVIN.group()

        if VIN in vinsnotified['VINS']:
            continue
        else:
            newinventory.append(VIN)

        print(newinventory)



#Scraping the specific Vehicle Data
        for VIN1 in newinventory:
            vin_url = 'https://www.tesla.com/new/' + VIN1
            browser.get(vin_url)

            try:
                browser.find_element_by_id('inventory-details-app-root')  ## this statement is incorrect. It should check for an error
            except:
                break

            path = browser.find_element_by_id('inventory-details-app-root')

            #REGEX List
            regexprice = re.compile(r'\$\d{2},\d{3}')
            regexmodel = re.compile(r'(\n)(.*)(\n)')
            #regexfeatures = re.compile(r'(Key Features)\\n(.*)\*')
            regexcolor = re.compile(r'(Midnight Silver Metallic Paint|Pearl White Paint|Solid Black Paint|Deep Blue Metallic Paint|Red Multi-Coat Paint)')

            foundmodel = regexmodel.search(path.text)
            model = foundmodel.group(2)

            foundprice = regexprice.search(path.text)
            price = foundprice.group()

            #foundfeatures = regexfeatures.search(path.text)
            #features = foundfeatures.group(2)

            foundcolor = regexcolor.search(path.text)
            color = foundcolor.group()



#Notifier
            print('Notification Incoming')
            zip = i
            notification = {}
            notification['value1'] = zip  ##zipcode should be extracted from above
            print(vin_url)
            notification['value2'] = vin_url  ## this should also be extracted from the above
            notification['value3'] = model + ' | ' + price + ' | ' + color
            requests.post('https://maker.ifttt.com/trigger/TeslaScrape/with/key/eZlP4Tz4ksoGfUk157ATQSdiWJlJPfjz04kPLMdgSWT',data=notification)

    if newinventory == []:
        print('No New Inventory')
        continue

## If new VINS, add them to the shelved file with all existing VINS
    else:
        print('Stock Reported')

    vinsnotified['VINS'] += newinventory
    vinsnotified.close()

## Post a notification through IFTTT
    #zip = i
    #notification = {}
    #notification['value1'] = zip ##zipcode should be extracted from above
    #vin_url = 'https://www.tesla.com/new/' + VIN
    #print(vin_url)
    #notification['value2'] = vin_url ## this should also be extracted from the above
    #requests.post('https://maker.ifttt.com/trigger/TeslaScrape/with/key/eZlP4Tz4ksoGfUk157ATQSdiWJlJPfjz04kPLMdgSWT', data=notification)

browser.close()