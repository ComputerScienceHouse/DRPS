import resolve
import fs
import studio_server
import os
import subprocess
from models import *
from exceptions import ProjectServerNameInvalidException, ProjectMediaDirDoesNotExistException

resolve_process: None

def init_resolve_proc():
    resolve_process = resolve.start_resolve()

def kill_resolve_proc():
    resolve.terminate_resolve(resolve_process)
    resolve_process = None

def create_project(database: Database) -> Project:
    """
    Requirements for project name: [A-Za-z0-9_] up to 32 characters
    """
    if not check_project_name_validity(database.name):
        raise ProjectServerNameInvalidException
    if database.name in studio_server.get_databases():
        raise studio_server.ProjectServerAlreadyExistsException
    if os.path.exists(fs.get_project_media_dir(database.name)):
        os.rmdir(fs.get_project_media_dir(database.name))
        
    project = Project(database=database)
    studio_server.create_database(database)
    abs_path = fs.init_project_media_dir(database.name)
    project.abs_media_dir = abs_path
    return project

def delete_project(db_name: str) -> bool:
    if not check_project_name_validity(db_name):
        raise ProjectServerNameInvalidException
    try:
        fs.remove_project_media_dir(db_name)
    except ProjectMediaDirDoesNotExistException:
        pass
    if not studio_server.delete_database(db_name):
        return False
    return True
    
def check_project_name_validity(name: str) -> bool:
    return not list(filter(lambda letter: letter not in 'abcdefghijklmnopqrstuvwxyz1234567890_', name))
