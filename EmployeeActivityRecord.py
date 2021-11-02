from datetime import datetime

class EmployeeActivityRecord:

    def __init__(self, employee_id: int, activity: str, start_time: datetime, end_time: datetime):
        self.employee_id = employee_id
        self.activity = activity
        self.start_time = start_time
        self.end_time = end_time
    
    def __repr__(self):
        return f'EmployeeActivityRecord(employee_id={self.employee_id}, activity={self.activity}, start_time={self.start_time}, end_time={self.end_time})'
    
    def is_valid(self) -> bool:
        return self.end_time > self.start_time
    
    def getAll(db_cursor):
        db_cursor.execute("SELECT employee_id, activity_name, start_time, end_time FROM employee_activity ORDER BY start_time desc")
        return filter(
            lambda activity: activity.is_valid(),
            [EmployeeActivityRecord(*record) for record in db_cursor.fetchall()]
        )
    