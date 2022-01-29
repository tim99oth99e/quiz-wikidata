######################### This file is not used yet #########################
class Thing(object):
    def _init_(self, name = "Thing", options = []):
        self.name = name
        self.options = options

    def _str_(self) -> str:
        pass

class Conflict(object):
    def __init__(self,
                 name,
                 code,
                 location,
                 country,
                 participants,
                 start_date,
                 end_date) -> None:
        self.name = name
        self.code = code
        self.location = location
        self.country = country
        self.participants = participants
        self.start_date = start_date
        self.end_date = end_date

    def generate_question(self):
        pass


class City():
    def _init_(self, name, code) -> None:
        pass

class Country():
    def _init_(self, name, code) -> None:
        pass

class Building():
    def _init_(self, name, code) -> None:
        pass

class People():
    def _init_(self) -> None:
        pass

class  Actor():
    def _init_(self, name, code) -> None:
        pass

class Movie():
    def _init_(self, name, code) -> None:
        pass

class Musician():
    def _init_(self, name, code) -> None:
        pass

class Musichit():
    def _init_(self, name, code) -> None:
        pass
