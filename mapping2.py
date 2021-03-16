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
    sqlquery = '''SELECT State, round(avg(grads_repay_cohort)*100, 2)||'%' AS 'Declining Balance',
round(AVG(a_pct25),2) AS Wage, CAST(AVG(grads_repay_cohort)*AVG(a_pct25) AS INT) AS Income FROM jobs_data
inner join state_lookup ON jobs_data.area_title = state_lookup.state_name
inner join college_data ON state_lookup.state_abbrev = college_data.state
GROUP BY state;'''
    result = cur.execute(sqlquery)
    rows = result.fetchall()
    data = []
    for row in rows:
        data.append(row)

    df = DataFrame(data, columns=['State', 'Declining Balance', 'Wage', 'Income'])
    df["id"] = df['State'].apply(lambda x: state_id_map[x])
    connection.close()

    fig = px.choropleth(
        df,
        locations="id",
        geojson=usa,
        color="Income",
        scope='usa',
        hover_name="State",
        hover_data=['Declining Balance', 'Wage', 'Income'],
        title="Income After College Debt",
    )
    fig.write_html('tmp2.html', auto_open=True)


if __name__ == '__main__':
    main()
