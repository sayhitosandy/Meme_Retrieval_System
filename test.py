from selenium import webdriver
from bs4 import BeautifulSoup

driver= webdriver.Chrome('C:\Program Files\chromedriver\chromedriver.exe')

# driver = webdriver.Firefox()


driver.get('https://www.instagram.com/9gag/')
soup = BeautifulSoup(driver.page_source)
driver.quit()

# for item in soup.select('._o6mpc'):
#    name = item.select('._kc4z2')[0].text
#    followers= item.select('._fd86t')[1].text
#    following = item.select('._fd86t')[2].text
#    print('Name :{}\nFollowers :{}\nFollowing :{}'.format(name,followers,following))

for x in soup.findAll('li', {'class':'photo'}):
    print x