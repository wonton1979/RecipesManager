import re
from PIL import Image


class InputValidate:
    def __init__(self, content: str) -> None:
        self.content: str = content

    def check_text_only(self) -> bool:
        if re.search(r"\w+", self.content) is not None:
            return True
        else:
            return False

    def check_number_only(self) -> bool:
        if self.content.isnumeric():
            return True
        else:
            return False

    def check_text_number(self) -> bool:
        if self.content.isalnum():
            return True
        else:
            return False

    def check_password(self) -> dict:
        password: str = self.content
        length_error: bool = not (8 < len(password) < 15)
        digit_error: bool = re.search(r"\d", password) is None
        uppercase_error: bool = re.search(r"[A-Z]", password) is None
        lowercase_error: bool = re.search(r"[a-z]", password) is None
        symbol_error: bool = re.search(r"[!#$%&*@]", password) is None
        password_ok: bool = not (length_error or digit_error or uppercase_error or lowercase_error or symbol_error)
        check_result: dict = {
            'password_ok': [password_ok, 'Password check failed !'],
            'length_error': [length_error, 'Your Password should between 8 and 15 characters long !'],
            'digit_error': [digit_error, 'Your Password should include at least one number !'],
            'uppercase_error': [uppercase_error, 'Your Password should include at least one Up case letter !'],
            'lowercase_error': [lowercase_error, 'Your Password should include at least one Lower case letter !'],
            'symbol_error': [symbol_error, 'Your Password should include at least special symbol from this list '
                                           '( !,#,$,%,&,*,@ ) !'],
        }
        return check_result

    def check_email(self) -> bool:
        email: str = self.content
        email_check_result: bool = re.search(r"^([a-z0-9.-_]+)@([a-z0-9_-])+\.[a-z]{2,10}(.[a-z]{2,8})?",
                                             email) is not None
        return email_check_result

    def check_picture(self) -> bool:
        picture: str = self.content
        try:
            Image.open(picture)
            return True
        except FileNotFoundError:
            return False
        except IsADirectoryError:
            return False
        except IOError:
            return False


