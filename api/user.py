class User:
  def __init__(self, username, email, password,last_sheet):
    '''
      Constructor de la clase User
    '''
    self.username = username
    self.email = email
    self.password = password
    self.last_sheet = last_sheet
  def toDBCollection(self):
    '''
      Estrucutra de la colección de usuarios en la base de datos
    '''
    return {
      "username": self.username,
      "email": self.email,
      "password": self.password,
      "last_sheet": self.last_sheet
    }