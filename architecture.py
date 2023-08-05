universities = [
    {'name': 'Harvard', 'gpa_req': 4.18, 'sat_req': 1540},
    {'name': 'Stanford', 'gpa_req': 4.0, 'sat_req': 1500},
    {'name': 'MIT', 'gpa_req': 4.0, 'sat_req': 1490},
    {'name': 'Princeton', 'gpa_req': 3.9, 'sat_req': 1460},
    {'name': 'Caltech', 'gpa_req': 4.0, 'sat_req': 1550},
    {'name': 'Yale', 'gpa_req': 4.0, 'sat_req': 1460},
    {'name': 'Columbia', 'gpa_req': 3.91, 'sat_req': 1500},
    {'name': 'Duke', 'gpa_req': 3.9, 'sat_req': 1490},
    {'name': 'University of Pennsylvania', 'gpa_req': 3.9, 'sat_req': 1500},
    {'name': 'Johns Hopkins', 'gpa_req': 3.9, 'sat_req': 1470},
    {'name': 'Northwestern', 'gpa_req': 3.89, 'sat_req': 1490},
    {'name': 'Brown', 'gpa_req': 3.86, 'sat_req': 1480},
    {'name': 'Cornell', 'gpa_req': 3.9, 'sat_req': 1480},
    {'name': 'Dartmouth', 'gpa_req': 4.0, 'sat_req': 1490},
    {'name': 'Vanderbilt', 'gpa_req': 3.85, 'sat_req': 1480},
    {'name': 'Rice', 'gpa_req': 3.96, 'sat_req': 1500},
    {'name': 'Washington University in St. Louis', 'gpa_req': 3.9, 'sat_req': 1520},
    {'name': 'Georgetown', 'gpa_req': 3.89, 'sat_req': 1450},
    {'name': 'University of California - Berkeley', 'gpa_req': 3.87, 'sat_req': 1410},
    {'name': 'University of Chicago', 'gpa_req': 3.9, 'sat_req': 1500},
    {'name': 'University of Notre Dame', 'gpa_req': 3.87, 'sat_req': 1440},
    {'name': 'Emory University', 'gpa_req': 3.74, 'sat_req': 1410},
    {'name': 'University of Virginia', 'gpa_req': 4.0, 'sat_req': 1460},
    {'name': 'University of Michigan - Ann Arbor', 'gpa_req': 3.87, 'sat_req': 1420},
    {'name': 'University of North Carolina - Chapel Hill', 'gpa_req': 4.0, 'sat_req': 1400},
    {'name': 'University of Southern California', 'gpa_req': 3.85, 'sat_req': 1440},
    {'name': 'Tufts University', 'gpa_req': 3.83, 'sat_req': 1460}
]

def find_universities(gpa, sat):
    qualified_universities = []
    for university in universities:
        if gpa >= university['gpa_req'] and sat >= university['sat_req']:
            qualified_universities.append(university['name'])
    
    if len(qualified_universities) == 0:
        print("Sorry, you do not qualify for any of the universities.")
    else:
        print("The following universities match your criteria:")
        for university in qualified_universities:
            print(university)

user_gpa = float(input("Enter your GPA: "))
user_sat = int(input("Enter your SAT score: "))

find_universities(user_gpa, user_sat)

