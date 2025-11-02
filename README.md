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

## How the lotteries work
Currently under investigation. I need more events with lotteries and analyse them. I have seen to events with lotteries, these are the raw data:

Mantra Halloween
- event id a0d16535-e64b-41bf-8be0-7d9edc7daf60
- subevent id: f6b81e1c-c9df-40ef-91ed-4a69db398bc7
- start 1.11.2025 23:00
- lottery id: 2055889f-9d99-4f11-96f6-66de427c7b42
- draw: 31.10.2025 22:00 (25h before)
- time to claim the win: 1.11.2025 11:00 (12h before)
- link to claim the win: https://rausgegangen.de/lotteries/guestlist-slot/J2Z1XI0y3hStCUxEFIJh7Evk
- if not claimed, mail to other participants: 1.11.2025 11:00 (12h before)
- link: https://rausgegangen.de/lotteries/2055889f-9d99-4f11-96f6-66de427c7b42


SPOOKY JUICE I +21 Edition
- event id: 7f89f27b-e75c-4050-be06-de84dfbd4c4c
- subevent id: e6c329b0-92f4-49ea-b7ea-c6a7fb2ccc23
- start 1.11.2025 22:00
- lottery id: 7ae1c536-749d-48bb-9ea1-598e76d5e6cd
- draw: 31-10.2025 19:00 (27h before)
- time to claim the win: ?
- link to claim the win: ?
- if not claimed, mail to other participants: ?
- link: ?

**Learnings:**
- Lottery draws are around 24h before the event
- time to claim the win is always 12h before the event and right after that, if a ticket is not claimed, the link is send out to all participants
- this email doesn't come at the same time for all participants (I've seen arriving times from 11:02 to 11:10 for my accounts), making first come first serve unfair
- the link is predictable: https://rausgegangen.de/lotteries/{lottery_id} -> maybe a script trying to access this link every second?
- the link opens the browser (not the app on the phone) but I have no idea what is happening afterwards. If you are to late, then you get forwarded to the event page
- the link to claim the ticket is not predictable (it would be really embarresing if you could claim the tickets even if you didn't win just by predicting the link)
- sometimes every winner claims its price, so no mail is send

## Create more accounts
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