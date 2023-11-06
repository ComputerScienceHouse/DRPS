import DaVinciResolveScript as dvr
import subprocess
import os
import time


DBLIST_PATH = "/home/atom/.local/share/DaVinciResolve/configs/.dblist"

class RenderJobListEmptyException(Exception):
    "Raised when attempting to render but no jobs created beforehand"
    pass

class ProjectInvalidException(Exception):
    "Raised when project is inaccessible"

    def __init__(self, message="Project was inaccessible! Please change the project first or load one."):
        super().__init__(message)
        
class TimelineRenderException(Exception):
    "Raised when there is a render error"
    pass

class TimelineInvalidException(Exception):
    "Raised when timline is inaccessible"
    pass

def get_current_database() -> dict[str, str]:
    return resolve.GetProjectManager().GetCurrentDatabase()

def get_database_list() -> list[dict[str, str]]:
    return resolve.GetProjectManager().GetDatabaseList()

def load_database(db_info: dict[str, str]):
    """
    Sample DB Info:
    {
       'DbType': 'Disk' or 'Postgres',
       'DbName': database name,
       'IpAddress': IP address (optional)
    }
    """

    return resolve.GetProjectManager().SetCurrentDatabase(db_info)

def load_project(proj_name: str):
    project = get_current_project()
    if project is not None:
        if project.GetName() == proj_name:
            print("Project already loaded!")
            return project
    result = resolve.GetProjectManager().LoadProject(proj_name)
    if result:
        print(f"Project {result.GetName()} loaded!")
    else:
        print(f"Unable to load project {proj_name}...")
        return result

def start_rendering():
    project = get_current_project()
    if len(project.GetRenderJobList()) == 0:
        raise RenderJobListEmptyException("No jobs in render queue!")
    return project.StartRendering()
    
def add_timeline_render_job(timeline, render_preset: str, output_path: str, custom_name: str, render_format: str, render_codec: str):
    project = get_current_project()
    resolve.OpenPage("Deliver")
    project.SetCurrentTimeline(timeline)
    project.LoadRenderPreset(render_preset)
    project.SetCurrentRenderFormatAndCodec(render_format, render_codec)
    
    project.SetRenderSettings({
           "SelectAllFrames": 1,
           "TargetDir": output_path,
           "CustomName": custom_name
    })

    return project.AddRenderJob()

def get_timeline_by_index(idx: int):
    project = get_current_project()
    timeline = project.GetTimelineByIndex(idx)
    if timeline is None:
        raise TimelineInvalidException
    return timeline

def get_all_timelines_by_index() -> dict[int, str]:
    timelines = {}
    project = get_current_project()
    if project is not None:
        num_timelines = project.GetTimelineCount()

        for i in range(1, num_timelines+1):
            timeline = project.GetTimelineByIndex(i)
            if timeline is not None:
                timelines[i] = timeline.GetName()
    else:
        raise ProjectInvalidException

    return timelines

def get_render_formats() -> dict[str, str]:
    return get_current_project().GetRenderFormats()

def get_render_codecs(render_format: str) -> dict[str, str]:
    return get_current_project().GetRenderCodecs(render_format)

def get_render_presets() -> list[str]:
    return get_current_project().GetRenderPresetList()

def get_current_project():
    project = resolve.GetProjectManager().GetCurrentProject()
    if project is None:
        raise ProjectInvalidException
    return project

def terminate_resolve(process):
    process.kill()
    
def start_resolve() -> subprocess.Popen:
    return subprocess.Popen([f".{os.getenv('RESOLVE_ABS_PATH')}"], cwd='/',
                            stdout=subprocess.DEVNULL)

process = start_resolve()
resolve = dvr.scriptapp("Resolve")

while resolve is None:
    time.sleep(1)
    resolve = dvr.scriptapp("Resolve")
load_project("Test")
