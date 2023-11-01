from fastapi import APIRouter
import sys
sys.path.append("..")
from models import Database
import subprocess

router = APIRouter()

@router.get("/databases")
async def get_databases():
    return subprocess.check_output(['studio', '-l'])

@router.post("/databases/create")
async def create_database(database: Database):
    if database.username != database.db_name:
        return gen_message(422, "!! Unprocessable Entity !! - Database username must be the same as database name.")
    
    p = call_subprocess_with_confirmation(['studio', '-c', database.username, database.password], b'n')

    return gen_message(200 if p.returncode == -6 else 500, {
        "process_return_code": p.returncode,
        "message": f"Database {database.db_name} successfully created!",
        "db_object": database
    })

@router.delete("/databases/delete")
async def delete_database(db_name: str):
    p = call_subprocess_with_confirmation(['studio', '-d', db_name], b'y')

    return gen_message(200 if p.returncode == -6 else 500, {
        "process_return_code": p.returncode,
        "message": f"Database {db_name} successfully deleted!"
    })

@router.get("/databases/backup")
async def backup_database(db_name: str):
    p = subprocess.check_output(['studio', '-b', db_name])

    return gen_message(200, {
        "process_return_message": p,
        "message": f"Database {db_name} successfully backed up!"
    })

def call_subprocess_with_confirmation(command: list[str], confirm_text):
    # confirm_text must be a binary string
    p = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = ''
    while output == '':
        output = p.stdout.read()
    p.communicate(input=confirm_text)
    
    return p

def gen_message(code: int, content):
    return {
        "code": code,
        "message": content
    }

