import io, urllib.request, os, sys, os.path, subprocess

def __dobytes(value, sub=0, ending=True):
  bvalues = ["b", "kb", "mb", "gb", "tb", "pb", "eb", "zb", "yb"]
  n = value / 1024
  if n >= 1:
    if n >= 1024:
      return __dobytes(n, sub+1)
    else:
      if ending:
        return str(round(n, 1)) + " " + str(bvalues[sub+1])
      else:
        return str(round(n, 1))
  else:
    if ending:
      return str(value) + " " + str(bvalues[sub])
    else:
      return str(value)

def download(url, filelocation, customtext=""):
  try:
    res = urllib.request.urlopen(url)
  except:
    print("404 not found error")
    return "404"
  length = res.getheader("content-length")

  if length:
    length = int(length)
    blocksize = max(4096, length // round(os.get_terminal_size().columns / 2))
  else:
    blocksize = 1000000
    print("cannot get total size, no loading bar present", end="")

  bufferall = io.BytesIO()
  size = 0
  while True:
    currentbuffer = res.read(blocksize)
    if not currentbuffer:
      break
    bufferall.write(currentbuffer)
    size += len(currentbuffer)

    if length:
      percent = float(size / length)
      width = round(os.get_terminal_size().columns / 2)
      
      sys.stdout.write("\r[" + "#"*(round(percent*width)) + " "*round(width-(percent*width)) + "] " + __dobytes(size, ending=False) + "/" + __dobytes(length) + " " + customtext)
      sys.stdout.flush()

  print()


  if filelocation == None:
    return bufferall.getvalue()
  else:
    with open(filelocation, 'wb') as file:
      file.write(bufferall.getvalue())

  return "200"

def mkdirs(paths):
  dirpath = '/'.join(paths.split('/')[:-1])
  try:
    os.makedirs(dirpath)
  except:
    pass

# start script here:

t = download("https://raw.githubusercontent.com/MaceroniMan/Pom/master/install.py", None, "Getting File List...")

allfiles = t.decode("utf-8").split("\n")

for line in range(len(allfiles)):
  mkdirs(os.path.join(os.getcwd(), allfiles[line]))
  download("https://raw.githubusercontent.com/MaceroniMan/Pom/master" + allfiles[line], allfiles[line], str(line) + " of " + str(len(allfiles)))

subprocess.run([sys.executable, "install.py"])