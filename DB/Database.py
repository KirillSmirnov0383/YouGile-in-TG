from sqlalchemy import create_engine
from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from DB.DatabaseClass import User, Company, ApiCompany

from sqlalchemy import cast, String

from services.NetworkingManager import NetworkingManager



class DatabaseManager:
    def __init__(self):
        self.engine = create_engine("postgresql://postgres:KlimKva22@localhost/YouGile_Managment")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.NM = NetworkingManager()

    def add_user(self, telegram_id, email=None, password=None, company=None):
        if not (self.session.query(User).filter(cast(User.Telegram_id, String) == str(telegram_id)).first()):
            new_user = User(Telegram_id=telegram_id, email=email, password=password, company_name=company)  # Используйте 'company_name' вместо 'company'
            self.session.add(new_user)
            self.session.commit()
        

    def set_user_email(self, email, telegram_id):
        user = self.session.query(User).filter(cast(User.Telegram_id, String) == str(telegram_id)).first()
        user.email = email
        self.session.commit()

    def set_user_company(self, company, telegram_id):
        user = self.session.query(User).filter(cast(User.Telegram_id, String) == str(telegram_id)).first()
        user.company_name = company
        self.session.commit()

    def set_user_password(self, password, telegram_id):
        user = self.session.query(User).filter(cast(User.Telegram_id, String) == str(telegram_id)).first()
        print("Before password change:", user.password)  # Отладочный вывод
        user.password = password
        setattr(user, '_password', user.password)  # Уведомляем SQLAlchemy о изменении _password
        print("After password change:", user.password)  # Отладочный вывод
        self.session.commit()

    def get_user_data(self, telegram_id):
        user_data = self.session.query(User.password, User.email, User.company_name).filter(cast(User.Telegram_id, String) == str(telegram_id)).first()

        if user_data:
            password, email, company_name = user_data
            
            user_dict = {
                "password": password,
                "email": email,
                "company": company_name
            }

            return user_dict
        else:
            return None
        
    def add_company(self, company_id, company_name):
        # Проверяем существует ли компания с таким id
        existing_company = self.session.query(Company).filter(cast(Company.id, String) == company_id).first()

        # Если компания уже существует, выводим сообщение и выходим из функции
        if existing_company:
            print(f"Company with id {company_id} already exists.")
            return company_id

        # Если компания не существует, создаем новую компанию и добавляем её в базу данных
        new_company = Company(id=company_id, name=company_name)
        self.session.add(new_company)
        self.session.commit()
        return company_id

    def add_ApiKey(self, telegram_id, company_id):
        # Проверяем существует ли запись ApiCompany с указанным пользователем и компанией
        existing_api_company = self.session.query(ApiCompany).filter(
            ApiCompany.user_id == self.session.query(User.id).filter(cast(User.Telegram_id, String) == str(telegram_id)).scalar(),
            ApiCompany.company_id == company_id
        ).first()

        # Если запись уже существует, выводим сообщение и завершаем функцию
        if existing_api_company:
            print("ApiKey for this user and company already exists.")
            return

        # Получаем данные пользователя
        user_dict = self.get_user_data(telegram_id)

        # Создаем новый ApiKey
        ApiKey = self.NM.createApiKey(login=user_dict["email"], password=user_dict["password"], companyID=company_id)

        # Создаем новую запись ApiCompany и добавляем ее в сессию
        new_Api = ApiCompany(
            user_id=self.session.query(User.id).filter(cast(User.Telegram_id, String) == str(telegram_id)).scalar(),
            company_id=company_id,
            api_key=ApiKey
        )
        self.session.add(new_Api)
        self.session.commit()

    def get_api_key(self, TelegramId):
        user_id = self.session.query(User.id).filter(User.Telegram_id == str(TelegramId)).scalar()
        
        if user_id is None:
            return None

        api_key = self.session.query(ApiCompany.api_key).filter(ApiCompany.user_id == user_id).scalar()
        
        return api_key
        
    def close(self):
        self.session.close()


