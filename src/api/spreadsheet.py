class Spreadsheet:
  def __init__(self,user_id, name,description,content,tags,tracker):
    '''
      Constructor de la clase Spreadsheet
    '''
    self.user_id = user_id
    self.name = name
    self.description = description
    self.content = content
    self.tags = tags
    self.tracker = tracker
  
  def toDBCollection(self):
    '''
      Estrucutra de la colección de hojas de cálculo en la base de datos
    '''
    return {
      "user_id": self.user_id,
      "name": self.name,
      "description": self.description,
      "content": self.content,
      "tags": self.tags,
      "tracker": self.tracker
    }
