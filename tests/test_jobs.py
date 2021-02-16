import main
import secrets


def test_num_entries():
    url = f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded.predominant=2,3" \
          f"&api_key={secrets.api_key}&per_page=1"
    result = main.total_pages(url)
    assert result == 3203
