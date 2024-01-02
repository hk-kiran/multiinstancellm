
class User:
    # Class variable to keep track of the unique IDs
    next_id = 1

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.id = User.next_id
        User.next_id += 1

    def __str__(self):
        return f"User ID: {self.id}, Name: {self.name}, Email: {self.email}"
