import psycopg2

def fetch():
    """ Connect to the PostgreSQL database server """
    conn = None
    employee_record= {}
    emp_activity_record = []
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(
            host="localhost",
            database="<dbName>",
            user="<userName>",
            password="<password>"
        )

        # create a cursor
        cur = conn.cursor()
        query_employees = "select * from employee"
        query_employee_activity = "select * from employee_activity"

        cur.execute(query_employees)
        employees = cur.fetchall()

        # get employee data
        for employee in employees:
            if employee not in employee_record:
                employee_record[employee[0]] = employee[1]

        #get employee acrivity
        cur.execute(query_employee_activity)
        emp_activity = cur.fetchall()
        for activity in emp_activity:

            employee = employee_record[activity[1]]
            emp_activity = activity[2]
            startTime = activity[3].strftime("%Y-%m-%d %I:%M %p")
            endTime = activity[4].strftime("%Y-%m-%d %I:%M %p")
            # calculate activity duration
            delta = activity[4] - activity[3]
            duration = divmod(delta.total_seconds(), 60)[0]

            emp_activity_record.append({
                                        "employee": employee,
                                        "emp_activity": emp_activity,
                                        "startTime": startTime,
                                        "endTime" : endTime,
                                        "duration" : duration
                                        }
                                       )

        cur.close()
        return emp_activity_record

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def combinePunches():
    employee_records = fetch()
    result = []
    employee= employee_records[0]['employee']
    activity = employee_records[0]['emp_activity']
    startTime = employee_records[0]['startTime']
    endTime = employee_records[0]['endTime']

    for i in range(1, len(employee_records)):
       if employee_records[i]['employee'] == employee:
           if employee_records[i]['emp_activity'] == activity:
               startTime = min(startTime, employee_records[i]['startTime'])
               endTime = max(endTime, employee_records[i]['endTime'])
           else:
               if employee_records[i]['duration'] <= 5:
                   startTime = min(startTime, employee_records[i]['startTime'])
                   endTime = max(endTime, employee_records[i]['endTime'])
               else:
                   result.append([employee, activity, startTime, endTime])
                   employee = employee_records[i]['employee']
                   activity = employee_records[i]['emp_activity']
                   startTime = employee_records[i]['startTime']
                   endTime = employee_records[i]['endTime']

       else:
           result.append([employee, activity, startTime, endTime])
           employee = employee_records[i]['employee']
           activity = employee_records[i]['emp_activity']
           startTime = employee_records[i]['startTime']
           endTime = employee_records[i]['endTime']
    result.append([employee, activity, startTime, endTime])

    for r in result:
        print(r)
if __name__ == '__main__':
    combinePunches()


