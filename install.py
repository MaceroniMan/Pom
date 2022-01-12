import os, sys, shutil, subprocess

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

print(""" _____              _         _       _ _         
|  _  |___ _____   | |___ ___| |_  __| | |___ ___ 
|   __| . |     |  | |   |_ -|  _||. | | | -_|  _|
|__|  |___|_|_|_|  |_|_|_|___| | |___|_|_|___|_|  
                             |__|                 """)

log("starting module install...")

try:
  with open(".pip_output", "w") as pipOut:
    outputv = subprocess.run([sys.executable, "-m", "pip", "install", "."], stdout=pipOut, stderr=pipOut)
except KeyboardInterrupt:
  os.remove(".pip_output")
  print("")
  log("pip install failed, keyboard interrupt")
  sys.exit()

if str(outputv.returncode) == "0":
  log("done")
else:
  log("pip install failed, see '.pip_output'")
  sys.exit()

log("cleaning up...")
os.remove(".pip_output")
log("done\n")

log("starting pom install...")
try:
  install()
except PermissionError:
  log("failed to create exec, please run command with 'sudo'")