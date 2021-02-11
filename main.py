import requests
import secrets
import math
import psycopg2 as pg2


def school_data(url: str):
    all_data = []
    for page in range(total_pages(url)):
        full_url = f"{url}&api_key={secrets.api_key}&page={page}&fields=school.name,2018.student.size,2017.student.size," \
                   f"school.city,school.state,2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line," \
                   f"2016.repayment.3_yr_repayment.overall"
        response = requests.get(full_url)
        json_data = response.json()
        results = json_data['results']
        all_data.extend(results)
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
    result = math.ceil(total/pages)
    return result


def main():
    url = 'https://api.data.gov/ed/collegescorecard/v1/schools.json?' \
          'school.degrees_awarded.predominant=2,3'
    all_data = school_data(url)
    try:
        #modify the user and password fields if your server has a different config
        conn = pg2.connect(database='college', user='postgres', password='password')
        cur = conn.cursor()
        query1 = '''
                CREATE TABLE college_data (
                    id SERIAL PRIMARY KEY
                    , name varchar(250)
                    , city varchar(100)
                    , state varchar(5)
                    , size_2019 integer
                    , size_2018 integer
                    , earning_grads integer
                    , grads_repay_3yrs integer
                );
                '''
        cur.execute(query1)
        conn.commit()
        query1 = '''
                    INSERT INTO college_data(name,city,state,size_2019,size_2018,earning_grads,grads_repay_3yrs)
                    VALUES(%s,%s,%s,%s,%s,%s,%s);
                    '''
        for i, data in enumerate(all_data):
            cur.execute(query1, (data['school.name'], data['school.city'], data['school.state'], data['2018.student.size'],
                                 data['2017.student.size'], data["2017.earnings.3_yrs_after_completion."
                                                                 "overall_count_over_poverty_line"],
                                 data["2016.repayment.3_yr_repayment.overall"]))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Can't connect. Invalid dbname, user or password")
        print(e)


if __name__ == '__main__':
    main()
