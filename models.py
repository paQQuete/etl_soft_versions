import datetime

from peewee import Model
from peewee import AutoField, TextField, DateField, DateTimeField, ForeignKeyField

from config import conn


class BaseModel(Model):
    id = AutoField(column_name='id')
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = conn


class User(BaseModel):
    username = TextField(column_name='Username', null=False)

    class Meta:
        table_name = 'User'


class Host(BaseModel):
    hostname = TextField(column_name='Hostname', null=False)

    class Meta:
        table_name = 'Host'


class Program(BaseModel):
    publisher = TextField(column_name='Publisher', null=True)
    display_name = TextField(column_name='DisplayName', null=True)
    display_version = TextField(column_name='DisplayVersion', null=True)
    install_date = DateField(column_name='InstallDate', null=True)
    username = ForeignKeyField(User, related_name='fk_record_user', to_field='username', on_delete='cascade')
    hostname = ForeignKeyField(Host, related_name='fk_record_host', to_field='hostname')

    class Meta:
        table_name = 'Program_record'
        order_by = ('InstallDate',)
