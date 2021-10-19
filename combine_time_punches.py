"""
assumptions made:
*made time punches based on the order of the id in employee_activity, i.e. data already in order

not sure why:
*order is different
*times seemed wrong so updated data
*William Packing     2021-01-24 10:30 AM     2021-01-24 3:00 PM, time gets consolidated like this

current result:
Name Activity Start Time End Time

Joe Picking 2021-01-24 9:05 AM 2021-01-24 10:00 AM

William Packing 2021-01-24 9:15 AM 2021-01-24 10:00 AM

Joe Packing 2021-01-24 11:00 AM 2021-01-24 11:45 AM

Lucy Packing 2021-01-24 11:30 AM 2021-01-24 12:20 PM

Joe Picking 2021-01-24 11:50 AM 2021-01-24 12:30 PM

William Packing 2021-01-24 10:30 AM 2021-01-24 1:00 PM

Lucy Picking 2021-01-24 12:25 PM 2021-01-24 2:00 PM

William Packing 2021-01-24 1:30 PM 2021-01-24 3:00 PM

William Picking 2021-01-24 3:05 PM 2021-01-24 5:00 PM

Joe Cleaning 2021-01-24 11:55 PM 2021-01-25 12:35 AM

"""
import psycopg2

conn = psycopg2.connect(dbname="postgres")
cur = conn.cursor()
cur.execute("select employee.name, employee_activity.activity_name, employee_activity.start_time, employee_activity.end_time"
            " from employee_activity join employee on employee_activity.employee_id = employee.id order by employee_activity.id;")
employee_activities = cur.fetchall()

time_punches = []
for activity in employee_activities:
    if time_punches and time_punches[-1][0] == activity[0]:
        # if same activities occur in a row and the time difference <= 5 minutes or the different activity is <= 5 minutes
        if (time_punches[-1][1] == activity[1] and (activity[2] - time_punches[-1][3]).seconds / 60 <= 5) \
                or (activity[3] - activity[2]).seconds / 60 <= 5:
            time_punches[-1][3] = activity[3]
        else:
            time_punches.append(list(activity))
    else:
        time_punches.append(list(activity))

print("Name", "Activity", "Start Time", "End Time", "\n")
for time_punch in time_punches:
    print(time_punch[0], time_punch[1], time_punch[2].strftime("%Y-%m-%d %-I:%M %p"), time_punch[3].strftime("%Y-%m-%d %-I:%M %p"), "\n")
