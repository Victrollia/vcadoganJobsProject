import main
import secrets
import sqlite3


def test_num_entries():
    # test to check if we get at least 1000 entries
    url = f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3" \
          f"&api_key={secrets.api_key}&per_page=1"
    result = main.total_pages(url)
    assert result > 1000


def test_funcs(db1='test.sqlite', db2='college_data.sqlite'):
    # test the functions from main such as creating tables and adding data to it
    conn1, cur1 = main.create_connection(db1)
    conn2, cur2 = main.create_connection(db2)
    main.create_college_table(cur1)
    main.create_jobs_table(cur1)
    main.add_school_data(cur1)
    main.add_jobs_data(cur1)
    main.close_db(conn1)
    main.close_db(conn2)


def test_database():
    # test to compare first 5 rows of each table and see if total number of entries match
    main.main()
    sql1 = """SELECT * FROM college_data LIMIT 5;"""
    sql2 = """SELECT * FROM jobs_data LIMIT 5"""
    db1 = 'test.sqlite'
    db2 = 'college_data.sqlite'
    row_comparison(db1, db2, sql1, 'College_Data')
    row_comparison(db1, db2, sql2, 'Jobs_Data')
    entry_num(db1, db2, "college_data;")
    entry_num(db1, db2, "jobs_data;")


def row_comparison(db1, db2, query, table_name):
    # created a separate function that compares rows to avoid repetition/reuse for 2 tables
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
    print("...Completed table comparison for " + table_name + ": all tables match")
    main.close_db(conn1)
    main.close_db(conn2)


def entry_num(db1, db2, table_name):
    # to avoid repetition/reuse for 2 tables, this function will take the output from another function and compare
    result1 = exec_sql(db1, table_name)
    result2 = exec_sql(db2, table_name)
    assert result1 == result2


def exec_sql(filename, table_name):
    # this function will return the number of entries from a table
    conn, cursor = main.create_connection(filename)
    cursor.execute("SELECT COUNT(*) FROM " + table_name)
    query = cursor.fetchone()[0]
    main.close_db(conn)
    return query


def test_num_states():
    # test to see if we get entries from all 50 states at least (in my case i also got data from territories)
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT area_title) FROM jobs_data;")
    query = cursor.fetchone()[0]
    conn.close()
    assert query >= 50
