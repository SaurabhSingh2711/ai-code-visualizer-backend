import os
import json

class Database:
    def __init__(self):
        self.users = []
    
    def save_user(self, user):
        self.users.append(user)
        print(f"User saved: {user}")

    def get_all_users(self):
        return self.users


class UserService:
    def __init__(self):
        self.db = Database()

    def create_user(self, name):
        self.db.save_user(name)

    def list_users(self):
        return self.db.get_all_users()


def main():
    service = UserService()
    service.create_user("Alice")
    service.create_user("Bob")
    
    print("All users:", service.list_users())


if __name__ == "__main__":
    main()
