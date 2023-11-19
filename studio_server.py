import os
from models import Database
from exceptions import ProjectServerAlreadyExistsException, ProjectServerDoesNotExistException
import subprocess

def get_databases() -> list[str]:
    return [a[3::] for a in list(filter(lambda x: len(x) >= 2 and x[1] == '*', subprocess.check_output(['studio', '-l']).decode().split("\n")))]

def create_database(database: Database) -> bool:
    if database.name in get_databases():
        raise ProjectServerAlreadyExistsException
    p = call_subprocess_with_confirmation(['studio', '-c', database.name, database.name if database.password == '' else database.password], b'n')
    return p.returncode == -6

def delete_database(db_name: str) -> bool:
    if db_name not in get_databases():
        raise ProjectServerDoesNotExistException
    p = call_subprocess_with_confirmation(['studio', '-d', db_name], b'y')

    return p.returncode == -6

def backup_database(db_name: str) -> str:
    if db_name not in get_databases():
        raise ProjectServerDoesNotExistException
    results = list(filter(lambda x: 'Backup archive created' in x, subprocess.check_output(['studio', '-b', 'atom']).decode().split('\n')))
    if len(results) > 0:
        return results[0].split('`')[1]
    return ''

def reset_database_password(database: Database) -> bool:
    if database.name not in get_databases():
        raise ProjectServerDoesNotExistException
    p = call_subprocess_with_confirmation(['studio', '-p', database.name, database.name if database.password == '' else database.password], b'y')
    return p.returncode == -6

def call_subprocess_with_confirmation(command: list[str], confirm_text):
    # confirm_text must be a binary string
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = ''
    while output == '':
        output = p.stdout.read()
        print(output)
    p.communicate(input=confirm_text)
    return p
