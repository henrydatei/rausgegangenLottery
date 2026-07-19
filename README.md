# Lottery Bot for rausgegangen.de
rausgegangen.de offers Lotterys (Gewinnspiele) for tickets for events. This bot aims to increase you chances by using multiple accounts.

## Quick Start
- Clone the repo
- install requests (if not already done)
- create a file `accounts.txt` with the following content:
```
email:password
email2:password2
email3:password3
email4:password4
```
Add as many accounts as you want. The first account is the main account and all following accounts will be participating in the same lotteries as the main account.
- run `bot.py`

Actually you can run the bot multiple times. It seems to be that you can participate in a lottery multiple times, but I have no idea if this is really increasing your chances. At least you get multiple emails stating that you participated, but it might be the case that they filter duplicate accounts right before the draw of the lottery. It seems to be that only the app prevents you from participating multiple times.

## Create more accounts

**This method is already fixed!! Currently in the look for a new one**

I have a script locally that can create accounts but there are some things in it which I don't want to share publicly. I suggest using Googlemail oder Microsoft's live as an email provider because the have a unique feature: If your email is `example@gmail.com` than, instead of entering this mail, you can enter `example+rausgegangen1@gmail.com` as email. The key thing is: whatever is send to `example+rausgegangen1@gmail.com` will land in your inbox and you can apply filter rules etc to sort your email. You don't have to register that in Googlemail, it just works out of the box. [Source](https://www.streak.com/post/gmail-plus-addressing-trick) 

[Works with dots in a similar way](https://support.google.com/mail/answer/7436150)

With that you can create a simple script for creating accounts:
```python
import requests
import logging
import random
import string
import time

logging.basicConfig(level=logging.INFO)

def create_account(username: str, email: str, password: str) -> bool:
    """
    Creates a new account on the service using the provided email and password.
    Returns True if account creation is successful, otherwise False.
    """
    create_account_url = "https://api.rausgegangen.de/rausgegangen/api/v2/user/signup"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Rausgegangen/233 CFNetwork/3826.600.41 Darwin/24.6.0"
    }
    payload = {
        "username": username,
        "email": email,
        "password": password,
        "tosAccepted": True,
        "newsletterAccepted": False,
        "mergeDataAccepted": False,
        "city": "",
        "deviceType": "ios"
    }
    response = requests.post(create_account_url, json=payload, headers=headers)
    if response.status_code == 200:
        logging.info(f"Created account with email: {email}, username: {username}, password: {password}")
        return True
    else:
        logging.error(f"Account creation failed for email: {email}. Error: {response.text}")
        return False

def generate_random_username_password() -> tuple[str, str]:
    """
    Generates a random username and password for account creation.
    Returns a tuple of (username, password).
    """

    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    return username, password

if __name__ == "__main__":
    # base google mail prefix
    mail_prefix = "example+rausgegangen"

    # Check if accounts.txt exists, if not create it
    try:
        with open("accounts.txt", "r") as f:
            pass
    except FileNotFoundError:
        logging.info("accounts.txt not found. Creating a new one.")
        with open("accounts.txt", "w") as f:
            pass

    for number in range(20, 101):
        username, password = generate_random_username_password()
        email = f"{mail_prefix}{number}@gmail.com"
        success = create_account(username, email, password)
        if success:
            # Append to accounts.txt
            with open("accounts.txt", "a") as f:
                f.write(f"{email}:{password}\n")
            logging.info(f"Account details saved to accounts.txt: {email}:{password}")
        else:
            logging.error(f"Failed to create account with email: {email}")
        time.sleep(20)  # Sleep to avoid hitting rate limits
```

You can add more features like automatically add it to your password manager, etc.