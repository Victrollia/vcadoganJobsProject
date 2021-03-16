import requests
import secrets
import math
import sqlite3
import pandas as pd
from typing import Tuple


def school_data(url: str):
    all_data = []
    index = 1
    for page in range(total_pages(url)):
        full_url = f"{url}&api_key={secrets.api_key}&page={page}&fields=school.name,2018.student.size,2017.student.size," \
                   f"school.city,school.state,2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line," \
                   f"2016.repayment.3_yr_repayment.overall,2016.repayment.repayment_cohort.3_year_declining_balance"
        response = requests.get(full_url)
        json_data = response.json()
        results = json_data['results']
        for data in results:
            all_data.append(
                [index, data['school.name'], data['school.city'], data['school.state'], data['2018.student.size'],
                 data['2017.student.size'], data["2017.earnings.3_yrs_after_completion."
                                                 "overall_count_over_poverty_line"],
                 data["2016.repayment.3_yr_repayment.overall"],
                 data["2016.repayment.repayment_cohort.3_year_declining_balance"]])
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
    conn = sqlite3.connect(filename)
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
                        , grads_repay_cohort NUMERIC
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


def add_school_data(db='college_data.sqlite'):
    conn, cursor = create_connection(db)
    create_college_table(cursor)
    url = 'https://api.data.gov/ed/collegescorecard/v1/schools.json?' \
          'school.degrees_awarded.predominant=2,3'
    all_data = school_data(url)
    try:
        for data in all_data:
            cursor.execute('''INSERT INTO college_data(id, name,city,state,size_2019,size_2018,earning_grads,
            grads_repay_3yrs,grads_repay_cohort)
                        VALUES(?,?,?,?,?,?,?,?,?)''', data)
    except Exception as e:
        print(e)
    create_state_lookup(cursor)
    close_db(conn)


def add_jobs_data(db='college_data.sqlite', filename="state_M2019_dl.xlsx"):
    conn, cursor = create_connection(db)
    create_jobs_table(cursor)
    if filename == "":
        pass
    else:
        all_data = jobs_data(filename)
        try:
            for data in all_data:
                cursor.execute('''INSERT INTO jobs_data(job_id, area_title, o_group, occ_title, tot_emp, h_pct25, a_pct25)
                            VALUES(?,?,?,?,?,?,?)''', data)
        except Exception as e:
            print(e)
    close_db(conn)


def jobs_data(filename="state_M2019_dl.xlsx"):
    wb = pd.read_excel(filename, index_col=0)
    df = pd.DataFrame(wb)
    data = df[['occ_code', 'area_title', 'o_group', 'occ_title', 'tot_emp', 'h_pct25', 'a_pct25']].query(
        'o_group == "major"')
    all_data = []
    for i in range(len(data)):
        all_data.append(data.iloc[i].values.tolist())
    return all_data


def drop_jobs_data():
    conn, cursor = create_connection('college_data.sqlite')
    create_jobs_table(cursor)
    cursor.execute('''DROP TABLE jobs_data''')
    close_db(conn)


def create_state_lookup(cursor: sqlite3.Cursor):
    query1 = '''
                    CREATE TABLE IF NOT EXISTS state_lookup (
                        state_id INTEGER PRIMARY KEY AUTOINCREMENT
                        , state_name TEXT
                        , state_abbrev TEXT
                    );
                    '''
    cursor.execute(query1)
    query1 = '''
    INSERT INTO state_lookup(state_name, state_abbrev)
VALUES ('Alabama', 'AL'), ('Alaska', 'AK'), ('Arizona', 'AZ'), ('Arkansas', 'AR'), ('California', 'CA'),
       ('Colorado', 'CO'), ('Connecticut', 'CT'), ('Delaware', 'DE'), ('District of Columbia', 'DC'),
       ('Florida', 'FL'), ('Georgia', 'GA'), ('Guam', 'GU'), ('Hawaii', 'HI'), ('Idaho', 'ID'),
       ('Illinois', 'IL'), ('Indiana', 'IN'), ('Iowa', 'IA'), ('Kansas', 'KS'), ('Kentucky', 'KY'),
       ('Louisiana', 'LA'), ('Maine', 'ME'), ('Maryland', 'MD'), ('Massachusetts', 'MA'), ('Michigan', 'MI'),
       ('Minnesota', 'MN'), ('Mississippi', 'MS'), ('Missouri', 'MO'), ('Montana', 'MT'), ('Nebraska', 'NE'), 
       ('Nevada', 'NV'), ('New Hampshire', 'NH'), ('New Jersey', 'NJ'), ('New Mexico', 'NM'), ('New York', 'NY'),
       ('North Carolina', 'NC'), ('North Dakota', 'ND'), ('Ohio', 'OH'), ('Oklahoma', 'OK'), ('Oregon', 'OR'),
       ('Pennsylvania', 'PA'), ('Puerto Rico', 'PR'), ('Rhode Island', 'RI'), ('South Carolina', 'SC'),
       ('South Dakota', 'SD'), ('Tennessee', 'TN'), ('Texas', 'TX'), ('Utah', 'UT'), ('Vermont', 'VT'),
       ('Virginia', 'VA'), ('Virgin Islands', 'VI'), ('Washington', 'WA'), ('West Virginia', 'WV'), ('Wisconsin', 'WI'),
       ('Wyoming', 'WY')'''
    cursor.execute(query1)


def main():
    add_school_data('college_data.sqlite')
    add_jobs_data('college_data.sqlite', "state_M2019_dl.xlsx")


if __name__ == '__main__':
    main()
