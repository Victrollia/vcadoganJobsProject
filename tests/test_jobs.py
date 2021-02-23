import main
import secrets
import sqlite3


def test_num_entries():
    url = f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3" \
          f"&api_key={secrets.api_key}&per_page=1"
    result = main.total_pages(url)
    assert result > 1000


def test_database():
    conn = sqlite3.connect('test.sqlite')
    cursor = conn.cursor()
    main.create_college_table(cursor)
    main.add_school_data(cursor)
    main.close_db(conn)
    main.main()
    db1 = 'test.sqlite'
    db2 = 'college_data.sqlite'
    conn1 = sqlite3.connect(db1)
    conn2 = sqlite3.connect(db2)
    cur1 = conn1.cursor()
    cur2 = conn2.cursor()
    res1 = cur1.execute("""SELECT * FROM college_data""")
    res2 = cur2.execute("""SELECT * FROM college_data""")
    print("...Comparing Tables")
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
    print("....Done comparing table presence")
