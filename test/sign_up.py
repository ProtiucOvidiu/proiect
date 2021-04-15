
class Person:
  def __init__(full_name, user_name, email, password, pass_confirm, phone):
    self.full_name = full_name
    self.user_name = user_name
    self.email = email
    self.password = password
    self.pass_confirm = pass_confirm
    self.phone = phone


  def check_pass(password, pass_confirm):
    if pass_confirm != password:
        return false
        
  def insert():
    query = "Insert into sql11402476.users(username,password,full_name,email,phone_number)"
    "values (\"" + user_name + "\", \"" + password + "\", \"" + full_name + "\", \"" 
    + email + "\", \"" + phone + ";"
  
