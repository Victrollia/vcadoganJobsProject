import json
from pandas import DataFrame
import plotly.express as px
import plotly.io as pio
import sqlite3


def main():
    pio.renderers.default = 'firefox'
    usa = json.load(open("us_states.geojson", "r"))
    state_id_map = {}
    for feature in usa["features"]:
        feature["id"] = feature["properties"]["STATEFP"]
        state_id_map[feature["properties"]["abbr"]] = feature["id"]

    connection = sqlite3.connect("college_data.sqlite")
    cur = connection.cursor()
    sqlquery = '''SELECT state_abbrev, grads AS Grads, sum(tot_emp) AS Jobs, sum(tot_emp)/grads AS Rate FROM jobs_data
            inner join state_lookup ON jobs_data.area_title = state_lookup.state_name
            inner join (SELECT state, sum(size_2019)/4 AS grads
            FROM college_data GROUP BY state) grads ON state_lookup.state_abbrev = grads.state
            WHERE job_id NOT LIKE '3%'  AND job_id NOT LIKE '4%'
            AND state_abbrev NOT IN ('PR', 'GU', 'VI')
            GROUP BY area_title;'''
    result = cur.execute(sqlquery)
    rows = result.fetchall()
    data = []
    for row in rows:
        data.append(row)

    df = DataFrame(data, columns=['State', 'Grads', 'Jobs', 'Rate'])
    df["id"] = df['State'].apply(lambda x: state_id_map[x])
    connection.close()

    fig = px.choropleth(
        df,
        locations="id",
        geojson=usa,
        color="Rate",
        scope='usa',
        hover_name="State",
        hover_data=["Jobs", "Grads", "Rate"],
        title="Employment Rate",
    )
    fig.write_html('tmp.html', auto_open=True)


if __name__ == '__main__':
    main()




