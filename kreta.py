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
    sleep(3)

    tabla = wd.find_element_by_id('legutobbiErtekelesek')
    jegyek = tabla.find_elements_by_class_name('k-link')

    tabla = wd.find_element_by_id('legutobbiMulasztasok')
    mulasztasok = tabla.find_elements_by_class_name('k-link')
    
    email_data += f'<hr/><h2>JEGYEK/{k}</h2>'
    for jegy in jegyek:
        t = jegy.text.split('\n')
        email_data += f'<p>{t[2]:<14} <strong>{t[0]}</strong> {t[1]:<10}</p>'

    email_data += f'<hr/><h2>HIÁNYZÁSOK/{k}</h2>'
    for mulasztas in mulasztasok:
        m = mulasztas.text.split('\n')
        email_data += f'<p>{m[0]:<14} {m[3]:<10} {m[4]}</p>'
email_data += '<hr/'            
wd.close()

print('Email küldés.')

email = EmailMessage()
email['from'] = email_user
email['to'] = 'cimzett1@email.com'
email['cc'] = 'cimzett2@email.com'
email['subject'] = 'Kréta jegyek'

email.set_content(html.substitute(data=email_data), 'html')

with smtplib.SMTP(host='smtp szerver címe => port szám', port=587) as s:
    s.ehlo()
    s.starttls()
    s.login(email_user, email_password)
    s.send_message(email)
    s.quit()

print('Kész!')    