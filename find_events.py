import requests
import logging

from bot import open_or_create_accounts_txt, login, get_user_info, get_subevent_details, lottery_participate

def get_events_with_lotteries(token: str) -> dict:
    """
    Fetches details of events with lotteries using the provided authentication token.
    Returns a dictionary with event details.
    """
    details_url = f"https://api.rausgegangen.de/rausgegangen/api/v2/geospatial-search?city=frankfurt&geospatial_query_type=CITY&is_free_b=false&has_lottery_b=true&is_ticketing_b=false&rows=24&lat=50.11090895495324&lng=8.682125269925267&radius=5000"
    headers = {
        "Authorization": f"Token {token}"
    }
    response = requests.get(details_url, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        logging.info("Events with lotteries retrieved successfully.")
        return response.json()
    else:
        logging.error(f"Failed to retrieve events with lotteries. Error: {response.text}")
        return {}

WHITELIST_TAGS = ["party", "variete", "zaubershow", "zauberei"]
WHITELIST_CATEGORIES = ["Party", "Festivals", "Concerts & Music", "Feste & Festival"]

if __name__ == "__main__":
    accounts = open_or_create_accounts_txt()

    # get only main account
    if len(accounts) > 0:
        account_line = accounts[0]
        account, password = account_line.split(":")
        token = login(account, password)
        logging.debug(f"Token for account {account}: {token}")
        if token:
            user_info = get_user_info(token)
            logging.debug(f"User Info: {user_info}")

            participated_lotteries = user_info.get("participated_active_lotteries", [])
            logging.info(f"{len(participated_lotteries)} participated active lotteries found for account {account}.")
            logging.debug(f"Participated Active Lotteries: {participated_lotteries}")

            events_with_lotteries = get_events_with_lotteries(token).get("subevents", [])
            logging.info(f"{len(events_with_lotteries)} events with lotteries found.")
            logging.debug(f"Events with Lotteries: {events_with_lotteries}")
            for event in events_with_lotteries:
                subevent_id = event.get("id")
                if subevent_id:
                    subevent_details = get_subevent_details(token, subevent_id)
                    logging.debug(f"Details for Subevent ID {subevent_id}: {subevent_details}")
                    category = subevent_details.get("category", {}).lower()
                    tags = [tag.get("name", "").lower() for tag in subevent_details.get("tags", [])]
                    logging.debug(f"Subevent Name: {subevent_details.get('title', 'Unknown')}, Subevent ID {subevent_id} - Category: {category}, Tags: {tags}")
                    lottery_id = subevent_details.get("lottery_id", {})

                    if any(tag.lower() in WHITELIST_TAGS for tag in tags) or category in [category.lower() for category in WHITELIST_CATEGORIES]:
                        logging.info(f"Subevent {subevent_details.get('title', 'Unknown')} is whitelisted. Participating in lottery.")
                        if lottery_id not in participated_lotteries:
                            success = lottery_participate(token, lottery_id)
                            if success:
                                logging.info(f"Successfully participated in lottery for subevent {subevent_details.get('title', 'Unknown')}.")
                            else:
                                logging.error(f"Failed to participate in lottery for subevent {subevent_details.get('title', 'Unknown')}.")
                        else:
                            logging.info(f"Already participated in lottery for subevent {subevent_details.get('title', 'Unknown')}. Skipping.")
                    else:
                        logging.info(f"Subevent {subevent_details.get('title', 'Unknown')} is not whitelisted. Skipping lottery participation.")
                else:
                    logging.warning("Subevent ID not found in event data.")