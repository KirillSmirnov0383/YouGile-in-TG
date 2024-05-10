import requests
from datetime import datetime

key1 = 'f5jmTUMVBtPQ334LDbgmChHfDj+cfiiQ7sI2dCH4ElxQaMUeuj-dlDqs3RhKFJqK'

class NetworkingManager: 

    @staticmethod
    def format_single_date(date):
        return date.strftime("%Y-%m-%d %H:%M:%S")



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
        name = data['realName'].encode('utf-8').decode('unicode-escape')

        returned_data = {
            "Имя": name,
            "Почта": data['email'],
            "Статус": data['status'],
            "Последняя активность": f"{date}",
            "Админ": data["isAdmin"]
            }
        
        return returned_data
    
    @staticmethod
    def format_board(data: dict, key: str):
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
        returned_data = {
            "Название": data['title'],
        }

        return returned_data
    
    @staticmethod
    def format_project(data: dict):
        returned_data = {
            "Название": data['title'],
        }

        return returned_data
    
    @staticmethod
    def format_column(data: dict):
        returned_data = {
            "Название": data['title'],
        }

        return returned_data
    
    @staticmethod
    def format_task(data: dict):
        returned_data = {
            "Название": data['title'],
            "Описание": data['description'],
            "Статус выполнения": data['completed'],

        }

        return returned_data
    
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
            print("ID:", id_value) # id компании который нужно будет запомнить
        else:
            print("Вы ввели неверный логин или пароль")


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
            print("Key:", key_value)

    @staticmethod
    def getApiKey(password: str, login: str, companyID: str):

        url = "https://ru.yougile.com/api-v2/auth/keys/get"

        payload = {
            "login": f"{login}",
            "password": f"{password}",
            "companyId": f"{companyID}"
        }
        headers = {"Content-Type": "application/json"}

        response = requests.request("POST", url, json=payload, headers=headers)
        data = response.json()
        if type(data) == type(list()):
            return data[0]['key']
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


        print(ids, real_names)

    @staticmethod
    def getStaffById(id: str, key: str):
        url = f"https://ru.yougile.com/api-v2/users/{id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers)

        print(response.text)

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
        if response.status_code == 201:
            print(True)
        else: print(False)



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
    def deleteUser(key: str, user_id: str):
        url = f"https://ru.yougile.com/api-v2/users/{user_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("DELETE", url, headers=headers)

        print(response.text)
    
    @staticmethod
    def getUsersByProject(key: str, project_id: str):
        url = f"https://ru.yougile.com/api-v2/projects/{project_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()

        users = data["users"]

        print(users)

