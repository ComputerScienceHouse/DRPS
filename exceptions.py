"""
File exclusively for custom exceptions
"""

class ProjectServerNameInvalidException(Exception):
    pass

class ProjectServerAlreadyExistsException(Exception):
    pass

class ProjectServerDoesNotExistException(Exception):
    pass

class ProjectNameConflictException(Exception):
    pass

class ProjectMediaDirDoesNotExistException(Exception):
    pass

