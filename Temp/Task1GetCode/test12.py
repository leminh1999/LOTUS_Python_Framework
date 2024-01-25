from Global.loggingSetup import *
import logging
class indentMan():
  def __init__(self,treeEna=1,autoNum = 0):
    self.level = 1
    self.tree = "|_"
    self.treeEna = treeEna
    self.autoNum = autoNum
    
  def inc(self):
    self.level += 1
    self.indentStringGen()
  def dec(self):
    self.level -= 1
    self.indentStringGen()
  def indentStringGen(self):
    if self.treeEna == 1:
      self.tree = ""
      while self.level > 1:
        self.tree += "| "
        self.level -= 1
      self.tree += "|_"
    else:
      self.tree = ""
  def gen(self):
    # if self.autoNum == 0:
      return self.tree
    # else:
      
    
indent = indentMan()
aaa = "JUBEI"
logger.info(indent.gen()+"HELLO1 %s",aaa)
indent.inc()
logger.info("%sHELLO 2",indent.gen())
indent.dec()
logger.info("%sHELLO  3",indent.gen())
