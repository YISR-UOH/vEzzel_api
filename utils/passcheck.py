


def password_check(passwd):
    val = True
    msg = {}
    if len(passwd) < 8: 
        msg['length_min'] = 'La contraseña debe tener al menos 8 caracteres'
        val = False
          
    if not any(char.isdigit() for char in passwd): 
        msg['digit'] = 'La contraseña debe tener al menos un dígito'
        val = False
          
    if not any(char.isupper() for char in passwd): 
        msg['upper'] = 'La contraseña debe tener al menos una letra mayúscula'
        val = False
          
    if not any(char.islower() for char in passwd): 
        msg['lower'] = 'La contraseña debe tener al menos una letra minúscula'
        val = False
        
    if val: 
        return val 
    else:
      return msg