# -------------------------- PROJECTS ------------------------------

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

        print(result_dict)        

    @staticmethod
    def getProjectById(key: str, project_id: str):
        url = f"https://ru.yougile.com/api-v2/projects/{project_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers)

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
        if title is None:
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

    
# -------------------------- BOARDS ------------------------------

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

        print(result_dict)


    @staticmethod
    def getBoardByID(board_id: str, key: str):
        url = f"https://ru.yougile.com/api-v2/boards/{board_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        } 

        response = requests.request("GET", url, headers=headers)

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
    def moveBoardToAnotherProject(board_id: str, project_id: str, key: str):

        url = f"https://ru.yougile.com/api-v2/boards/{board_id}"

        payload = {
            "projectId": f"{project_id}",

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

        print(result_dict)

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
    def deleteColumn(column_id: str, key: str):

        url = f"https://ru.yougile.com/api-v2/columns/{column_id}"

        payload = {
            "deleted": True,
            # "title": "To do",
            # "color": 2,
            # "boardId": "0d923a9f-3675-43c6-84ce-f3580cf5e760"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("PUT", url, json=payload, headers=headers)

        print(response.text)

    @staticmethod
    def renameColumn(column_id: str, key: str, title: str):
        url = f"https://ru.yougile.com/api-v2/columns/{column_id}"

        payload = {
            # "deleted": True,
            "title": f"{title}",
            # "color": 2,
            # "boardId": "0d923a9f-3675-43c6-84ce-f3580cf5e760"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("PUT", url, json=payload, headers=headers)

        print(response.text)

    @staticmethod
    def getTasksByColumn(column_id: str, key: str):

        url = "https://ru.yougile.com/api-v2/tasks"

        querystring = {"columnId": f"{column_id}"}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)

    @staticmethod
    def getTasksByTitle(title: str, key: str):

        url = "https://ru.yougile.com/api-v2/tasks"

        querystring = {"title": f"{title}"}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)

    @staticmethod
    def getTaskById(task_id: str, key: str):

        url = f"https://ru.yougile.com/api-v2/tasks/{task_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers)

        print(response.text)
    
    @staticmethod
    def createTask(columnId: str, title: str, key: str, description: str = None):

        url = "https://ru.yougile.com/api-v2/tasks"

        payload = {
            "title": f"{title}",
            "columnId": f"{columnId}",
            "description": f"{description}",
            "archived": False,
            "completed": False,
            # "subtasks": ["329c548b-4869-43e6-a094-9a30e9eed819"],
            # "assigned": ["80eed1bd-eda3-4991-ac17-09d28566749d"],
            "deadline": {
                "deadline": 1653029146646,
                "startDate": 1653028146646,
                "withTime": True
            },
            # "timeTracking": {
            #     "plan": 10,
            #     "work": 5
            # },
            # "checklists": [
            #     {
            #         "title": "list 1",
            #         "items": [
            #             {
            #                 "title": "option 1",
            #                 "isCompleted": False
            #             },
            #             {
            #                 "title": "option 2",
            #                 "isCompleted": False
            #             }
            #         ]
            #     }
            # ],
            # "stickers": {
            #     "fbc30a9b-42d0-4cf7-80c0-31fb048346f9": "0baced9640b2",
            #     "645250ca-1ae8-4514-914d-c070351dd905": "815016901edd"
            # },
            # "stopwatch": {"running": True},
            # "timer": {
            #     "running": True,
            #     "seconds": 600
            # }
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





company_id_adun = '62697425-36fb-461d-945a-0a54dd008105'
key = 'ehCLgtqOp8h9Jwb5fZSTgX05k9jTSlInz70hakr0dieiDwMJXvOW97+ESJa5b-ZY'
key2 = "W7Mfahp0mlU+bHN5WxUSwzdPgiZmNgZ3XQmwY5l7WlHdaHpl+OUA+Fw5F7zDMPHg"



# NetworkingManager.getStaff(key=key2)
# NetworkingManager.getProjectById(key="W7Mfahp0mlU+bHN5WxUSwzdPgiZmNgZ3XQmwY5l7WlHdaHpl+OUA+Fw5F7zDMPHg", project_id="42b08f17-b53c-4aee-8b1e-f83039c677ff")
# NetworkingManager.getProjects(key='W7Mfahp0mlU+bHN5WxUSwzdPgiZmNgZ3XQmwY5l7WlHdaHpl+OUA+Fw5F7zDMPHg')
# NetworkingManager.createApiKey(password='80156220722vlad', login='sadovodov23092002@mail.ru', companyID='aee173e7-46ab-49ca-a688-23f9ba250b07')
# NetworkingManager.getApiKey(password='7Kj-eFX-72w-5PM', login='sadovodov2002@gmail.com', companyID=company_id_adun)
# NetworkingManager.createTask(columnId='80169cbb-1643-4620-9211-e9ceb4f16deb', title='aaa', key=key)
# NetworkingManager.getTaskById(task_id='4810c2f5-6105-4b48-849f-b63602beb936', key=key)
# NetworkingManager.createSubtask(taskId='4810c2f5-6105-4b48-849f-b63602beb936', title='aaa', description='sss', key=key)
# NetworkingManager.getTasksByTitle(title='qqq', key=key)
# NetworkingManager.getTasksByColumn(column_id='80169cbb-1643-4620-9211-e9ceb4f16deb', key=key)
# NetworkingManager.deleteColumn(column_id='30d00704-5634-4ad6-983f-11661cba0970', key=key)
# NetworkingManager.createColumn(board_id='8d0b3203-ba18-493e-b01a-9b35d89fc2a2', title="In Progress", key=key)
# NetworkingManager.getColumns(board_id='8d0b3203-ba18-493e-b01a-9b35d89fc2a2', key=key)
# NetworkingManager.moveToAnotherProject(project_id='f8639053-08ac-460c-90bc-6d5564225403', board_id='07eb7c41-8c0b-40de-80cf-f5f1a5000192', key=key)
# NetworkingManager.renameBoard(board_id='07eb7c41-8c0b-40de-80cf-f5f1a5000192', new_title="qq", key=key)
# NetworkingManager.deleteBoard(board_id='406303c9-4692-421e-836e-307e8b0bde50', key=key, delete=True)
# NetworkingManager.createBoard(title='asd', project_id='b03cd9bc-07a5-47a6-95a9-a5f467de7fa4', key=key)
# NetworkingManager.getBoardByID(board_id='540d8df0-8203-4678-aa64-45d00249e1e5', key=key)    
# NetworkingManager.getBoardsByProjectID(project_id="b03cd9bc-07a5-47a6-95a9-a5f467de7fa4", key=key)
# NetworkingManager.getProjectById(key=key, project_id="0f57b6e1-93aa-4a33-90b1-f2ecae9c71fa")
# NetworkingManager.getProjects(key)
# NetworkingManager.getStaffById(id="7cd5f056-ae44-4eb8-a01e-fc4a808d31e0", key=key)
# NetworkingManager.inviteStaff(email='user@mail.ru', key=key)
# NetworkingManager.login(password='7Kj-eFX-72w-5PM', login='sadovodov2002@gmail.com', companyName='adun')
# NetworkingManager.getStaff(key=key)
# NetworkingManager.getApiKey(password='7Kj-eFX-72w-5PM', login='sadovodov2002@gmail.com', companyID=company_id_adun)
# NetworkingManager.createApiKey(password='7Kj-eFX-72w-5PM', login='sadovodov2002@gmail.com', companyID=company_id_adun)
# NetworkingManager.login(password='7Kj-eFX-72w-5PM', login='sadovodov2002@gmail.com', companyName='adun')


