import sys, string, os

variables = {}
variablel = []
values = []
actions = []
jumps = {}

alphabets = string.ascii_lowercase + string.ascii_lowercase.upper() + "1234567890_"
ops = {"==":1,"!=":2,"<<":3,">>":4,"<=":5,">=":6}
maths = ["+", "-", "*", "/"]
bscs = ["n"]

def _error(text, word, line, linet, start):
  if len(word) < 1:
    word = "  "
  text = text.split(":")
  if os.name == 'nt':
    print(text[0] + " on line " + str(line+1) + ":" + ":".join(text[1:]))
    print(linet)
    print(((len(start))-len(word))*" " + (len(word))*"^")
  else:
    print("\033[1;91m" + text[0] + " on line " + str(line+1) + ":" + ":".join(text[1:]))
    print("\033[00m" + linet)
    print(((len(start))-len(word))*" " + "\033[1;32m" + (len(word))*"^" + "\033[00m")
  print()
  sys.exit(1)

def _is_int(string):
  try:
    int(string)
    return True
  except:
    return False

def _get_type(string):
  string = str(string)
  if string[0] == "\"":
    if string == "\"":
      return "starts"
    elif string[-1] == "\"":
      return "string"
    else:
      return "starts"
  elif _is_int(string):
    return "int"
  elif string in variables:
    return "var"
  elif string in ["==", "!="]:
    return "operator"
  elif string in [">>", "<<", ">=", "<="]:
    return "int_operator"
  elif string in maths:
    return "math_symbol"
  elif string[0] == ":":
    if string[1:] in ["string", "int"]:
      return "internal_type"
    else:
      return "_e_type"
  else:
    bad = False
    for char in string:
      if char in alphabets:
        pass
      else:
        bad = True
    if bad:
      return "_e_notvar"
    return "_e_none"

