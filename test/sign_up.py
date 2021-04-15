
class Person:
  def __init__(self, full_name, user_name, email, phone, password, pass_confirm):
    self.full_name = full_name
    self.user_name = user_name
    self.email = email
    self.phone = phone
    self.password = password
    self.pass_confirm = pass_confirm



  def check_pass(password, pass_confirm):
    if pass_confirm != password:
        return false

  def insert():
    query = "Insert into sql11402476.users(username,password,full_name,email,phone_number)"
    "values (\"" + user_name + "\", \"" + password + "\", \"" + full_name + "\", \"" 
    + email + "\", \"" + phone + ";"
    return query

  def __repr__(self): 
        return "Test user_name:% s password:% s" % (self.user_name, self.password) 
  
