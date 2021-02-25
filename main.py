import requests
import secrets
import math
import sqlite3
import pandas as pd
from pandas.tests.io.excel.test_openpyxl import openpyxl
import os
from typing import Tuple


def school_data(url: str):
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


def create_college_table(cursor: sqlite3.Cursor):
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


def create_jobs_table(cursor: sqlite3.Cursor):
    query1 = '''
                    CREATE TABLE IF NOT EXISTS jobs_data (
                        job_id INTEGER
                        , area_title TEXT
                        , o_group TEXT NOT NULL
                        , occ_title TEXT NOT NULL
                        , tot_emp INTEGER
                        , h_pct25 NUMERIC
                        , a_pct25 NUMERIC
                        , PRIMARY KEY (job_id, area_title)
                    );
                    '''
    cursor.execute(query1)


def add_school_data(cursor: sqlite3.Cursor):
    url = 'https://api.data.gov/ed/collegescorecard/v1/schools.json?' \
          'school.degrees_awarded.predominant=2,3'
    all_data = school_data(url)
    try:
        for data in all_data:
            cursor.execute('''INSERT INTO college_data(id, name,city,state,size_2019,size_2018,earning_grads,grads_repay_3yrs)
                        VALUES(?,?,?,?,?,?,?,?)''', data)
    except Exception as e:
        print(e)


def add_jobs_data(cursor: sqlite3.Cursor):
    all_data = jobs_data()
    try:
        for data in all_data:
            cursor.execute('''INSERT INTO jobs_data(job_id, area_title, o_group, occ_title, tot_emp, h_pct25, a_pct25)
                        VALUES(?,?,?,?,?,?,?)''', data)
    except Exception as e:
        print(e)


def jobs_data():
    this_folder = os.path.dirname(os.path.abspath(__file__))
    file_to_open = os.path.join(this_folder, "state_M2019_dl.xlsx")
    wb = pd.read_excel(file_to_open, sheet_name='State_M2019_dl', index_col=0, engine=openpyxl)
    df = pd.DataFrame(wb)
    data = df[['occ_code', 'area_title', 'o_group', 'occ_title', 'tot_emp', 'h_pct25', 'a_pct25']].query(
        'o_group == "major"')
    all_data = []
    for i in range(len(data)):
        all_data.append(data.iloc[i].values.tolist())
    return all_data


def main():
    conn, cursor = create_connection('college_data.sqlite')
    create_college_table(cursor)
    create_jobs_table(cursor)
    add_school_data(cursor)
    add_jobs_data(cursor)
    close_db(conn)


if __name__ == '__main__':
    main()
