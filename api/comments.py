from datetime import datetime

class Comments:
  def __init__(self,spread_id,user_id,comment,score,username,spreadname):
    '''
      Constructor de la clase comments
    '''
    self.spread_id = spread_id
    self.user_id = user_id
    self.username = username
    self.spreadname = spreadname
    self.comment = comment
    self.score = score
    now = datetime.now()
    self.last_modified = now.strftime("%Y%m%d%H%M%S%f")
  
  def toDBCollection(self):
    '''
      Estrucutra de la colección de hojas de cálculo en la base de datos
    '''
    return {
      "spread_id": self.spread_id,
      "user_id": self.user_id,
      "username": self.username,
      "spreadname": self.spreadname,
      "comment": self.comment,
      "score": self.score,
      "last_modified": self.last_modified
    }