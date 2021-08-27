import argparse, sys, json
import application
import compiler
import preprocesser

def _error(place, text):
  print("\033[91merror: " + place + ": " + text + "\033[00m")
  sys.exit(0)

def runt(text):
  listelems = []
  elems = text.split("ec")
  for elem in elems:
    if elem == "":
      continue
    try:
      typ = elem[0]
      try:
        com = int(elem[1:3])
      except ValueError:
        _error("runtime", "invalid pom file")
      val = elem[3:]
    except IndexError:
      _error("runtime", "invalid pom file")
    listelems.append([typ, com, val])

  d = {}
  count = 0
  for item in listelems:
    try:
      if item[0] == "i":
        d[count] = [int(item[1]), int(item[2])]
      elif item[0] == "s":
        d[count] = [int(item[1]), str(item[2])]
      elif item[0] == "n":
        d[count] = [int(item[1]), '']
      count += 1
    except ValueError:
      _error("runtime", "invalid pom file")

  m = application.memory()
  m.load(d, autosize=True)
  a = application.emulator(m)
  a.run()

def compilet(itext, output, replaceargs):
  itext = preprocesser.process(itext, replaceargs)

  d = compiler.compile(itext)
  string = ""
  for item in d:
    rstring = ""
    l = d[item]
    c = l[0]
    if len(str(c)) == 1:
      c = "0" + str(c)
    if str(l[1]) == "":
      rstring += "n" + str(c) + "0"
    else:
      if type(l[1]) == int:
        rstring += "i"
      elif type(l[1]) == str:
        rstring += "s"
      rstring += str(c) + str(l[1])
    string += rstring + "ec"

  with open(output, 'w') as file:
    file.write(string)

parser = argparse.ArgumentParser(description="The Pom language compiler and runtime script", allow_abbrev=False, add_help=False)

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('run', action='store', metavar=('run'), help="Run a compiled Pom file", nargs='?', default=None)
group.add_argument('-c', '--compile',  nargs=2, action='store', metavar=('input', 'output'), help="Compile a Pom source code file")
group.add_argument('-pc', '--pom_code',  nargs=1, action='store', metavar=('file'), help="Run a PomCode JSON file")
group.add_argument('-h', '--help', action='store_true', help="List this help menu and exit")
parser.add_argument('-r', '--replace', nargs=2, metavar=('variable', 'value'), action="append", help="Add a preprocesser replace item, only used with -c / --compile")

args = parser.parse_args()
replaceargs = {}

if args.help != False:
  print("""usage: pom [run] [-h] [-c input output] [-pc file] [-r variable value]

PomCode Commands:
  -pc / --pom_code [file] ............ Run a PomCode JSON file

Pom Commands:
  [run] .............................. Run a compiled Pom file
  -c / --compile [input] [output] .... Compile a Pom source code file
  -r / --replace [variable] [value] .. Add a preprocesser replace item, only used with -c / --compile

Misc Commands:
  -h / --help ........................ List this help menu and exit""")

if args.replace != None:
  if args.compile == None:
    parser.error('-rp / --replace can only be used with -c / --compile')
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

if args.run != None:
  try:
    with open(args.run, 'r') as file:
      text = file.read()
  except:
    parser.error('\"' + args.run + '\" file not found')
  runt(text)

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