import bs4
import re
from selenium import webdriver


def quoting(text: str) -> str:
    return f'\"{text}\"'


options = webdriver.FirefoxOptions()
options.headless = True

driver = webdriver.Firefox(executable_path='./geckodriver', options=options)

driver.get(r'http://wspinanie.pl/topo2/page,wyszukiwarka.html')
driver.find_element_by_css_selector(r'#szukajKraj > option:nth-child(2)').click()
driver.find_element_by_css_selector(r'input.image:nth-child(1)').click()

count_list = []
for nr in range(30, 50):
    if nr in range(30, 40):
        count_list.append(rf'\{nr} ')
    else:
        count_list.append(rf'\31 {nr - 40}')

for page in range(1, 359):

    driver.find_element_by_css_selector('#form_limit > select').click()
    driver.find_element_by_css_selector(rf"#form_limit > select > option:nth-child({page})").click()

    source = driver.page_source
    soup = bs4.BeautifulSoup(source, "html.parser")

    for index, count in enumerate(count_list):

        droga = soup.select(rf'#{count} > td:nth-child(1) > a')
        droga = droga[0].text.strip("<>\n\t ")
        droga = quoting(droga)

        formacja = soup.select(rf'#{count} > td.sciezka > a:nth-child(1)')
        formacja = formacja[0].text.strip("<>\n\t ")
        formacja = quoting(formacja)

        skala = soup.select(rf'#{count} > td.sciezka > a:nth-child(3)')
        skala = skala[0].text.strip("<>\n\t ")
        skala = quoting(skala)

        wycena = soup.select(rf'#{count} > td:nth-child(3)')
        wycena = wycena[0].text.strip("<>\n\t ")

        tabelka = soup.select(rf'#widok{index} > div > table > tbody > tr > td:nth-child(5)')
        tabelka = tabelka[0].text.strip("<>\n\t ")

        dlugosc = re.search('(\d)m', tabelka)[1]

        ksztalt = soup.select(rf'#widok{index} > div > table > tbody > tr > td:nth-child(2)')
        ksztalt = ksztalt[0].text.strip("<>\n\t ")

        ubezpieczona = soup.select(rf'#widok{index} > div > table > tbody > tr > td:nth-child(1)')
        ubezpieczona = ubezpieczona[0].text.strip("<>\n\t ")

        print(f'{droga},{formacja},{skala},{dlugosc},{wycena},{ksztalt},{ubezpieczona}')

        with open('data.csv', 'a') as data:
            print(f'{droga},{formacja},{skala},{dlugosc},{wycena},{ksztalt},{ubezpieczona}', file=data)
