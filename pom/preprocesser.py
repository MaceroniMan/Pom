import re, sys, string

alphabets = string.ascii_lowercase + string.ascii_lowercase.upper() + "1234567890_"

def _error(text, word, line, linet, start):
  if len(word) < 1:
    word = "  "
  text = text.split(":")
  print("\033[1;91m" + text[0] + " on line " + str(line+1) + ":" + ":".join(text[1:]))
  print("\033[00m" + linet)
  print(((len(start))-len(word))*" " + "\033[1;32m" + (len(word))*"^" + "\033[00m")
  print()
  sys.exit(1)

def _get_length(span):
  return span[1]-span[0]

def _getline(text, char):
  lines = text.split("\n")
  line = 0
  linechar = 0
  for i in range(char):
    if linechar == len(lines[line]):
      line += 1
      linechar = 0
    else:
      linechar += 1
  return line, linechar

def process(text, replaceArgs):
  for item in replaceArgs:
    for char in item:
      if char in alphabets:
        pass
      else:
        print("\033[1;91mpreproc error: replace argument '" + item + "' contains non-alphabet charecters\033[00m")
        sys.exit(1)
  p = re.compile("({{\s*(?P<word>\w+)\s*}})")
  matches = p.finditer(text)
  replacem = []
  for match in matches:
    if match.group('word') in replaceArgs:
      replacem.append(match)
    else:
      linen, linechar = _getline(text, match.span()[0])
      _error("preproc error: a preprocesser directive was left unchanged", _get_length(match.span())*" ", linen, text.split("\n")[linen], (linechar+_get_length(match.span()))*" ")
  for match in replacem:
    text = text.replace(match.group(0), replaceArgs[match.group('word')])
  return text