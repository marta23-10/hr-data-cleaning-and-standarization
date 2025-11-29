import pandas as pd
import numpy as np
import random
import datetime

NUM_ROWS = 2500
OUTPUT_FILE = 'messy_hr_data.csv'

depts = ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'IT Support', 'Legal']
locations = ['New York, NY', 'San Francisco, CA', 'London, UK', 'Austin, TX', 'Remote', 'Berlin, DE']
job_levels = ['Junior', 'Mid', 'Senior', 'Lead', 'Manager', 'Director']
titles_base = ['Analyst', 'Developer', 'Specialist', 'Consultant', 'Officer']



def dirty_salary():
    base = random.randint(40, 180) * 1000
    r = random.random()
    if r < 0.5:
        return base
    elif r < 0.7:
        return f"${base:,}"
    elif r < 0.8:
        return f"{base / 1000:.0f}k"
    elif r < 0.9:
        return f"{base} USD"
    elif r < 0.95:
        return round(base / 12, 2)
    else:
        return np.nan


def dirty_phone():
    area = random.randint(100, 999)
    mid = random.randint(100, 999)
    end = random.randint(1000, 9999)
    r = random.random()
    if r < 0.4:
        return f"({area}) {mid}-{end}"
    elif r < 0.6:
        return f"{area}.{mid}.{end}"
    elif r < 0.8:
        return f"{area}-{mid}-{end}"
    elif r < 0.9:
        return f"+1 {area} {mid} {end}"
    else:
        return f"{area}{mid}{end}"


def dirty_date(year_start=2015):
    start = datetime.date(year_start, 1, 1)
    end = datetime.date(2024, 1, 1)
    days = (end - start).days
    d = start + datetime.timedelta(days=random.randrange(days))
    r = random.random()
    if r < 0.6:
        return d.strftime("%Y-%m-%d")
    elif r < 0.8:
        return d.strftime("%m/%d/%Y")
    elif r < 0.9:
        return d.strftime("%d.%m.%Y")
    elif r < 0.95:
        return "Pending"
    else:
        return np.nan


def messy_dept(dept_name):
    if random.random() > 0.15: return dept_name
    mapping = {
        'Engineering': ['Eng.', 'Engineering Dept', 'Enginering'],
        'Marketing': ['Mktg', 'Marketting'],
        'HR': ['Human Resources', 'H.R.'],
        'Finance': ['Fin.', 'Fiance'],
        'IT Support': ['IT', 'Tech Support']
    }
    return random.choice(mapping.get(dept_name, [dept_name]))


def dirty_skills():
    skills_pool = ['Python', 'Excel', 'SQL', 'Java', 'PowerBI', 'Management', 'Sales', 'Communication']

    selected = random.sample(skills_pool, k=random.randint(1, 3))

    dirty_selected = []
    for s in selected:
        if s == 'Excel' and random.random() > 0.7: s = 'Excell'
        if s == 'Python' and random.random() > 0.8: s = 'python'
        if s == 'PowerBI' and random.random() > 0.7: s = 'Power BI'
        dirty_selected.append(s)

    separator = random.choice([', ', ';', ' | ', ',', '/'])
    return separator.join(dirty_selected)


def dirty_education():
    options = [
        ('Bachelor', ['B.Sc', 'BS', 'Bachelors', 'Bachelor Degree']),
        ('Master', ['M.Sc', 'Masters', 'MBA', 'Master\'s']),
        ('PhD', ['Ph.D.', 'Doctorate']),
        ('High School', ['High School', 'H.S.', 'None'])
    ]
    base, variants = random.choice(options)
    if random.random() < 0.3:
        return random.choice(variants)
    return base


def dirty_ssn():
    part1 = f"{random.randint(100, 999)}"
    part2 = f"{random.randint(10, 99)}"
    part3 = f"{random.randint(1000, 9999)}"

    r = random.random()
    if r < 0.6:
        return f"{part1}-{part2}-{part3}"
    elif r < 0.8:
        return f"{part1}{part2}{part3}"
    elif r < 0.9:
        return f"{part1} {part2} {part3}"
    elif r < 0.95:
        return f"XXX-XX-{part3}"
    else:
        return np.nan


data = []

for i in range(NUM_ROWS):
    fname = random.choice(
        ['James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 'Michael', 'Linda', 'David', 'Elizabeth'])
    lname = random.choice(['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'])

    if random.random() < 0.1:
        full_name = f"{fname.upper()} {lname.lower()}"
    else:
        full_name = f"{fname} {lname}"

    lvl = random.choice(job_levels)
    role = random.choice(titles_base)
    job_title = f"{lvl} {role}" if random.random() < 0.6 else f"{role} - {lvl}"

    row = {
        'Employee_ID': f"EMP-{i:04d}",
        'Full_Name': full_name,
        'SSN': dirty_ssn(),
        'Department': messy_dept(random.choice(depts)),
        'Job_Title': job_title,
        'Salary': dirty_salary(),
        'Joining_Date': dirty_date(2018),
        'Education': dirty_education(),
        'Skills': dirty_skills(),
        'Performance_Rating': random.choice([1, 2, 3, 4, 5, '3', '4', 'A', 'B', np.nan]),
        'Email': f"{fname.lower()}.{lname.lower()}@company.com",
        'Phone': dirty_phone(),
        'Location': random.choice(locations)
    }
    data.append(row)

df = pd.DataFrame(data)

df = pd.concat([df, df.sample(n=40)], ignore_index=True)

for _ in range(15):
    df.loc[len(df)] = [np.nan] * len(df.columns)

df = df.sample(frac=1).reset_index(drop=True)

df.to_csv(OUTPUT_FILE, index=False)

print(f"Generated file: {OUTPUT_FILE}")
print(f"Number of rows: {len(df)}")
