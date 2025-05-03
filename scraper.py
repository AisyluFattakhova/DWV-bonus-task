import requests
import pandas as pd


def get_raw_vacancies(search_term, amount):
    raw_vacancies_data = []
    url = 'https://api.hh.ru/vacancies'

    for i in range(amount // 10):
        params = {
            'text': search_term,
            'area': '113',  # Russia
            'per_page': '10',
            'page': i
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        raw_vacancies_data.append(response.json())
    return raw_vacancies_data


def extract_salary(vacancy):
    if vacancy['salary'] is not None:
        salary_from = vacancy['salary']['from']
        salary_to = vacancy['salary']['to']
    else:
        salary_from = None
        salary_to = None
    return salary_from, salary_to


def extract_address(vacancy):
    return vacancy['address']['raw'] if vacancy['address'] else None


def extract_information(search_term, amount):
    clear_data = []
    for elem in get_raw_vacancies(search_term, amount):
        for vacancy in elem['items']:
            salary_from, salary_to = extract_salary(vacancy)
            address_raw = extract_address(vacancy)
            clear_data.append([
                vacancy['name'],
                vacancy['employer']['name'],
                salary_from,
                salary_to,
                vacancy['area']['name'],
                address_raw,
                vacancy['apply_alternate_url'],
                vacancy['alternate_url'],
                vacancy['published_at'],
                vacancy['archived'],
                vacancy['snippet']['requirement'],
                vacancy['snippet']['responsibility']
            ])
    return clear_data


def save_to_excel(data, filename):
    columns = [
        'Job Title', 'Company Name', 'Salary From', 'Salary To', 'Region',
        'Full Address', 'Apply URL', 'Vacancy URL', 'Publication Time',
        'Archived', 'Requirements', 'Responsibilities'
    ]
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(filename, index=False)
    print(f'Successfully saved {len(data)} vacancies to {filename}')


if __name__ == '__main__':
    total_data = []
    while len(total_data) < 1500:
        print(f'\nCollected {len(total_data)} vacancies so far.')
        search_term = input('Enter job title to search (or type "exit" to stop): ')
        if search_term.lower() == 'exit':
            break
        try:
            batch_data = extract_information(search_term, 1000)
            if batch_data:
                total_data.extend(batch_data)
                print(f"Added {len(batch_data)} vacancies from '{search_term}'.")
            else:
                print(f"No vacancies found for '{search_term}'.")
        except Exception as e:
            print(f"Error: {e}")

    save_to_excel(total_data, 'collected_vacancies.xlsx')