def _parse_line(line, linen):
  ctype = "null"
  command = []
  mlength = 0
  
  if line[-1][-1] == ";":
    _error("syntax error: cannot have semi-colons at the end of a line", line[0].split(":")[1], linen, " ".join(line), " ".join(line))

  if line[0] == "@if":
    ctype = "if"
  elif line[0] == "@type":
    ctype = "type"
  elif line[0][0] == "@":
    ctype = "func"
    command.append(line[0][1:])
  elif len(line[0].split(":")) >= 2:
    ctype = "variable"
    fcommand = line[0].split(":")
    if fcommand[0] == "int":
      command.append("int")
      if fcommand[1] == "~":
        command.append(str(fcommand[1]))
      elif fcommand[1] == "":
        _error("syntax error: length descriptor field cannot be left empty", ":", linen, " ".join(line), fcommand[0]+":")
      elif _is_int(fcommand[1]):
        command.append(int(fcommand[1]))
      else:
        _error("value error: length descriptor must be int", fcommand[1], linen, " ".join(line), fcommand[0] + ":" + fcommand[1])
    elif fcommand[0] == "string":
      command.append("string")
      if fcommand[1] == "~":
        command.append(str(fcommand[1]))
      elif fcommand[1] == "":
        _error("syntax error: length descriptor field cannot be left empty", ":", linen, " ".join(line), fcommand[0]+":")
      elif _is_int(fcommand[1]):
        command.append(int(fcommand[1]))
      else:
        _error("value error: length descriptor must be int", fcommand[1], linen, " ".join(line), fcommand[0] + ":" + fcommand[1])
    else:
      if fcommand[0] == "":
        _error("syntax error: cannot have blank type field", ":", linen, " ".join(line), "")
      else:
        _error("syntax error: variable type " + fcommand[0] + " does not exist", fcommand[0], linen, " ".join(line), "")
  elif line[0] in variables:
    do = True
    for item in maths:
      if item in line:
        if variables[line[0]][2] == "int":
          mlength = variables[line[0]][3]
          ctype = "math"
          command.append(line[0])
          do = False
          break
        else:
          _error("syntax error: cannot do math on a non-int variable", line[0], linen, " ".join(line), line[0])
    if do:
      mlength = variables[line[0]][3]
      ctype = "reset"
      command.append(line[0])
  elif _get_type(line[0]) == "_e_none":
    _error("syntax error: variable does not exist", line[0], linen, " ".join(line), "")
  else:
    _error("syntax error: cannot parse keyword", line[0], linen, " ".join(line), "")

  next_r = False
  rstring = False
  value = False
  intcompare = False
  rstring_t = ""
  assemble = line[0]
  nline = line[1:]
  text = ""

  for item in range(len(nline)):
    if nline[item] == "":
      assemble += " "
      continue
    if nline[item][0] == "#":
      if not rstring:
        break
    assemble += " " + nline[item]
    text = nline[item]
    if ctype == "func":
      if rstring:
        if text[-1] == "\"":
          rstring_t += " " + text[:-1]
          command.append(rstring_t)
          rstring = False
        else:
          rstring_t += " " + text
      elif text == "<":
        if len(command) == 2 and command[0] in ["jump", "input"]:
          _error("forward error: cannot forward more than one value with " + command[0] + " function", text, linen, " ".join(line), assemble)
        elif len(command) == 1 and command[0] in ["exit", "flush"]:
          _error("forward error: " + command[0] + " cannot take parameters", text, linen, " ".join(line), assemble)
        if next_r == True:
          _error("forward error: cannot forward a forward", text, linen, " ".join(line), assemble)
        else:
          next_r = True
      elif next_r:
        gtype = _get_type(text)
        if gtype == "string":
          command.append(text[1:-1])
        elif gtype == "int":
          command.append(int(text))
        elif gtype == "starts":
          rstring_t = text[1:]
          rstring = True
        elif gtype == "var":
          if command[0] == "jump":
            _error("value error: cannot use variable for jump function", text, linen, " ".join(line), assemble)
          else:
            command.append(variables[text])
        else:
          if command[0] == "jump":
            _error("value error: cannot use variable for jump function", text, linen, " ".join(line), assemble)
          else:
            _error("value error: variable does not exist", text, linen, " ".join(line), assemble)
        next_r = False
      else:
        _error("forward error: must have forward between values", text, linen, " ".join(line), assemble)
    elif ctype == "if":
      if rstring:
        if text[-1] == "\"":
          rstring_t += " " + text[:-1]
          command.append(rstring_t)
          rstring = False
        else:
          rstring_t += " " + text
      elif text == "<":
        if len(command) == 5:
          _error("forward error: if function only takes 2 forwards", text, linen, " ".join(line), assemble)
        if len(command) >= 3:
          if next_r == True:
            _error("forward error: cannot forward a forward", text, linen, " ".join(line), assemble)
          else:
            next_r = True
        else:
          _error("forward error: cannot forward a value before conditional is over", text, linen, " ".join(line), assemble)
      elif len(command) < 3 or next_r:
        gtype = _get_type(text)
        if gtype == "string":
          if intcompare and not next_r:
            _error("type error: operator type does not match value type", text, linen, " ".join(line), assemble)
          command.append(text[1:-1])
        elif gtype == "operator":
          if len(command) < 3:
            command.append(text)
          else:
            _error("value error: cannot use operator outside a conditional", text, linen, " ".join(line), assemble)
        elif gtype == "int_operator":
          if len(command) < 3:
            if type(command[0]) == list:
              if command[0][2] != "int":
                _error("type error: previous variable type does not match operator type", text, linen, " ".join(line), assemble)
            else:
              if _get_type(command[0]) != "int":
                _error("type error: previous value type does not match operator type", text, linen, " ".join(line), assemble)
            intcompare = True
            command.append(text)
          else:
            _error("value error: cannot use operator outside a conditional", text, linen, " ".join(line), assemble)
        elif gtype == "int":
          command.append(int(text))
        elif gtype == "starts":
          if intcompare and not next_r:
            _error("type error: operator type does not match value type", text, linen, " ".join(line), assemble)
          rstring_t = text[1:]
          rstring = True
        elif gtype == "var":
          if not next_r:
            if intcompare:
              if variables[text][2] != "int":
                _error("type error: operator type does not match variable type", text, linen, " ".join(line), assemble)
            command.append(variables[text])
          else:
            _error("value error: cannot use variable for jump placement", text, linen, " ".join(line), assemble)
        elif gtype == "_e_notvar":
          _error("type error: invalid value type", text, linen, " ".join(line), assemble)
        else:
          _error("value error: variable does not exist", text, linen, " ".join(line), assemble)
        next_r = False
      else:
        _error("forward error: must have forward between values", text, linen, " ".join(line), assemble)
    elif ctype == "variable":
      if rstring:
        if text[-1] == "\"":
          rstring_t += " " + text[:-1]
          if command[1] == "~":
            command.append(rstring_t)
          else:
            if len(rstring_t) > command[1]:
              _error("value error: added value is too long", text, linen, " ".join(line), assemble)
            else:
              command.append(rstring_t)
          rstring = False
        else:
          rstring_t += " " + text
          if not command[1] == "~":
            if len(rstring_t) > command[1]:
              _error("value error: value is too long", text, linen, " ".join(line), assemble)
      elif text == "<":
        if value == False:
          _error("name error: name cannot be a forward", text, linen, " ".join(line), assemble)
        else:
          if next_r == True:
            _error("forward error: can only forward once", text, linen, " ".join(line), assemble)
          else:
            next_r = True
      elif next_r:
        gtype = _get_type(text)
        if (gtype == "starts" and command[0] == "string") or command[0] == gtype:
          if gtype == "string":
            if command[1] == "~":
              command.append(text[1:-1])
            else:
              if len(text[1:-1]) > command[1]:
                _error("value error: value is too long", text, linen, " ".join(line), assemble)
              else:
                command.append(text[1:-1])
          elif gtype == "int":
            con = False
            if command[1] == "~":
              con = True
            else:
              if len(text) > command[1]:
               _error("value error: value is too long", text, linen, " ".join(line), assemble)
              else:
                con = True
            if con:
              if len(command) == 4:
                _error("forward error: cannot forward type 'int'", text, linen, " ".join(line), assemble)
              else:
                command.append(int(text))
          elif gtype == "starts":
            rstring_t = text[1:]
            rstring = True
          next_r = False
        else:
          if gtype in ["var", "_e_none"]:
            _error("type error: cannot use variables in defign statement", text, linen, " ".join(line), assemble)
          else:
            if gtype == "_e_notvar": # check if the variable syntax is wrong
              _error("type error: invalid value type", text, linen, " ".join(line), assemble)
            else:
              _error("type error: type declaration does not match value type", text, linen, " ".join(line), assemble)
      elif next_r == False and value == False:
        gtypes = _get_type(text)
        if gtypes == "_e_none":
          value = True
          command.append(text)
        elif gtypes == "var":
          _error("syntax error: cannot redefign a variable", text, linen, " ".join(line), assemble)
        elif gtypes == "_e_notvar": # check if the variable syntax is wrong
          _error("type error: invalid value type", text, linen, " ".join(line), assemble)
        else:
          _error("syntax error: must use a variable type", text, linen, " ".join(line), assemble)
      else:
        _error("syntax error: must forward value", text, linen, " ".join(line), assemble)
    elif ctype == "reset":
      var = variables[command[0]]
      if rstring:
        if text[-1] == "\"":
          rstring_t += " " + text[:-1]
          if len(rstring_t) > mlength:
            _error("value error: value is too long", text, linen, " ".join(line), assemble)
          else:
            mlength -= len(rstring_t)
            command.append(rstring_t)
          rstring = False
        else:
          rstring_t += " " + text
          if len(rstring_t) > mlength:
            _error("value error: value is too long", text, linen, " ".join(line), assemble)
      elif text == "<":
        if next_r == True:
          _error("forward error: can only forward once", text, linen, " ".join(line), assemble)
        else:
          next_r = True
      elif next_r:
        gtype = _get_type(text)
        if gtype != 'var':
          if gtype != var[2]:
            _error("type error: type declaration does not match value type", text, linen, " ".join(line), assemble)
        if gtype == "string":
          if len(text[1:-1]) > mlength:
            _error("type error: value is too long", text, linen, " ".join(line), assemble)
          else:
            mlength -= len(text[1:-1])
            command.append(text[1:-1])
        elif gtype == "int":
          if len(text) > mlength:
            _error("type error: value is too long", text, linen, " ".join(line), assemble)
          else:
            if len(command) == 2:
              _error("forward error: cannot forward type 'int'", text, linen, " ".join(line), assemble)
            else:
              mlength -= len(text)
              command.append(int(text))
        elif gtype == "starts":
          rstring_t = text[1:]
          rstring = True
        elif gtype == "var":
          nvar = variables[text]
          if nvar[2] == var[2]:
            if var[2] == "int" and len(command) == 2:
              _error("type error: cannot forward variable type 'int'", text, linen, " ".join(line), assemble)
            else:
              command.append(nvar)
          else:
            _error("type error: type declaration does not match variable type", text, linen, " ".join(line), assemble)
        else:
          _error("type error: invalid value type", text, linen, " ".join(line), assemble)
        next_r = False
      else:
        _error("syntax error: must forward value", text, linen, " ".join(line), assemble)
    elif ctype == "type":
      if text == "<":
        if value == False:
          _error("name error: variable cannot be a forward", text, linen, " ".join(line), assemble)
        else:
          if next_r == True:
            _error("forward error: can only forward once", text, linen, " ".join(line), assemble)
          else:
            next_r = True
      elif next_r:
        gtype = _get_type(text)
        if gtype == "internal_type":
          command.append(text[1:])
        elif gtype == "_e_type":
          _error("value error: " + text[1:] + " is not a valid internals type", text, linen, " ".join(line), assemble)
        else:
          _error("value error: invalid type, internals type expected", text, linen, " ".join(line), assemble)
        next_r = False
      elif next_r == False and value == False:
        gtypes = _get_type(text)
        if gtypes == "_e_none":
          _error("value error: variable does not exist", text, linen, " ".join(line), assemble)
        elif gtypes == "var":
          value = True
          command.append(text)
        elif gtypes == "_e_notvar": # check if the variable syntax is wrong
          _error("type error: invalid value type", text, linen, " ".join(line), assemble)
        else:
          _error("syntax error: must use a variable type", text, linen, " ".join(line), assemble)
      else:
        _error("syntax error: must forward a internals type", text, linen, " ".join(line), assemble)
    elif ctype == "math":
      var = variables[command[0]]
      if text == "<":
        if value:
          _error("forward error: cannot forward more values for math", text, linen, " ".join(line), assemble)
        elif len(command) >= 2:
          _error("forward error: can only forward once", text, linen, " ".join(line), assemble)
        else:
          next_r = True
      elif text in maths:
        if next_r:
          _error("syntax error: must have value before using symbol", text, linen, " ".join(line), assemble)
        elif value:
          _error("syntax error: cannot have multiple math symbols", text, linen, " ".join(line), assemble)
        else:
          value = True
          command.append(text)
      elif next_r or value:
        if len(command) == 4:
          _error("syntax error: cannot do math with more than 2 items", text, linen, " ".join(line), assemble)
        gtype = _get_type(text)
        if gtype == "string":
          _error("type error: cannot do math with non-int values", text, linen, " ".join(line), assemble)
        elif gtype == "int":
          command.append(int(text))
        elif gtype == "starts":
          _error("type error: cannot do math with non-int values", text, linen, " ".join(line), assemble)
        elif gtype == "var":
          nvar = variables[text]
          if nvar[2] == "int":
            if var[2] == "int" and len(command) == 2:
              _error("type error: cannot forward variable type 'int'", text, linen, " ".join(line), assemble)
            else:
              command.append(nvar)
          else:
            _error("type error: cannot do math with non-int variables", text, linen, " ".join(line), assemble)
        elif gtype == "_e_none":
          _error("syntax error: variable does not exist", text, linen, " ".join(line), assemble)
        else:
          _error("type error: invalid value type", text, linen, " ".join(line), assemble)
        next_r = False
      else:
        if _get_type(text) != "_e_nothing" and len(command) == 1:
          _error("forward error: must forward the value", text, linen, " ".join(line), assemble)
        else:
          _error("syntax error: must have math symbol between values", text, linen, " ".join(line), assemble)

  if next_r:
    _error("forward error: must forward a value", text, linen, " ".join(line), assemble)

  if rstring:
    _error("type error: string must end in \"", text, linen, " ".join(line), assemble)
  
  if command == []:
    _error("syntax error: cannot parse line", " ".join(line), linen, " ".join(line), "")
  
  if ctype == "func":
    # 1 command, 2 value, 3 command (changing, compiler only), 4 command (changing, compiler only)
    if command[0] == "print":
      count = 0
      start = len(values)
      for item in command[1:]:
        if type(item) == list:
          for thing in range(item[0], item[1]):
            actions.append([1, 8])
            actions.append([3, thing])
        else:
          hold = ""
          for char in item:
            if char == "\\":
              hold += char
              continue
            if hold != "":
              if char in bscs:
                hold += char
                values.append([2, hold])
                hold = ""
              else:
                values.append([2, hold])
                actions.append([1, 8])
                actions.append([2, count+start])
                count += 1
                values.append([2, char])
            else:
              values.append([2, char])
            actions.append([1, 8])
            actions.append([2, count+start])
            count += 1
    elif command[0] == "input":
      if type(command[1]) == list:
        if command[1][2] == "string":
          actions.append([1, 10])
          actions.append([3, command[1][0]])
          actions.append([2, command[1][3]])
        else:
          _error("type error: variable must be a string", text, linen, " ".join(line), assemble)
      else:
        _error("type error: input function parameter must be a variable", text, linen, " ".join(line), assemble)
    elif command[0] == "jump":
      if len(command) != 2:
        _error("forward error: must forward a value", line[0], linen, " ".join(line), "")
      actions.append([1, 3])
      actions.append([5, command[1], text, linen, " ".join(line), assemble])
    elif command[0] == "flush":
      actions.append([1, 9])
    elif command[0] == "exit":
      actions.append([1, 0])
    else:
      _error("syntax error: not a valid function", line[0], linen, " ".join(line), "")
  
  elif ctype == "variable":
    startn = len(variablel)
    if len(command) == 3:
      if command[1] == "~":
        _error("syntax error: cannot auto-set a blank variable", text, linen, " ".join(line), assemble)
      joinv = ""
    elif command[0] == "int":
      joinv = str(command[3])
    else:
      joinv = "".join(command[3:])
    if command[1] == "~":
      length = len(joinv)
    else:
      if len(joinv) > command[1]:
        _error("type error: forwarded value is too long", text, linen, " ".join(line), assemble)
      else:
        length = command[1]

    for i in range(length):
      if i < len(joinv):
        if command[0] == "int":
          if joinv[i] in ["-", "."]:
            variablel.append([2, joinv[i]])
          else:
            variablel.append([2, int(joinv[i])])
        else:
          variablel.append([2, joinv[i]])
      else:
        variablel.append([2, ''])
    variables[command[2]] = [startn, len(variablel), command[0], length]

  elif ctype == "reset":
    var = variables[command[0]]

    if var[2] == "int":
      if type(command[1]) == list:
        ivar = command[1]
        #if ivar[3] > var[3]:
        #  _error("type error: forwarded value is too long", text, linen, " ".join(line), assemble)
        #else:
        for i in range(ivar[3]):
          actions.append([1, 1])
          actions.append([3, ivar[0]+i])
          if i < ivar[3]:
            actions.append([3, var[0]+i])
          else:
            actions.append([2, ''])
      else:
        joinv = str(command[1])
        #if len(joinv) > var[3]:
        #  _error("type error: forwarded value is too long", text, linen, " ".join(line), assemble)
        #else:
        for i in range(var[3]):
          actions.append([1, 2])
          actions.append([3, var[0]+i])
          if i < len(joinv):
            if joinv[i] in ["-", "."]:
              actions.append([2, joinv[i]])
            else:
              actions.append([2, int(joinv[i])])
          else:
            actions.append([2, ''])
    else:
      newcommand = command[1:]
      totallength = 0
      for ncitem in newcommand:
        if type(ncitem) == list:
          vtotallength = 0
          for num in range(ncitem[3]):
            actions.append([1, 1])
            actions.append([3, vtotallength+ncitem[0]+num])
            actions.append([3, totallength+var[0]+num])
          totallength += ncitem[3]
          vtotallength += ncitem[3]
        else:
          for char in range(len(ncitem)):
            actions.append([1, 2])
            actions.append([3, totallength+var[0]+char])
            actions.append([2, ncitem[char]])
          totallength += len(ncitem)


        #if totallength > var[3]:
        #  _error("type error: forwarded value is too long", text, linen, " ".join(line), assemble)
        #else:
        for item in range(var[3]-totallength):
          actions.append([1, 2])
          actions.append([3, totallength+var[0]+item])
          actions.append([2, ''])

  elif ctype == "if":
    actions.append([1, 4])
    for item in command[0:3]:
      if type(item) == list:
        actions.append([3, item[0]])
        actions.append([3, item[1]])
      elif _get_type(item) in ["operator", "int_operator"]:
        actions.append([2, ops[item]])
      else:
        actions.append([2, len(values)])
        for char in str(item):
          if type(item) == int:
            values.append([2, int(char)])
          else:
            values.append([2, str(char)])
        actions.append([2, (len(values)-1)+len(char)])

    if len(command) == 4:
      actions.append([4, len(actions)])
      actions.append([5, command[3], text, linen, " ".join(line), assemble])
    elif len(command) == 5:
      actions.append([5, command[3], text, linen, " ".join(line), assemble])
      actions.append([5, command[4], text, linen, " ".join(line), assemble])
    elif len(command) <= 3:
      _error("syntax error: if function needs at least one jump argument", text, linen, " ".join(line), assemble)
  
  elif ctype == "math":
    var = variables[command[0]] # get the STARTING variable, all other mathing vars
    # are already included in the command menu

    if len(command) != 4:
      _error("syntax error: math function missing arguments", text, linen, " ".join(line), assemble)
    else:
      actions.append([1, 6])      
      if type(command[1]) == list:
        actions.append([3, command[1][0]])
        actions.append([3, command[1][1]])
      else:
        for item in range(len(str(command[1]))):
          values.append([2, int(str(command[1])[item])])
        actions.append([2, (len(values))-len(str(command[1]))])
        actions.append([2, len(values)])
      
      actions.append([2, 0])
      actions.append([1, 6])
      if type(command[3]) == list:
        actions.append([3, command[3][0]])
        actions.append([3, command[3][1]])
      else:
        for item in range(len(str(command[3]))):
          values.append([2, int(str(command[3])[item])])
        actions.append([2, (len(values))-len(str(command[3]))])
        actions.append([2, len(values)])
      
      actions.append([2, 1])

      actions.append([1, 7])
      actions.append([2, command[2]])

      actions.append([1, 5])
      actions.append([3, var[0]])
      actions.append([3, var[1]])
      actions.append([2, linen+1])
  
  elif ctype == "type":
    var = variables[command[0]]

    if len(command) < 2:
      _error("syntax error: type function needs change type", text, linen, " ".join(line), assemble)

    variables[command[0]][2] = command[1]

    if command[1] == "int":
      num = 2
    elif command[1] == "string":
      num = 1

    for item in range(var[0], var[1]):
      actions.append([1, 11])
      actions.append([3, item])
      actions.append([2, num])
      actions.append([3, item])

