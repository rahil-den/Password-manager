from cryptography.fernet import Fernet # Import the Fernet class from the cryptography library
import os

KEY_FILE = 'key.key' # Path to the key file

def generate_key():
   if not os.path.exists(KEY_FILE): # Check if the key file already exists
         key = Fernet.generate_key() # Generate a new key
         with open(KEY_FILE, 'wb') as key_file: # Write the key to a file
              key_file.write(key) # Save the key to a file
         print("Key generated and saved to key.key")
  
def load_key():
     with open(KEY_FILE, 'rb') as key_file: # Load the key from the file
         return key_file.read() # Return the key
     
def encrypt_passsword(password): # Encrypt the password
     key = load_key() # Load the key
     Fernetk = Fernet(key) # Create a Fernet object
     return Fernetk.encrypt(password.encode()).decode() # Encrypt the password and return it as a string

def decrypt_password(encrypted_passsword): # Decrypt the password
        key = load_key()
        Fernetk = Fernet(key)
        return Fernetk.decrypt(encrypted_passsword.encode()).decode() # Decrypt the password and return it as a string

# Example usage
