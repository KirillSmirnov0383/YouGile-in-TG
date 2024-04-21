import requests

key1 = 'f5jmTUMVBtPQ334LDbgmChHfDj+cfiiQ7sI2dCH4ElxQaMUeuj-dlDqs3RhKFJqK'

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

        print(response.text)

    
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
    def getTasks(column_id: str, key: str):

        url = "https://ru.yougile.com/api-v2/tasks"

        querystring = {"columnId":f"{column_id}"}

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)
    




company_id_adun = '62697425-36fb-461d-945a-0a54dd008105'
key = 'ehCLgtqOp8h9Jwb5fZSTgX05k9jTSlInz70hakr0dieiDwMJXvOW97+ESJa5b-ZY'

NetworkingManager.getTasks(column_id='80169cbb-1643-4620-9211-e9ceb4f16deb', key=key)
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

# NetworkingManager.inviteStaff(email='kirill.smirnov.spb@gmail.com', key=key)
# NetworkingManager.login(password='7Kj-eFX-72w-5PM', login='sadovodov2002@gmail.com', companyName='adun')
# NetworkingManager.getStaff(key=key)
# NetworkingManager.getApiKey(password='7Kj-eFX-72w-5PM', login='sadovodov2002@gmail.com', companyID=company_id_adun)
# NetworkingManager.createApiKey(password='7Kj-eFX-72w-5PM', login='sadovodov2002@gmail.com', companyID=company_id_adun)
# NetworkingManager.login(password='7Kj-eFX-72w-5PM', login='sadovodov2002@gmail.com', companyName='adun')

