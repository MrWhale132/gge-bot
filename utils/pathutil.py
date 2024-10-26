import root
from config import Config

from resources.category import Resource

def from_resource(resource:Resource)->str:
    absPath = f"{root.project_path}/{Config.resources_rel_path}/{resource.namespace}/{resource._name}"
    return  absPath