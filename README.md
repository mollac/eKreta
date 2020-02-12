# eKreta
Új jegyek és mulasztások a eKréta naplóból és azok küldése email-ben. :)
 
## Értelemszerűen ki kell tölteni a data.json file-t. ##

```
{
  "kreta":{
    "1. gyerek":[
      "https://klik.....e-kreta.hu",
      "azonosító",
      "jelszó"
    ],
    "2. gyerek":[
      "https:/....e-kreta.hu",
      "azonosító",
      "jelszó"
    ]
  },
  "gmail":{
    "user":"küldő email cím",
    "password":"smtp jelszó"
  }
}
```
## A kreta.py programban beállítani az smtp szerver címét és portját! ##
```
with smtplib.SMTP(host='smtp szerver címe => port szám', port=587) as s:
```
## A címzetteket beállítani a kreta.py-ban. ##
```
email = EmailMessage()
email['from'] = email_user
email['to'] = 'cimzett1@email.com'
email['cc'] = 'cimzett2@email.com'
email['subject'] = 'Kréta jegyek'
```
