import os
import json

class CasinoManager:
    def __init__(self, file_path="casino_data.json"):
        self.file_path = file_path
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump({}, f)
        with open(file_path, 'r') as f:
            self.data = json.load(f)

    def save_data(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def make_account(self, user_id):
        if str(user_id) in self.data:
            return None
        self.data[str(user_id)] = {"balance": 10, "games_played": 0, "wins": 0, "losses": 0}
        self.save_data()
        return self.data[str(user_id)]['balance']
    
    def get_balance(self, user_id):
        user_id = str(user_id)
        if str(user_id) not in self.data:
            return None
        return self.data[user_id]['balance']
    
    def update_balance(self, user_id, amount):
        user_id = str(user_id)
        self.get_balance(user_id)
        self.data[user_id]['balance'] += amount
        self.save_data()
        return self.data[user_id]['balance']
    
    def set_balance(self, user_id, amount):
        user_id = str(user_id)
        self.data[user_id] = {"balance": amount}
        self.save_data()