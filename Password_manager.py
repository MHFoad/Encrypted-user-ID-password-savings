import json
from cryptography.fernet import Fernet, InvalidToken


class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        self.passwords = {}

    def encrypt_password(self, password):
        print(f"Encryption Key: {self.key.decode()}")
        return self.fernet.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        try:
            decrypted_password = self.fernet.decrypt(encrypted_password.encode()).decode()
            print(f"Decrypted password: {decrypted_password}")
            return decrypted_password
        except InvalidToken as e:
            print("Error: Invalid token. Failed to decrypt password.")
            return None

    def add_password(self, website, username, password):
        encrypted_password = self.encrypt_password(password)
        self.passwords[website] = {'username': username, 'password': encrypted_password}

    def get_password(self, website):
        if website in self.passwords:
            encrypted_password = self.passwords[website]['password']
            decrypted_username, decrypted_password = self.decrypt_credentials(encrypted_password)
            if decrypted_username is not None and decrypted_password is not None:
                return decrypted_username, decrypted_password
            else:
                print("Error: Failed to retrieve password for", website)
                return None, None
        else:
            print("Error: Website", website, "not found")
            return None, None

    def decrypt_credentials(self, encrypted_credentials):
        print(f"Encryption Key: {self.key.decode()}")
        try:
            decrypted_credentials = self.fernet.decrypt(encrypted_credentials.encode()).decode()
            if ':' in decrypted_credentials:
                decrypted_username, decrypted_password = decrypted_credentials.split(':')
                return decrypted_username, decrypted_password
            else:
                print("Error: Failed to decrypt password.")
                return None, None
        except InvalidToken as e:
            print("Error: Invalid token. Failed to decrypt password.")
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
    password_manager = PasswordManager(input())

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
