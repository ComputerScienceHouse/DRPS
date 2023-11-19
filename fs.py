import os

from exceptions import ProjectNameConflictException, ProjectMediaDirDoesNotExistException

ROOT_FOLDER = os.getenv("ROOT_MEDIA_DIR")
SSHFS_HOSTNAME = os.getenv("SSHFS_HOSTNAME")

if not os.path.exists(ROOT_FOLDER):
    os.makedirs(f"{ROOT_FOLDER}/projects/")

def init_project_media_dir(project_name: str) -> str:
    path = get_project_media_dir(project_name)
    if os.path.exists(path):
        raise ProjectNameConflictException
    os.makedirs(path)
    os.makedirs(f"{path}/.config")

    permissions = 0o666
    os.chmod(path, permissions)

def get_project_media_dir(proj_name: str, unsafe: bool = False) -> str:
    if not unsafe:
        if not project_media_dir_exists(proj_name):
            return ''
    return f"{ROOT_FOLDER}/projects/{proj_name}/"

def project_media_dir_exists(proj_name: str) -> bool:
    path = get_project_media_dir(proj_name, True)
    return os.path.exists(path)

def remove_project_media_dir(proj_name: str) -> bool:
    if not project_media_dir_exists(proj_name):
        raise ProjectMediaDirDoesNotExistException
    path = get_project_media_dir(proj_name)
    os.rmdir(path)
    return True

def get_sshfs_link(proj_name: str) -> str:
    return f"<user>@{SSHFS_HOSTNAME}:{ROOT_FOLDER}/projects/{proj_name}/"
