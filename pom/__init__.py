from pom.compiler import compile
from pom.application import memory
from pom.application import emulator

import os
import sys

def exeLocation(checkinstall=True):
  if os.name == "nt":
    path = os.path.join("\\".join(sys.executable.split("\\")[:-1]), "Scripts", "pom.bat")
  else:
    path = os.path.join("/".join(sys.executable.split("/")[:-1]), "pom")

  if checkinstall:
    if os.path.exists(path):
      return path
    else:
      return None
  else:
    return path

def preLoad(pomcode):
  if type(pomcode) != dict:
    raise TypeError("'pomcode' argument must be a dictionary")
  else:
    m = memory()
    m.load(pomcode, autosize=True)
    a = emulator(m)
    a.run()