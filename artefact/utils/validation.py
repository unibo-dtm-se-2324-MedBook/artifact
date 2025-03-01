import re

class Validator():
    def __init__(self):
        pass

    def name_correctness(self, name):
        if not isinstance(name, str):
            return None
        if len(name.strip()) < 2:
            return None
        if not all(l.isalpha() or l.isspace() or l in "-'." for l in name):
            return None
        return True
    
    def surname_correctness(self, surname):
        if not isinstance(surname, str):
            return None
        if len(surname.strip()) < 2:
            return None
        if not all(l.isalpha() or l.isspace() or l in "-'." for l in surname):
            return None
        return True
        
    def email_correctness(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None
    
    def password_correctness(self, password):
        if not isinstance(password, str):
            return False
        if len(password) < 8:
            return False
        if not any(l.isdigit() for l in password):
            return False
        if not re.search("[@_!#$%^&*()<>?/\|}{~:]", password):
            return False
        return True 