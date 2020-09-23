from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path

chrome_options = Options()  
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

try:
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.loads(f.read())
except  FileNotFoundError:
    print('No data.json file!')
    exit(-1)

email_user = data['gmail']['user']
email_password = data['gmail']['password']
urls = data['kreta']

email_data = ''
html = Template(Path('index.html').read_text())

wd = webdriver.Chrome(options=chrome_options)
for k, v in urls.items():
    print(k,'adatgyűjtés.')
    wd.get(v[0])
    wd.find_element_by_id('UserName').send_keys(v[1])
    wd.find_element_by_id('Password').send_keys(v[2])
    wd.find_element_by_id('btnSubmit').click()
    sleep(2)

    tabla = wd.find_element_by_id('legutobbiErtekelesek')
    jegyek = tabla.find_elements_by_class_name('k-link')

    tabla = wd.find_element_by_id('legutobbiMulasztasok')
    mulasztasok = tabla.find_elements_by_class_name('k-link')
    email_data += f'<h2>{k}</h2>'
    email_data += f'<h3>JEGYEK</h3>'
    for jegy in jegyek:
        t = jegy.text.split('\n')
        email_data += f'<code>{t[0]} - {t[1]}\t - {t[2]}</code><br/>'

    email_data += f'<h3>HIÁNYZÁSOK</h3>'
    for mulasztas in mulasztasok:
        m = mulasztas.text.split('\n')
        try:
            email_data += f'<code>{m[0]}, {m[3]} -> {m[4]}</code><br/>'
        except:
            email_data += f'<code>{m[0]}</code><br/>'

    tabla = wd.find_element_by_id('legutobbiFeljegyzesek')
    uzenet = tabla.find_elements_by_class_name('k-link')
    if not 'Nincsenek' in uzenet[0].text:
        tabla.click()
        sleep(2)
        uzenet = wd.find_element_by_xpath('//*[@id="InformaciokFeljegyzesekGrid"]/div[2]/div[1]/table/tbody/tr/td[6]/span')
        email_data += f'<h3>ELEKTRONIKUS ÜZENET</h3>'
        email_data += f'<code>{uzenet.text}</code><br/>'
        
wd.close()
wd.quit()

print('Email küldés.')

email = EmailMessage()
email['from'] = email_user
email['to'] = 'l.molnar@outlook.hu'
email['cc'] = 'bona.eniko@outlook.com'
email['subject'] = 'Kréta jegyek'

email.set_content(html.substitute(data=email_data), 'html')

with smtplib.SMTP(host='SMTP.office365.com', port=587) as s:
    s.ehlo()
    s.starttls()
    s.login(email_user, email_password)
    s.send_message(email)
    s.quit()

print('Kész!')    