import sys
import json
import argparse
import urllib.request
try:
  import application
  import compiler
  import preprocesser
except:
  import pom.application as application
  import pom.compiler as compiler
  import pom.preprocesser as preprocesser

VERSION = "1.5"

def webversion():
  version = None
  try:
    with urllib.request.urlopen('https://raw.githubusercontent.com/MaceroniMan/Pom/master/README.md') as response:
      html = response.read().decode("ascii")
      lines = html.split("\n")
      for line in lines:
        if line.startswith("# Version"):
          version = line.split(" ")[2]
  except:
    print("Failed to check version")
    return
  if float(version) > float(VERSION):
    print("Out of date, current version: " + version)
  else:
    print("Up to date with current version")

def compilet(itext, output, replaceargs):
  itext = preprocesser.process(itext, replaceargs)

  dictionary, warnings = compiler.compile(itext)
  byte_arr = []
  for num in dictionary:
    item = dictionary[num]
    byte_arr.append(ord(str(item[0])))
    if item[1] == "":
      byte_arr.append(254)
    else:
      if type(item[1]) == str:
        byte_arr.append(253)
      else:
        byte_arr.append(252)
      for char in str(item[1]):
        byte_arr.append(ord(str(char)))
    byte_arr.append(255)
    
  with open(output, 'w+b') as file:
    file.write(bytearray(byte_arr))

  print("\033[0;32mcompiler finished with " + str(warnings) + " warning" + "s"*((warnings!=1)*1) + ", output executable in '" + output +"'\033[00m")
  
def runt(filename, start=True):
  dictionary = {}
  with open(filename, 'r+b') as file:
    byte_arr = list(file.read())
    second = ''
    first = ''
    number = 0
    vtype = ''
    for entry in byte_arr:
      if entry == 255:
        if vtype == "string":
          dictionary[number] = [first, str(second)]
        elif vtype == "number":
          dictionary[number] = [first, int(second)]
        number += 1
        first = ''
        second = ''
      else:
        if first == '':
          first = int(chr(entry))
        elif entry == 254:
          second += ''
          vtype = "string"
        elif entry == 253:
          vtype = "string"
        elif entry == 252:
          vtype = "number"
        else:
          second += chr(entry)

  if start:
    m = application.memory()
    m.load(dictionary, autosize=True)
    a = application.emulator(m)
    a.run()
  else:
    return dictionary
  
def shell():
  while True:
    try:
      instr = input("...")
      if instr == ":run":
        return compiler._shell_compile()
      elif instr == ":ext":
        print("ShellExit")
        sys.exit()
      else:
        compiler._shell(instr)
    except KeyboardInterrupt:
      print("\nKeyboardInterrupt")
    except EOFError:
      print("\nShellExit")
      sys.exit()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(prog="pom", description="The Pom language compiler and runtime script", allow_abbrev=False, add_help=False)

  group = parser.add_mutually_exclusive_group()
  group.add_argument('run', action='store', metavar=('run'), help="Run a compiled Pom file", nargs='?', default=None)
  group.add_argument('-c', '--compile',  nargs=2, action='store', metavar=('input', 'output'), help="Compile a Pom source code file")
  group.add_argument('-pc', '--pom_code',  nargs=1, action='store', metavar=('file'), help="Run a PomCode JSON file")
  group.add_argument('-h', '--help', action='store_true', help="List this help menu and exit")
  group.add_argument('-v', '--version', action='store_true', help="List the current Pom version")
  group.add_argument('-up', '--unparse', nargs=2, metavar=('input', 'output'), action="store", help="Turn a pom executable into a PomCode json file")
  parser.add_argument('-r', '--replace', nargs=2, metavar=('variable', 'value'), action="append", help="Add a preprocesser replace item, only used with -c / --compile")
  parser.add_argument('-vb', '--verbose', action='store_true', help="Adds detail to the output of some operations, only used with -v / --version and -up / --unparse")

  args = parser.parse_args()
  replaceargs = {}
  verbose = None

  if args.verbose != False:
    if args.unparse == None and args.version == False:
      parser.error('-vb / --verbose can only be used with -up / --unparse or -v / --version')
    verbose = 2
  
  if args.version != False:
    print("Pom Version " + VERSION)
    if verbose != None:
      webversion()
  
  if args.help != False:
    print("""usage: pom [run] [-h] [-v] [-c input output] [-pc file] [-r variable value] [-pp]

PomCode Commands:
  -pc / --pom_code [file] ............ Run a PomCode JSON file

Pom Commands:
  [run] .............................. Run a compiled Pom file
  -c / --compile [input] [output] .... Compile a Pom source code file
  -r / --replace [variable] [value] .. Add a preprocesser replace item, only used with -c / --compile

Misc Commands:
  -h / --help ........................ List this help menu and exit
  -v / --version ..................... List the current Pom version
  -up / --unparse [input] [output] ... Turn a pom executable into a PomCode json file
  -vb / --verbose .................... Output of the unparse operation pretty, only if used with -up / --unparse
                                       Prints more version info, only if used with -v / --version""")

  if len(sys.argv) == 1:
    print("Pom Shell v" + VERSION)
    print("Type \":run\" to run the code, \":ext\" or \"ctrl-d\" to exit the Shell")
    out = shell()
    m = application.memory()
    m.load(out, autosize=True)
    a = application.emulator(m)
    a.run()
  
  if args.replace != None:
    if args.compile == None:
      parser.error('-r / --replace can only be used with -c / --compile')
    for i in args.replace:
      if i[0] in replaceargs:
        print("warning: key \"" + i[0] +  "\" already exists")
      replaceargs[i[0]] = i[1]
  
  if args.compile != None:
    try:
      with open(args.compile[0], 'r') as file:
        text = file.read()
    except:
      parser.error('\"' + args.compile[0] + '\" file not found')

    compilet(text, args.compile[1], replaceargs)

  if args.unparse != None:
    try:
      open(args.unparse[0]).close()
    except:
      parser.error('\"' + args.unparse[0] + '\" file not found')
    rdictionary = runt(args.unparse[0], False)

    if verbose:
      print("unparse: pretty printing " + args.unparse[1])
    
    with open(args.unparse[1], 'w') as file:
      file.write(json.dumps(rdictionary, indent=verbose))
  
  if args.run != None:
    try:
      open(args.run).close()
    except:
      parser.error('\"' + args.run + '\" file not found')
    runt(args.run)
  
  if args.pom_code != None:
    try:
      with open(args.pom_code[0], 'r') as file:
        jsond = json.loads(file.read())
    except:
      parser.error('\"' + args.pom_code[0] + '\" file not found or invalid JSON')
  
    m = application.memory()
    m.load(jsond, autosize=True)
    a = application.emulator(m)
    a.run()