from System.auth.login import authenticate


username = input("Username: ")
password = input("Password: ")

user = authenticate(username, password)

if user:
    print("Login successful!")
    print("Username:", user["username"])
    print("Admin:", user["is_admin"])
else:
    print("Invalid username or password.")