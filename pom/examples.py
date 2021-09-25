examples = {
  "counting" : """int:3 count < 0 # init 'int' type variable with the value of 0


>jump1< # defign a jump point

int:3 l # defign a new variable


@if count == 20 < "break" # if count is 20 then continue, otherwise jump to point                                 'break'

l < count + 1 # add 1 to that variable

@print < l < "\\n" # print the current count variable as well as a newline afterwards.

count < count + 1 # increment the count variable

@jump < "jump1" # jump to point 'jump1'


>break< # defign a new jump point

@exit # exit the program""",

  "inputmath" : """string:3 num1 # make a blank string variable
string:3 num2 # make a blank string variable

@print < "Number One: " # print out the input prompt
@input < num1 # get input and put it in the num1 variable

@print < "Number Two: " # print out the input prompt
@input < num2 # get input and put it in the num1 variable

@type num1 < :int # convert variable num1 to type of 'int'
@type num2 < :int # convert variable num2 to type of 'int'

int:6 end # make a blank int variable

end < num1 + num2 # add num1 variable and num2 variable together

@print < end # print out the end value"""
}

decs = {
  "counting" : "A script that counts up to number 20 printing out each number",
  "inputmath" : "A script that takes 2 numbers and adds them together"
}

def listexamples():
  lst = []
  for item in examples:
    lst.append(item)
  return lst

def getdec(name):
  return decs[name]

def getexample(name):
  return examples[name]