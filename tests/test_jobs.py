import main
import secrets
import sqlite3


def test_num_entries():
    url = f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3" \
          f"&api_key={secrets.api_key}&per_page=1"
    result = main.total_pages(url)
    assert result > 1000


def test_database():
    main.main()
    db1 = 'test.sqlite'
    db2 = 'college_data.sqlite'
    conn1 = sqlite3.connect(db1)
    conn2 = sqlite3.connect(db2)
    cur1 = conn1.cursor()
    cur2 = conn2.cursor()
    main.create_college_table(cur1)
    main.create_jobs_table(cur1)
    main.add_school_data(cur1)
    main.add_jobs_data(cur1)
    res1 = cur1.execute("""SELECT * FROM college_data""")
    res2 = cur2.execute("""SELECT * FROM college_data""")
    print("...Comparing Table: School_Data")
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
    print("...Comparison for College_Data is complete: all tables match")
    print("...Comparing Table: Jobs_Data")
    res3 = cur1.execute("""SELECT * FROM jobs_data""")
    res4 = cur2.execute("""SELECT * FROM jobs_data""")
    for row3 in res3:
        row4 = res4.fetchone()
        if row3 is not None and row4 is not None and (row3[0] == row4[0]):
            assert True
        else:
            assert False
            exit()
    print("....Done comparing table presence")
    print("....All tables match")
    main.close_db(conn1)
    main.close_db(conn2)


def test_num_states():
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(DISTINCT area_title) FROM jobs_data;")
    query = cursor.fetchone()[0]
    conn.close()
    assert query >= 50
