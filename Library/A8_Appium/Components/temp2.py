import __init
class parent (): 
  # global b #Vị trí 1: Khai báo biến b là global (Thông với các khai báo global trong các hàm khác)
  b = 5
  c = 8
  
  # def __init__(self):
  #   global b #Vị trí 2: Khai báo biến b là global (Thông với các khai báo global trong các hàm khác)
  #   b = 5 #Lưu ý: b tuy được khai báo trong init nhưng nó không phải self của riêng class này nên không phải self.b = 5
  
  def printHello ():
    # global b #Nếu bên trong hàm có thay đổi giá trị global thì phải khai báo là global để nó thông ra bên ngoài
    parent().b = 88
    print("Increase b value...",parent().b)

    
  class child ():
    def __init__(self):
      pass
    
    def print(self):
      print("Current value of b:",parent().b) #Hàm chỉ tham khảo biến global mà không thay đổi
      print("Current value of c:",parent().c) #Hàm chỉ tham khảo biến global mà không thay đổi



parent_int = parent #Dấu () ở đây là để báo class này có __init__

parent_int.child().print() #child có __init__ nên sử dụng phải có ()
parent_int.printHello()
parent_int.child().print() #child có __init__ nên sử dụng phải có ()
