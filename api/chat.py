from datetime import datetime

class Chat:
  def __init__(self,user1_id,user1_name,user2_id,user2_name, msg):
    '''
      Constructor de la clase Spreadsheet
    '''
    self.user1_id = user1_id
    self.user1_name = user1_name
    self.user2_id = user2_id
    self.user2_name = user2_name
    self.msg = msg
    now = datetime.now()
    self.time = now.strftime("%Y%m%d%H%M%S%f")
  
  def toDBCollection(self):
    '''
      Estrucutra de la colección de hojas de cálculo en la base de datos
    '''
    return {
      "users": [[self.user1_id,self.user1_name],[self.user2_id,self.user2_name]],
      "msg": [[self.user1_id,self.msg,self.time]],
      "time": self.time
    }
