import psycopg2
from EmployeeReportGenerator import EmployeeReportGenerator

# Hard-coding or even checking in this stuff is bad, but other approaches
# are specific to particulars of a deployment strategy
conn = psycopg2.connect(host="postgres", database="postgres", user="postgres", password="hopefullyaNISTcompliantpassword")
cur = conn.cursor()

# There are a lot of different possible approaches to seeding the DB
# but I'm just doing everything in a transaction here
cur.execute(open("data_load.sql", "r").read())

# No DI for me :(
EmployeeReportGenerator(cur).generate_report()



