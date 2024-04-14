import requests

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


        print(ids)

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

        print(ids, project_names)
    
    @staticmethod
    def getProjectById(key: str, project_id: str):
        url = f"https://ru.yougile.com/api-v2/projects/{project_id}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {key}"
        }

        response = requests.request("GET", url, headers=headers)

        print(response.text)

NetworkingManager.getProjectById(key=key, project_id="42b08f17-b53c-4aee-8b1e-f83039c677ff")
# NetworkingManager.getProjects(key)
# NetworkingManager.getStaffById(id="7cd5f056-ae44-4eb8-a01e-fc4a808d31e0", key=key)

# NetworkingManager.inviteStaff(email='sadovodov2002@gmail.com', key=key)
# NetworkingManager.login(password='80156220722vlad', login='sadovodov23092002@mail.ru', companyName='adun123')
# NetworkingManager.getStaff(key=key)
# NetworkingManager.getApiKey(password='80156220722vlad', login='sadovodov23092002@mail.ru', companyID='aee173e7-46ab-49ca-a688-23f9ba250b07')

# NetworkingManager.login(password='7Kj-eFX-72w-5PM', login='sadovodov2002@gmail.com', companyName='adun')

