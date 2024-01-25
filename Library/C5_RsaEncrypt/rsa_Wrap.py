import __init
import rsa #pip install rsa
import os

class RSA_Class():
  def __init__(self, publicKeyPath:str="",privateKeyPath:str=""):
    self.publicKeyPath = publicKeyPath
    self.privateKeyPath = privateKeyPath
    if os.path.exists(self.publicKeyPath):
      with open(self.publicKeyPath, mode='rb') as publicfile:
          keydata = publicfile.read()
          self.publicKey = rsa.PublicKey.load_pkcs1(keydata)
    else:
      self.publicKey = None
    if os.path.exists(self.privateKeyPath):
      with open(self.privateKeyPath, mode='rb') as privatefile:
          keydata = privatefile.read()
          self.privateKey = rsa.PrivateKey.load_pkcs1(keydata)
    else:
      self.privateKey = None
    
  def generateKeyPair(self, filePrefix="key",saveDir="./"):
    self.publicKey, self.privateKey = rsa.newkeys(2048)
    #save private key and public key to file
    with open(f'{saveDir}/{filePrefix}_private.pem', mode='wb') as privatefile:
        privatefile.write(self.privateKey.save_pkcs1())
    with open(f'{saveDir}/{filePrefix}_public.pem', mode='wb') as publicfile:
        publicfile.write(self.publicKey.save_pkcs1())

  def encrypt(self, message:str):
    # rsa.encrypt method is used to encrypt
    # string with public key string should be
    # encode to byte string before encryption
    # with encode method
    encMessage = rsa.encrypt(message.encode(),self.publicKey)
    return encMessage
  
  def decrypt(self, encMessageBinaryString:str):
    # the encrypted message can be decrypted
    # with ras.decrypt method and private key
    # decrypt method returns encoded byte string,
    # use decode method to convert it to string
    # public key cannot be used for decryption
    decMessage = rsa.decrypt(encMessageBinaryString, self.privateKey).decode()
    return decMessage