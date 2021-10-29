from typing import Any, Dict, List
import psycopg2

def run_program():
    result: List[List[str]] = [["ID", "Name", "Activity", "Start Time", "End Time"]]
    connection = None
    try:
        connection = psycopg2.connect(database="grovedb")
        cur = connection.cursor()
        
        id_to_employee_map = get_employees(cur)
        for emp_id, emp_name in id_to_employee_map.items():
            activities: List[Dict[str, Any]] = get_emp_activities(emp_id, emp_name, cur)
            # we assume there're no overlapping activities for same employee
            result.extend(combine_punches(activities))
        cur.close()
        for r in result:
            print(r)
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()

""" Combine punches for an employee"""
def combine_punches(emp_activities: List[Dict[str, Any]]) -> List[List[str]]:
    result: List[List[str]] = []
    prev_activity: Dict[str, Any] = None
    index = 0
    # activities for an employee are cronological and non-overlapping
    while index < len(emp_activities):
        activity = emp_activities[index]
        if prev_activity == None:
            prev_activity = activity
        else:
            # combine condition -> if activity name matches and time between is <= 5 mins
            if (activity["activity_name"] == prev_activity["activity_name"] and (activity["start_time"] - prev_activity["end_time"]).seconds <= 300):
                prev_activity["end_time"] = activity["end_time"]
            else:
                if (activity["duration"] <= 300 and index < len(emp_activities) - 1 and emp_activities[index+1]["activity_name"] ==  prev_activity["activity_name"]):
                    prev_activity["end_time"] = emp_activities[index+1]["end_time"]
                    # skip the next activity since it's already been merged
                    index += 1
                else:
                    result.append([
                        prev_activity["id"], 
                        prev_activity["employee_name"], 
                        prev_activity["activity_name"], 
                        prev_activity["start_time"].strftime("%Y-%m-%d %I:%M %p"), 
                        prev_activity["end_time"].strftime("%Y-%m-%d %I:%M %p")
                    ])
                    prev_activity = activity
        index += 1
    
    # append last activity
    result.append([
        prev_activity["id"], 
        prev_activity["employee_name"], 
        prev_activity["activity_name"], 
        prev_activity["start_time"].strftime("%Y-%m-%d %I:%M %p"), 
        prev_activity["end_time"].strftime("%Y-%m-%d %I:%M %p")
    ])
    return result
    

def get_emp_activities(emp_id: int, emp_name: str, cur) -> List[Dict[str, Any]]:
    emp_activities: List[Dict[str, Any]] = []
    employee_activity_query = (
        'select * from employee_activity ' 
        f'WHERE employee_id = {emp_id} ' 
        'order by start_time'
    )
    cur.execute(employee_activity_query)
    activities: List[tuple] = cur.fetchall()
    for activity in activities:
        emp_activities.append({
            "id": activity[0],
            "employee_name": emp_name,
            "activity_name": activity[2],
            "start_time": activity[3],
            "end_time": activity[4],
            "duration": (activity[4] - activity[3]).seconds
        })
    return emp_activities

def get_employees(cur) -> Dict[int, str]:
    id_to_employee: Dict[int, str] = {}
    employee_query: str = "select * from employee"
    cur.execute(employee_query)
    employees: List[tuple] = cur.fetchall()
    for employee in employees:
        id_to_employee[employee[0]] = employee[1]
    return id_to_employee

if __name__ == '__main__':
    run_program()
