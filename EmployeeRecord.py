class EmployeeRecord:

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
    
    def __repr__(self):
        return f'EmployeeRecord(id={self.id}, name={self.name})'
    
    def getAll(db_cursor):
        db_cursor.execute("SELECT id, name FROM employee")
        return [EmployeeRecord(*record) for record in db_cursor.fetchall()]