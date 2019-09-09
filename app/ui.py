"""
ui.py is a lightweight interface for creating a PyperCard application
Since the UI wasn't high priority on this, I didn't spend a lot of time on 
this section.
"""

from pypercard import Card, CardApp
import urllib


def create_user_cards(user_list: list):
    """
    Method for creating a stack of cards to render in the application
  
    Parameters: 
    user_list (list): A list of User objects
  
    Returns: 
    stack(list): On success, returns a list of Pypercard Cards.
    On failure, logs error output
    """

    stack = []
    len_users = len(user_list)
    for i in range(len_users):
        user = user_list[i]
        img_file = f"./img/image{i}.jpg"
        urllib.request.urlretrieve(user.photo, img_file)

        buttons = (
            [{"label": "Next", "target": f"Card{i+1}"}] if i < len_users - 1 else None
        )

        text = f"Name: {user.name.capitalize()}\nAge: {user.age}\nBio: {user.bio}\n{user.number}"
        card = Card(
            title=f"Card{i}",
            background=img_file,
            text=text,
            text_color="whitesmoke",
            buttons=buttons,
            text_size=25,
        )
        stack.append(card)
    return stack


def build_and_run_app(user_list: list):
    """
    Method for orchestrating application run
  
    Parameters: 
    user_list (list): A list of Users to expose through the app
  
    Returns:
    No return value, just launches application
    """

    stack = create_user_cards(user_list)
    app = CardApp(stack=stack)
    app.run()
