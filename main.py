import requests
import secrets
import math


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
    f = open("schools.txt", "w")
    data: object
    for i, data in enumerate(all_data):
        str1 = (repr(i+1) + ") " + data['school.name'], " in ", data['school.city'] + ", " + data['school.state'])
        str2 = "Student Size in 2018: " + repr(data['2018.student.size'])
        str3 = "Student Size in 2017: " + repr(data['2017.student.size'])
        str4 = "Grads who earned > 150% of the poverty threshold after 3 years: " \
               + repr(data["2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line"])
        str5 = "No. of students in the 3-year repayment rate cohort in 2016: " \
               + repr(data["2016.repayment.3_yr_repayment.overall"])
        f.write("".join(str1) + "\n\t" + "".join(str2) + "\n\t" + "".join(str3) + "\n\t"
                + "".join(str4) + "\n\t" + "".join(str5) + "\n\n")
        f.close()


if __name__ == '__main__':
    main()
