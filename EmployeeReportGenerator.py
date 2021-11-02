from operator import attrgetter
from datetime import datetime, timedelta, timezone
from EmployeeRecord import EmployeeRecord
from EmployeeActivityRecord import EmployeeActivityRecord

class EmployeeReportGenerator:
    
    def __init__(self, cursor, break_length_in_minutes: int = 30, confusion_length_in_minutes: int = 5):
        self.cursor = cursor
        self.break_length_in_minutes = break_length_in_minutes
        self.confusion_length_in_minutes = confusion_length_in_minutes
    
    def __combine_activities(self, activities):
        chronological_activities = sorted(activities, key=attrgetter('start_time'))
        result = []
        aggregate_activity = None
        confused_segment = None
        for activity in chronological_activities:

            if aggregate_activity == None:
                aggregate_activity = activity
                continue
            
            if self.__is_activity_confusingly_short(activity) and not aggregate_activity.activity == activity.activity:
                confused_segment = activity
                continue

            if aggregate_activity.activity == activity.activity and self.__are_activities_within_break_range(aggregate_activity, activity):
                aggregate_activity.end_time = activity.end_time
                confused_segment = None
                continue
            
            result.append(aggregate_activity)
            aggregate_activity = activity

            if confused_segment:
                result.append(confused_segment)
                confused_segment = None

        result.append(aggregate_activity)
        if confused_segment:
                result.append(confused_segment)
        return result
    
    def __are_activities_within_break_range(self, aggregate_activity: EmployeeActivityRecord, activity: EmployeeActivityRecord) -> bool:
        return aggregate_activity.end_time + timedelta(minutes=self.break_length_in_minutes) >= activity.start_time
    
    def __is_activity_confusingly_short(self, activity: EmployeeActivityRecord) -> bool:
        return activity.start_time + timedelta(minutes=self.confusion_length_in_minutes) >= activity.end_time
    
    def __group_activities_by_employee_id(self, activities):
        result = {}
        for activity in activities:
            if result.get(activity.employee_id) == None:
                result[activity.employee_id] = []
            result[activity.employee_id].append(activity)
        return result
    
    def __update_timezone(self, dt: datetime) -> datetime:
        return dt.astimezone(timezone(timedelta(hours=-8)))
    
    def __display_datetime(self, dt: datetime) -> str:
        return dt.strftime('%Y-%m-%d %I:%M %p')
    
    def __display_activity_tuple(self, tuple):
        print(f'{tuple[0]} \
            {tuple[1].activity} \
            {self.__display_datetime(self.__update_timezone(tuple[1].start_time))} \
            {self.__display_datetime(self.__update_timezone(tuple[1].end_time))}'
            )
    
    def generate_report(self):
        employee_activities = EmployeeActivityRecord.getAll(self.cursor)
        if not employee_activities: return "No activities found."

        employees = {employee.id: employee.name for employee in EmployeeRecord.getAll(self.cursor)}

        grouped_employee_activities = self.__group_activities_by_employee_id(employee_activities)
        redistributed_employee_activities = []
        for employee_id, activities in grouped_employee_activities.items():
            for activity in self.__combine_activities(activities):
                redistributed_employee_activities.append((employees.get(employee_id), activity))
        
        for activity in sorted(redistributed_employee_activities, key = lambda tuple: tuple[1].start_time):
            self.__display_activity_tuple(activity)
        return