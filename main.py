from collections import defaultdict
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas


def get_ru_spelling_years(number_years):
    if number_years % 100 >= 11 and number_years % 100 <= 14 or number_years % 10 == 0 or number_years % 10 >= 5:
        ru_spelling = 'лет'
    elif number_years % 10 == 1:
        ru_spelling = 'год'
    else:
        ru_spelling = 'года'
    return ru_spelling


def main():
    winery_start = 1920
    current_year = datetime.date.today().year
    number_years = current_year - winery_start
    ru_spelling_number_years = f'{number_years} {get_ru_spelling_years(number_years)}'

    excel_wines = pandas.read_excel('wine.xlsx', keep_default_na=False)
    wines = excel_wines.to_dict(orient='records')
    wine_groups = defaultdict(list)
    for wine in wines:
        wine_groups[wine["Категория"]].append(wine)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        ru_spelling_number_years=ru_spelling_number_years,
        wine_groups=wine_groups
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
