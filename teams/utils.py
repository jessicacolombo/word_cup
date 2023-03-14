from datetime import datetime


class NegativeTitlesError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidYearCupError(Exception):
    def __init__(self, message):
        self.message = message


class ImpossibleTitlesError(Exception):
    def __init__(self, message):
        self.message = message


def get_cup_years():
    this_year = datetime.now().year
    cup_years = []

    for year in range(1930, this_year, 4):
        cup_years.append(year)

    return cup_years


def has_valid_number_of_titles(cup_years, first_cup, declared_titles):
    valid_titles = len(cup_years) - cup_years.index(first_cup)

    return False if declared_titles > valid_titles else True


def data_processing(**kwargs):
    cup_years = get_cup_years()
    first_cup_year = datetime.strptime(kwargs["first_cup"], "%Y-%m-%d").year

    if kwargs["titles"] < 0:
        raise NegativeTitlesError("titles cannot be negative")

    if first_cup_year not in cup_years:
        raise InvalidYearCupError("there was no world cup this year")

    if not has_valid_number_of_titles(cup_years, first_cup_year, kwargs["titles"]):
        raise ImpossibleTitlesError("impossible to have more titles than disputed cups")
