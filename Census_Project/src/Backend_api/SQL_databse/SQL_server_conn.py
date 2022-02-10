import pyodbc


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    connection = None

    def connect(self):
        if self.connection is None:
            self.connection = pyodbc.connect(
                'DRIVER={SQL Server};Server=LAPTOP-V5I3M0RK\SQLEXPRESS;Database=stock;UID=ABC_login;PWD=abc;')

            # self.connection.autocommit = False
            self.cursorobj = self.connection.cursor()
        return self.cursorobj
