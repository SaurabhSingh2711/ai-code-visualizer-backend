import os
import sys

class UserService:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print(f"Hello, {self.name}")

def main():
    user = UserService("Alice")
    user.greet()

if __name__ == "__main__":
    main()

