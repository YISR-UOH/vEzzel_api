class User:
  def __init__(self, username, email, password):
    '''
      Constructor de la clase User
    '''
    self.username = username
    self.email = email
    self.password = password
  
  def toDBCollection(self):
    '''
      Estrucutra de la colección de usuarios en la base de datos
    '''
    return {
      "username": self.username,
      "email": self.email,
      "password": self.password
    }