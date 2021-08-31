import os, sys, shutil

def getLocation():
  if os.name == "nt":
    return os.path.join("\\".join(sys.executable.split("\\")[:-1]), "Scripts")
  else:
    return "/".join(sys.executable.split("/")[:-1])

def log(text):
  print("log: " + text)

def install():
  path = getLocation()
  if os.name == "nt":
    log("non-posix operating system detected")
    log("moving executable...")
    shutil.move("installer\\pom.bat", os.path.join(path, "pom.bat"))
    log("done")
  else:
    log("posix operating system detected")
    log("moving executable...")
    shutil.move("installer/pom.sh", os.path.join(path, "pom"))
    log("done")
    log("setting permissions...")
    os.system("chmod 777 " + os.path.join(path, "pom"))
    log("done")
  log("cleaning up...")
  shutil.rmtree("pom")
  shutil.rmtree("installer")
  os.remove("install.py")
  os.remove("setup.py")
  log("done (enter to finish installer)")
  input()

log("starting pom install...")
install()