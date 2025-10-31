import requests
import logging

logging.basicConfig(level=logging.INFO)

def open_or_create_accounts_txt() -> list:
    """
    Opens the accounts.txt file and reads account credentials.
    If the file does not exist, it creates one with default credentials.
    Returns a list of account credentials.
    """
    try:
        with open("accounts.txt", "r") as file:
            accounts = file.readlines()
            if not accounts:
                logging.warning("accounts.txt is empty.")
                raise FileNotFoundError
    except FileNotFoundError:
        logging.info("accounts.txt not found. Creating a new one with default credentials.")
        with open("accounts.txt", "w") as file:
            file.write("default_account:default_password\n")
        with open("accounts.txt", "r") as file:
            accounts = file.readlines()
    logging.info(f"Loaded {len(accounts)} accounts from accounts.txt.")
    return [line.strip() for line in accounts]

def login(account, password) -> str | None:
    """
    Logs into the service using provided account credentials.
    Returns the authentication token if successful, otherwise None.
    """
    login_url = "https://api.rausgegangen.de/rausgegangen/api/v2/user/login"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Rausgegangen/233 CFNetwork/3826.600.41 Darwin/24.6.0"
    }
    payload = {
        "email": account,
        "password": password,
        "deviceType": "ios",
        "identifier": "D6A8295E-690F-44FA-B2C5-5C581BD5DA17"
    }
    response = requests.post(login_url, json=payload, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        logging.info(f"Login successful for account: {account}")
        return response.json()["token"]
    else:
        logging.error(f"Login failed for account: {account}. Error: {response.text}")
        return None
    
def get_user_info(token: str) -> dict:
    """
    Fetches user information using the provided authentication token.
    Returns a dictionary with user information.
    """
    user_info_url = "https://api.rausgegangen.de/rausgegangen/api/v2/user"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(user_info_url, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        logging.info("User information retrieved successfully.")
        return response.json()["user"]
    else:
        logging.error(f"Failed to retrieve user information. Error: {response.text}")
        return {}
    
def subevent_favourite(token: str, subevent_id: int) -> bool:
    """
    Marks a subevent as favorite using the provided authentication token and subevent ID.
    Returns True if successful, otherwise False.
    """
    favourite_url = "https://api.rausgegangen.de/rausgegangen/api/v2/subevent/favorite"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "id": subevent_id
    }
    response = requests.post(favourite_url, headers=headers, json=payload)
    response.raise_for_status()
    if response.status_code == 200:
        logging.info(f"Subevent {subevent_id} marked as favorite successfully.")
        return True
    else:
        logging.error(f"Failed to mark subevent {subevent_id} as favorite. Error: {response.text}")
        return False

def lottery_participate(token: str, lottery_id: int) -> bool:
    """
    Participates in the lottery using the provided authentication token.
    Returns True if successful, otherwise False.
    """
    lottery_url = "https://api.rausgegangen.de/rausgegangen/api/v2/lottery/participate"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "id": lottery_id
    }
    response = requests.post(lottery_url, headers=headers, json=payload)
    response.raise_for_status()
    if response.status_code == 200:
        logging.info("Lottery participation successful.")
        return True
    else:
        logging.error(f"Failed to participate in lottery. Error: {response.text}")
        return False
    
def get_subevent_details(token: str, subevent_id: int) -> dict:
    """
    Fetches details of a subevent using the provided authentication token and subevent ID.
    Returns a dictionary with subevent details.
    """
    details_url = f"https://api.rausgegangen.de/rausgegangen/api/v2/subevents/{subevent_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(details_url, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        logging.info(f"Subevent {subevent_id} details retrieved successfully.")
        return response.json()
    else:
        logging.error(f"Failed to retrieve subevent {subevent_id} details. Error: {response.text}")
        return {}
    
if __name__ == "__main__":
    accounts = open_or_create_accounts_txt()
    for account_line in accounts:
        account, password = account_line.split(":")
        token = login(account, password)
        if token:
            user_info = get_user_info(token)
            logging.info(f"User Info: {user_info}")
            lotteries = user_info.get("participated_active_lotteries", [])
            logging.info(f"Participated Lotteries: {lotteries}")