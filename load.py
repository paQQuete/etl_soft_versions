from models import User, Host, Program


class LoadService:
    def __init__(self, data, cursor):
        self._username = data.username
        self._hostname = data.hostname
        self._timestamp = data.timestamp
        self._data = data.data
        self._cursor = cursor

    def _if_exist_host(self):
        self._cursor.execute(f"""select * from Host where Hostname = '{self._hostname}';""")
        _ = self._cursor.fetchall()
        return bool(len(_))

    def _if_exist_user(self) -> bool:
        self._cursor.execute(f"""select * from User where Username = '{self._username}';""")
        _ = self._cursor.fetchall()
        return bool(len(_))

    def _if_exist_record(self, row: dict) -> bool:
        self._cursor.execute(f"""
        select * from Program_record where Publisher = '{row["Publisher"]}' AND DisplayName = '{row["DisplayName"]}'
        AND DisplayVersion = '{row["DisplayVersion"]}' AND InstallDate = '{row["InstallDate"]}'
        AND username_id = '{self._username}' AND hostname_id = '{self._hostname}';
        """)
        _ = self._cursor.fetchall()
        return bool(len(_))

    def loads(self):
        if not self._if_exist_host():
            Host.create(hostname=self._hostname)
        if not self._if_exist_user():
            User.create(username=self._username)

        for row in self._data:
            if self._if_exist_record(row):
                continue
            Program.create(publisher=row['Publisher'], display_name=row['DisplayName'],
                           display_version=row['DisplayVersion'], install_date=row['InstallDate'],
                           username=self._username, hostname=self._hostname)

