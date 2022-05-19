import sys, os

def _error(place, text):
  if os.name == 'nt':
    print("error: " + place + ": " + text)
  else:
    print("\n\033[0;91merror: " + place + ": " + text + "\033[00m")
  sys.exit(0)

def _is_int(string):
  string = str(string)
  if string in ["True", "False"]:
    return False
  try:
    int(string)
    return True
  except:
    return False

def _strip(number):
  number = str(number)
  if number.endswith(".0"):
    return int(number[:-2])
  else:
    return float(number)

class memory(object):
  def __init__(self, length=255):
    self.__memory = {}
    self.__length = length
  
  def load(self, dictionary, autosize=False):
    if autosize:
      self.__length = len(dictionary)
    for item in dictionary:
      try:
        self.__memory[int(item)] = list(dictionary[item])
      except:
        _error("memory", "load: bad value")
  
  @property
  def getmemory(self):
    return self.__memory

  def __setitem__(self, key, item):
    if not _is_int(key):
      _error("memory", "key " + str(key) + " must be type integer")
    else:
      if key <= self.__length:
        try:
          self.__memory[key] = list(item)
        except:
          _error("memory", "load: bad value")
      else:
        _error("memory", "memory cannot excede " + str(self.__length))

  def __getitem__(self, key):
    if not _is_int(key):
      _error("memory", "key " + str(key) + " must be type integer")
    else:
      if key <= self.__length:
        if key in self.__memory:
         return self.__memory[key]
        else:
          self.__memory[key] = [0,0]
          return [0,0]
      else:
        _error("memory", "memory cannot excede " + str(self.__length))

  def __len__(self):
    return self.__length

class emulator(object):
  def __init__(self, memory):
    self.memory = memory
    self.registers = {"pointer":-1, "math1":[0,0,0]}
  
  def __execute(self, command):
    if command[0] == 0:
      return False
    elif command[0] == 1:
      old = self.memory[command[1]]
      self.memory[command[2]] = old
    elif command[0] == 2:
      self.memory[command[1]] = [2, command[2]]
    elif command[0] == 3:
      return int(command[1])-1
    elif command[0] == 4:
      first = ""
      second = ""
      for num in range(command[1], command[2]):
        first += str(self.memory[num][1])
      if type(self.memory[command[1]][1]) == int:
        first = int(first)
      for num in range(command[4], command[5]):
        second += str(self.memory[num][1])
      if type(self.memory[command[4]][1]) == int:
        second = int(second)
      if command[3] == 1:
        if first == second:
          return int(command[6])-1
        else:
          return int(command[7])-1
      elif command[3] == 2:
        if first != second:
          return int(command[6])-1
        else:
          return int(command[7])-1
      elif command[3] == 3:
        if first < second:
          return int(command[6])-1
        else:
          return int(command[7])-1
      elif command[3] == 4:
        if first > second:
          return int(command[6])-1
        else:
          return int(command[7])-1
      elif command[3] == 5:
        if first <= second:
          return int(command[6])-1
        else:
          return int(command[7])-1
      elif command[3] == 6:
        if first >= second:
          return int(command[6])-1
        else:
          return int(command[7])-1
    elif command[0] == 5:
      befornum = str(self.registers["math1"][2])
      if len(befornum) > command[2]-command[1]:
        try:
          print("\n\033[91mruntime error on line " + str(command[3]) + "\033[00m")
        except:
          pass
        _error("exceed memory", "value is too large for allocated space")
      else:
        numzs = (command[2]-command[1]) - len(befornum)
        befornum = befornum + " "*numzs
      for item in range(command[2]-command[1]):
        if befornum[item] == " ":
          self.memory[command[1]+item] = [2, '']
        else:
          if befornum[item] in ["-", "."]:
            self.memory[command[1]+item] = [2, befornum[item]]
          else:
            self.memory[command[1]+item] = [2, int(befornum[item])]
    elif command[0] == 6:
      addnum = ""
      for item in range(command[1], command[2]):
        addnum += str(self.memory[item][1])
      if _is_int(addnum):
        self.registers["math1"][command[3]] = float(addnum)
      else:
        _error("type error", "value \"" + str(addnum) + "\" cannot be used in register")
    elif command[0] == 7:
      if command[1] == "+":
        self.registers["math1"][2] = _strip(round(self.registers["math1"][0] + self.registers["math1"][1], 1))
      elif command[1] == "-":
        self.registers["math1"][2] = _strip(round(self.registers["math1"][0] - self.registers["math1"][1], 1))
      elif command[1] == "*":
        self.registers["math1"][2] = _strip(round(self.registers["math1"][0] * self.registers["math1"][1], 1))
      elif command[1] == "/":
        self.registers["math1"][2] = _strip(round(self.registers["math1"][0] / self.registers["math1"][1], 1))
    elif command[0] == 8:
      print(str(self.memory[command[1]][1]).replace("\\n", "\n"), end="")
    elif command[0] == 9:
      sys.stdout.flush()
    elif command[0] == 10:
      text = input()
      for num in range(command[2]):
        if num+1 > len(text):
          char = ''
        else:
          char = text[num]
        self.memory[num+command[1]] = [2, char]
    elif command[0] == 11:
      first = self.memory[command[1]]
      if command[2] == 1:
        first[1] = str(first[1])
      elif command[2] == 2:
        if first[1] in ["-", ".", ""]:
          first[1] = first[1]
        else:
          try:
            first[1] = int(first[1])
          except:
            _error("type error", "value \"" + first[1] + "\" cannot be converted into an int")
      self.memory[command[3]] = first
    return True

  def run(self):
    try:
      current = []
      while True:
        self.registers["pointer"] += 1
        command = self.memory[self.registers["pointer"]]
        if command == [0,0]:
          _error("executable", "cannot execute value")
        if command[0] == 1:
          if current != []:
            returnv = self.__execute(current)
            if _is_int(returnv):
              current = []
              self.registers["pointer"] = returnv
              continue
          if command[1] == 0:
            break
          current = []
          current.append(command[1])
        elif command[0] == 2:
          if current != []:
            current.append(command[1])
      print("\ninfo: executable: done")
    except KeyboardInterrupt:
      _error("executable", "keyboard interrupt")