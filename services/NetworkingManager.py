import requests
import json
from datetime import datetime


key = 'f5jmTUMVBtPQ334LDbgmChHfDj+cfiiQ7sI2dCH4ElxQaMUeuj-dlDqs3RhKFJqK'

class NetworkingManager: 

    @staticmethod
    def login(password: str, login: str, companyName: str):
        url = "https://ru.yougile.com/api-v2/auth/companies"
        payload = {
            "login": login,
            "password": password,
            "name": companyName
        }
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.text)
        if response.status_code == 200:
            response_json = response.json()
            id_value = response_json["content"][0]["id"]
            return id_value
        else:
            return True


    # запускается только при первом входе
    @staticmethod
    def createApiKey(password: str, login: str, companyID: str):
        url = "https://ru.yougile.com/api-v2/auth/keys"
        
        payload = {
            "login": login,
            "password": password,
            "companyId": companyID
        }
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, json=payload, headers=headers)

        if response.status_code == 201:
            response_json = response.json()
            key_value = response_json['key']
            return key_value
        else:
            return False

    @staticmethod
    def getApiKey(password: str, login: str, companyID: str):

        url = "https://ru.yougile.com/api-v2/auth/keys/get"
        return 'jkTWpLFxm0i1xY27dWbd4se4pknDoKpcEaXBZWf3vFdFBATKfzdetqNULmQKYmXk'
        payload = {
            "login": f"{login}",
            "password": f"{password}",
            "companyId": f"{companyID}"
        }
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, json=payload, headers=headers)
        data = response.json()
        if type(data) == type(list()):
            return data[1]['key']
        else: return data['key']


    
    @staticmethod
    def getStaff(key: str, email = None, projectId = None):
        url = "https://ru.yougile.com/api-v2/users"

        if email:
            querystring = {"email":f"{email}"}
        elif projectId:
            querystring = {"projectId":f"{projectId}"}
        else:
            querystring = {}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()


        real_names = [user["realName"] for user in data["content"]] # все имена
        ids = [user["id"] for user in data["content"]] # все id
        result_dict = dict(zip(ids, real_names))

        return result_dict

    @staticmethod
    def getStaffById(id: str, key: str):
        url = f"https://ru.yougile.com/api-v2/users/{id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers)

        data = response.json()
        return NetworkingManager.format_user(data)

    @staticmethod
    def isAdmin(id: str, key: str):
        url = f"https://ru.yougile.com/api-v2/users/{id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

        return data['isAdmin']

    @staticmethod
    def inviteStaff(email: str, key: str, isAdmin = False):

        url = "https://ru.yougile.com/api-v2/users"

        payload = {
            "email": email,
            "isAdmin": isAdmin
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        print(response.text)

        if response.status_code == 201:
            return True
        else: return False

    @staticmethod
    def giveAdmin(id: str, key: str, isAdmin: bool):
        url = f"https://ru.yougile.com/api-v2/users/{id}"
        payload = {"isAdmin": isAdmin}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("PUT", url, json=payload, headers=headers)

        print(response.text)    

    @staticmethod
    def getProjects(key: str):
        url = "https://ru.yougile.com/api-v2/projects"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

        ids = [project["id"] for project in data["content"]]
        project_names =  [project["title"] for project in data["content"]]
        result_dict = dict(zip(ids, project_names))

        return result_dict  
    
    @staticmethod
    def getProjectById(key: str, project_id: str):
        url = f"https://ru.yougile.com/api-v2/projects/{project_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers).json()
        
        return NetworkingManager.format_project(response)

    @staticmethod
    def deleteUser(key: str, user_id: str):
        url = f"https://ru.yougile.com/api-v2/users/{user_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("DELETE", url, headers=headers)

        print(response.text)

    @staticmethod
    def giveAdmin(id: str, key: str, isAdmin: bool):
        url = f"https://ru.yougile.com/api-v2/users/{id}"
        payload = {"isAdmin": isAdmin}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("PUT", url, json=payload, headers=headers)

        print(response.text)  

    @staticmethod
    def createProject(key: str, title: str, users: dict):
        url = "https://ru.yougile.com/api-v2/projects"

        payload = {
            "title": f"{title}",
            "users": users
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        print(response.text)

    @staticmethod
    def editProject(project_id: str, key: str, title = None, isDelete = False, users = dict()):

        url = f"https://ru.yougile.com/api-v2/projects/{project_id}"
        if title:
            payload = {
                "deleted": isDelete,
                "title": f"{title}",
            }
        else:
            payload = {
                "deleted": isDelete,
                "users": users
            }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("PUT", url, json=payload, headers=headers)

        print(response.text)

    @staticmethod
    def createBoard(title: str, project_id: str, key: str):
        url = "https://ru.yougile.com/api-v2/boards"

        payload = {
            "title": f"{title}",
            "projectId": f"{project_id}",
            "stickers": {
                "timer": False,
                "deadline": True,
                "stopwatch": True,
                "timeTracking": True,
                "assignee": True,
                "repeat": True,
                "custom": {
                    # "fbc30a9b-42d0-4cf7-80c0-31fb048346f9": True,
                    # "645250ca-1ae8-4514-914d-c070351dd905": True
                }
            }
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        data = response.json()
        board_id = data['id']
        print(board_id)

    @staticmethod
    def getBoardsByProjectID(project_id: str, key: str):
        url = "https://ru.yougile.com/api-v2/boards"

        querystring = {"projectId":f"{project_id}"}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()

        ids = [board["id"] for board in data["content"]]
        board_names =  [board["title"] for board in data["content"]]
        result_dict = dict(zip(ids, board_names))

        return result_dict
    
    @staticmethod
    def getBoardByID(board_id: str, key: str):
        url = f"https://ru.yougile.com/api-v2/boards/{board_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers).json()
    

        return NetworkingManager.format_board(response)
    
    @staticmethod
    def deleteBoard(board_id: str, key: str):

        url = f"https://ru.yougile.com/api-v2/boards/{board_id}"
        payload = {
            "deleted": True,

        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("PUT", url, json=payload, headers=headers)

        print(response.text)

    @staticmethod
    def getColumns(board_id: str, key: str):

        url = "https://ru.yougile.com/api-v2/columns"

        querystring = {"boardId":f"{board_id}"}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        data = response.json()
        result_dict = {item["id"]: item["title"] for item in data["content"]}

        return result_dict
    
    @staticmethod
    def getTasksByColumn(column_id: str, key: str):

        url = "https://ru.yougile.com/api-v2/tasks"

        querystring = {"columnId": f"{column_id}"}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json()
        result_dict = {item["id"]: item["title"] for item in data["content"]}

        return result_dict
    
    @staticmethod
    def getTaskById(task_id: str, key: str):

        url = f"https://ru.yougile.com/api-v2/tasks/{task_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers)

        return NetworkingManager.format_task(response.json())
    
    @staticmethod
    def renameBoard(board_id: str, new_title: str, key: str):

        url = f"https://ru.yougile.com/api-v2/boards/{board_id}"

        payload = {
            "title": f"{new_title}",
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("PUT", url, json=payload, headers=headers)

        print(response.text)

    @staticmethod
    def createColumn(board_id: str, title: str, key: str):

        url = "https://ru.yougile.com/api-v2/columns"

        payload = {
            "title": f"{title}",
            # "color": 2,
            "boardId": f"{board_id}"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        print(response.text)

    @staticmethod
    def etitTask(task_id: str, key: str, title = None, isDeleted = False, isComplete = False, column_id = None, description = None):

        url = f"https://ru.yougile.com/api-v2/tasks/{task_id}"

        if title:
            payload = {
                "title": f"{title}"
            }
        elif column_id:
            payload = {
                "columnId": f"{column_id}",
            }
        elif description:
            payload = {
                "description": f"{description}"
            }
        else:
            payload = {
                "deleted": isDeleted,
                "completed": isComplete,
                # "subtasks": ["0fe1e417-2415-4e76-932a-ca07a25d6c64", "f0118d9e-2888-48e4-a172-116085da4279"],
                # "assigned": ["80eed1bd-eda3-4991-ac17-09d28566749d"],
                # "deadline": {
                #     "deadline": 1653029146646,
                #     "startDate": 1653028146646,
                #     "withTime": True,
                #     "deleted": True
                # }
            }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("PUT", url, json=payload, headers=headers)

        print(response.text)


    @staticmethod
    def format_single_date(date):
        deadline_datetime = datetime.fromtimestamp(date / 1000)
        return deadline_datetime.strftime("%Y-%m-%d %H:%M:%S")


    @staticmethod
    def decode(data):
        decoded_dict = json.loads(str(data))
        return decoded_dict


    @staticmethod
    def format_user(data: dict):
        """
        {
            "id": "4f6f0391-0f94-4d30-9b0e-99430a36d4fb",
            "email": "example.user@yandex.ru",
            "isAdmin": false,
            "realName": "Калганов Андрей Алексеевич",
            "status": "online",
            "lastActivity": "1656012328"
        }
        """
        date = NetworkingManager.format_single_date(data['lastActivity'])
        # name = NetworkingManager.decode(data['realName'])

        returned_data = f"""Имя: {data['realName']}\nПочта: {data['email']}\nСтатус: {data['status']}\nПоследняя активность: {date}\nАдмин: {data["isAdmin"]}
            """
        
        return returned_data
    
    @staticmethod
    def format_board(data: dict):
        """{
            "deleted": true,
            "id": "4f6f0391-0f94-4d30-9b0e-99430a36d4fb",
            "title": "Тестирование",
            "projectId": "001623dc-6501-461b-9de6-c1d1d6fc1d16",
            "stickers": {
                "timer": false,
                "deadline": true,
                "stopwatch": true,
                "timeTracking": true,
                "assignee": true,
                "repeat": true,
                "custom": {
                "fbc30a9b-42d0-4cf7-80c0-31fb048346f9": true,
                "645250ca-1ae8-4514-914d-c070351dd905": true
                    }
                }
            }
            """
        return f"Название: {data['title']}"
    
    @staticmethod
    def format_project(data: dict):
        return f"Название: {data['title']}"
    
    
    @staticmethod
    def format_column(data: dict):
        return f"Название: {NetworkingManager.decode(data['title'])}"

    
    @staticmethod
    def format_task(data: dict):
        try:
            returned_data = f"""Название: {data['title']}\nОписание: {data['description']}\nСтатус выполнения: {data['completed']}
            """
        except: 
            returned_data = f"""Название: {data['title']}\n\nСтатус выполнения: {data['completed']}
            """
        

        return returned_data
# NetworkingManager.getProjectById(key=key, project_id="42b08f17-b53c-4aee-8b1e-f83039c677ff")
# NetworkingManager.getProjects(key)
# NetworkingManager.getStaffById(id="7cd5f056-ae44-4eb8-a01e-fc4a808d31e0", key=key)
# NetworkingManager.createApiKey(password='KlimKva22', login='kirill.smirnov.spb@gmail.com', companyID='aee173e7-46ab-49ca-a688-23f9ba250b07')
# NetworkingManager.inviteStaff(email='sadovodov2002@gmail.com', key=key)
# NetworkingManager.login(password='80156220722vlad', login='sadovodov23092002@mail.ru', companyName='adun123')
# NetworkingManager.getStaff(key=key)
# NetworkingManager.getApiKey(password='80156220722vlad', login='sadovodov23092002@mail.ru', companyID='aee173e7-46ab-49ca-a688-23f9ba250b07')

# NetworkingManager.login(password='7Kj-eFX-72w-5PM', login='sadovodov2002@gmail.com', companyName='adun')