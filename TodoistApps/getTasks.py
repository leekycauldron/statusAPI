import requests,sys
import requests
from requests.structures import CaseInsensitiveDict
sys.path.insert(1,".")
from config import TODIST_API_KEY
#Rate Limit: 1 per 2 seconds.

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "Bearer " + str(TODIST_API_KEY)
#This function gets all the tasks in the "Tasks" project which is the the project to be used.
def getTasks():
    #Get all the tasks in project and turn it into a list of dicts.
    tasks = requests.get('https://api.todoist.com/rest/v1/tasks?project_id=2208003845',headers=headers).json()
    tasksPretty = []
    #Filter out all the useless data
    for tasks in tasks:
        temp = {}
        temp["Task"] = tasks["content"]
        temp["Description"] = tasks["description"]
        temp["Priority"] = tasks["priority"]
        temp["Due Date"] = tasks["due"]["date"]
        temp["ID"] = tasks["id"]
  
        tasksPretty.append(temp)
    return tasksPretty