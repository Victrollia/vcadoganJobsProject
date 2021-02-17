import requests
import secrets
import math
import sqlite3
from sqlite3 import Error
from typing import Tuple


def school_data(url: str):
    c_list = []
    all_data = []
    index = 1
    for page in range(total_pages(url)):
        full_url = f"{url}&api_key={secrets.api_key}&page={page}&fields=school.name,2018.student.size,2017.student.size," \
                   f"school.city,school.state,2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line," \
                   f"2016.repayment.3_yr_repayment.overall"
        response = requests.get(full_url)
        json_data = response.json()
        results = json_data['results']
        for data in results:
            all_data.append(
                [index, data['school.name'], data['school.city'], data['school.state'], data['2018.student.size'],
                 data['2017.student.size'], data["2017.earnings.3_yrs_after_completion."
                                                 "overall_count_over_poverty_line"],
                 data["2016.repayment.3_yr_repayment.overall"]])
            index += 1
        if response.status_code != 200:
            print(response.text)
            return []
    return all_data


def total_pages(url: str):
    res = requests.get(f"{url}&api_key={secrets.api_key}")
    r = res.json()
    metadata = r.get('metadata')
    total = metadata['total']
    pages = metadata['per_page']
    result = math.ceil(total / pages)
    return result


def create_connection(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    conn = sqlite3.connect('college_data.sqlite')
    cursor = conn.cursor()
    return conn, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()
    connection.close()


def create_tables(cursor: sqlite3.Cursor):
    query1 = '''
                    CREATE TABLE IF NOT EXISTS college_data (
                        id INTEGER PRIMARY KEY
                        , name TEXT NOT NULL
                        , city TEXT
                        , state TEXT
                        , size_2019 INTEGER
                        , size_2018 INTEGER
                        , earning_grads INTEGER
                        , grads_repay_3yrs INTEGER
                    );
                    '''
    cursor.execute(query1)


def add_data(cursor: sqlite3.Cursor):
    url = 'https://api.data.gov/ed/collegescorecard/v1/schools.json?' \
          'school.degrees_awarded.predominant=2,3'
    all_data = school_data(url)
    try:
        for data in all_data:
            cursor.execute('''INSERT INTO college_data(id, name,city,state,size_2019,size_2018,earning_grads,grads_repay_3yrs)
                        VALUES(?,?,?,?,?,?,?,?)''', data)
    except Exception as e:
        print(e)


def main():
    conn, cursor = create_connection('college_data.sqlite')
    create_tables(cursor)
    add_data(cursor)
    close_db(conn)


if __name__ == '__main__':
    main()