def compile(text):
  lines = text.split("\n")
  for line in range(len(lines)):
    command = lines[line].rstrip().split(" ")
    if (len(lines[line]) - len(lines[line].lstrip())) == len(lines[line]):
      pass
    elif (len(lines[line]) - len(lines[line].lstrip())) >= 1:
      error = True
      for char in command[1:]:
        if len(char) > 0:
          if char[0] == "#":
            error = False
            break
      if error:
        _error("syntax error: cannot have leading whitespace on a command", (len(lines[line]) - len(lines[line].lstrip()))*" ", line, lines[line], "")
    elif command[0][0] == "#":
      pass
    elif command[0][0] == ">" and command[0][-1] == "<":
      # implement warning
      jumps[str(command[0][1:-1])] = len(actions)
    else:
      _parse_line(command, line)
  
  big_d = {}

  count = 0
  for item in values:
    big_d[count] = item
    count += 1

  for item in variablel:
    big_d[count] = item
    count += 1

  for item in actions:
    if item[0] == 3:
      big_d[count] = [2, item[1]+len(values)]
    elif item[0] == 4:
      big_d[count] = [2, item[1]+len(values)+len(variablel)]
    elif item[0] == 5:
      if not str(item[1]) in jumps:
        _error("jump error: point '" + str(item[1]) + "' does not exist", item[2], item[3], item[4], item[5])
      else:
        big_d[count] = [2, int(jumps[str(item[1])])+len(values)+len(variablel)]
    else:
      big_d[count] = item
    count += 1
  
  if len(actions) == 0:
    big_d[count] = [1,0]
  elif actions[-1] != [1,0]:
    big_d[count] = [1,0]
  
  return big_d