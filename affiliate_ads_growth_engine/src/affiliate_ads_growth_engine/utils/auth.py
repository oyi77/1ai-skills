class TokenManager:
 def __init__(self, token: str):
 self.token = token

 def refresh(self):
 return self.token
