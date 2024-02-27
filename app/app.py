"""
App.py holds the main application code that communicates with the web service, 
creates and validates users, and exposes the five youngest users in a lightweight
Pypercard UI
"""

from functools import wraps
import requests

from db import insert_user, get_youngest_five
from errors import NonUSPhoneNumberException
from logger import logger
from models import User
from schemas import UserSchema
from ui import build_and_run_app


def get_request_json(url: str):
    """
    Method for interfacing with web services
  
    Parameters: 
    url (string): The location of the web service
  
    Returns: 
    json response: On success, returns JSON response. On failure, logs error output
    """
    try:
        request = requests.get(url)
        return request.json()
    except Exception as e:
        logger.error(f"Error response for {url}. {e}")


def get_all_user_url(func):
    """
    Wrapper method for building urls from the user_ids yielded from inner function
  
    Parameters: 
    func (function): The inner function that yields a generator with lists of ids
  
    Yields: 
    url: On success, returns urls for user details. On failure, logs error output
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        for l in func():
            for user_id in l:
                yield f"{config['URL_BASE']}detail/{user_id}"

    return wrapper


@get_all_user_url
def get_user_lists():
    """
    Method for getting all the lists of ids available on the web service
  
    Parameters: 
    None

    Yields: 
    generator of lists: Yields lists of ids until there is no token.
    On failure, logs error output
    """

    has_token = True
    list_url = config["LIST_URL"]

    while has_token:
        result = get_request_json(list_url)
        yield result["result"]

        if has_token := "token" in result:
            list_url = f"{config['LIST_URL']}?token={result['token']}"


def get_and_validate_user(user_detail: dict):
    """
    Method for getting user details and ensuring their validity
    At this time, the only criteria for a valid user is that the phone number,
    with punctuation stripped, is ten digits
  
    Parameters: 
    user_detail (dictionary): The json response of the web service 

    Returns: 
    user: On success, returns User object. On failure, logs error output
    """

    try:
        user = User(**user_detail)
        user_schema = UserSchema()
        return user
    except NonUSPhoneNumberException as ne:
        logger.error(f"{ne}.Valid US phone number required.")
    except Exception as e:
        logger.error(e)


def main(*args, **kwargs):
    """
    Main function for orchestration of the application
  
    Parameters: 
    Currently not using any parameters, but left the *args, **kwargs because in
    a production application, the config values would come from using ChainMap
    with configargparse by chaining config file, os.environ, and command line args
  
    Returns:
    Exit code on success or failure
    """
    for url in get_user_lists():
        if url:
            user_detail = get_request_json(url)
        if user_detail:
            user = get_and_validate_user(user_detail)
            if user:
                insert_user(user)
                logger.info(f"Inserted valid user {user}.")
            else:
                logger.info(f"Unable to insert user: {user_detail}")
    result = get_youngest_five()
    logger.info(
        f"Retrieved youngest five:{result}... Getting ready to launch application"
    )
    build_and_run_app(result)


if __name__ == "__main__":
    global config
    config = {
        "URL_BASE": "https://appsheettest1.azurewebsites.net/sample/",
        "LIST_URL": "https://appsheettest1.azurewebsites.net/sample/list/",
    }
    main()
