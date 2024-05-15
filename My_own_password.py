import json


class PasswordManager:
    def __init__(self):
        self.passwords = {}

    def add_password(self, website, username, password):
        self.passwords[website] = {'username': username, 'password': password}

    def get_password(self, website):
        if website in self.passwords:
            return self.passwords[website]['username'], self.passwords[website]['password']
        else:
            print("Error: Website", website, "not found")
            return None, None

    def load_passwords(self, filename='passwords.json'):
        try:
            with open(filename, 'r') as f:
                self.passwords = json.load(f)
        except FileNotFoundError:
            print("Error: Password file not found.")

    def save_passwords(self, filename='passwords.json'):
        try:
            # Try to load existing passwords from the file
            with open(filename, 'r') as f:
                existing_passwords = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is empty or invalid JSON, create an empty dictionary
            existing_passwords = {}

        # Check if the website name and username are already present in existing passwords
        for website, credentials in self.passwords.items():
            if website not in existing_passwords or credentials['username'] != existing_passwords[website]['username']:
                existing_passwords[website] = credentials

        # Save the updated passwords to the file
        with open(filename, 'w') as f:
            json.dump(existing_passwords, f, indent=4)


if __name__ == "__main__":
    password_manager = PasswordManager()

    # Add passwords
    password_manager.add_password(input("The web address is: "), input("The user name is: "),
                                  input("The password is: "))

    # Save passwords to file
    password_manager.save_passwords()

    # Load passwords from file
    password_manager.load_passwords()

    # Retrieve password for a website
    website = input("Enter the website: ")
    password_manager.get_password(website)
