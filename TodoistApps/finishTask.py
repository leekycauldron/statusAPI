import requests,sys
import requests
from requests.structures import CaseInsensitiveDict
sys.path.insert(1,".")
from config import TODIST_API_KEY
#Rate Limit: 1 per 2 seconds.

headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = "Bearer " + str(TODIST_API_KEY)
#This function closes the task given the task ID.
def finishTask(taskID):
    #Send request to close given task.
    tasks = requests.post('https://api.todoist.com/rest/v1/tasks/'+str(taskID)+'/close',headers=headers)
    if tasks.status_code == 204:
        return True
    return False