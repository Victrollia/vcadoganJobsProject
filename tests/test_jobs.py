import main
import secrets
import sqlite3


def test_num_entries():
    url = f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3" \
          f"&api_key={secrets.api_key}&per_page=1"
    result = main.total_pages(url)
    assert result > 1000


def test_funcs(db1='test.sqlite', db2='college_data.sqlite'):
    conn1, cur1 = main.create_connection(db1)
    conn2, cur2 = main.create_connection(db2)
    main.create_college_table(cur1)
    main.create_jobs_table(cur1)
    main.add_school_data(cur1)
    main.add_jobs_data(cur1)
    entry_num(db1, db2, "college_data")
    entry_num(db1, db2, "jobs_data")
    main.close_db(conn1)
    main.close_db(conn2)


def test_database():
    main.main()
    sql1 = """SELECT * FROM college_data LIMIT 5;"""
    sql2 = """SELECT * FROM jobs_data LIMIT 5"""
    row_comparison('test.sqlite', 'college_data.sqlite', sql1, 'College_Data')
    row_comparison('test.sqlite', 'college_data.sqlite', sql2, 'Jobs_Data')


def row_comparison(db1, db2, query, table_name):
    conn1, cur1 = main.create_connection(db1)
    conn2, cur2 = main.create_connection(db2)
    res1 = cur1.execute(query)
    res2 = cur2.execute(query)
    print("...Comparing Table: " + table_name)
    for row1 in res1:
        row2 = res2.fetchone()
        print(row1)
        print(row2)
        if row1 is not None and row2 is not None and (row1[0] == row2[0]):
            print("........Tables Match:" + str(row1[0]))
            assert True
        else:
            if row1 is not None and row1[0] is not None:
                print("!!!!!!!!PROBLEM " + db1 + " is missing Table:" + str(row1[0]))
                assert False
            else:
                print("!!!!!!!!PROBLEM " + db2 + " is missing Table:" + str(row2[0]))
                assert False
            exit()
    print("...Completed table comparison for " + table_name + ": all tables match")
    main.close_db(conn1)
    main.close_db(conn2)


def entry_num(db1, db2, table_name):
    result1 = exec_sql(db1, table_name)
    result2 = exec_sql(db2, table_name)
    assert result1 == result2


def exec_sql(filename, table_name):
    conn, cursor = main.create_connection(filename)
    cursor.execute("SELECT COUNT(*) FROM " + table_name)
    query = cursor.fetchone()[0]
    main.close_db(conn)
    return query


def test_num_states():
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT area_title) FROM jobs_data;")
    query = cursor.fetchone()[0]
    conn.close()
    assert query >= 50
