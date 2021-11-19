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

@print < end # print out the end value""",

  "calculator" : """@print < "Calculator" # Print out a string

>loop< # Make a new jump point

string:1 sign # Make a new blank string variable

string:5 num1 # Make a new blank string variable
string:5 num2 # Make a new blank string variable

@print < "Number One: " # print out the input prompt
@input < num1 # get input and put it in the num1 variable

@print < "\nChoose the method: *,-,+,/ " # print out the input prompt
@input < sign # get input and put it in the num1 variable

@print < "Number Two: " # print out the input prompt
@input < num2 # get input and put it in the num1 variable

@print < "\n" < num1 < sign < num2 # Print out three variables back-to-back

@type num1 < :int # Change the type of variable
@type num2 < :int # Change the type of variable

int:10 end # Make a new blank int variable0

@if sign == "+" < "neg" # If the sign is + then continue, else go to the next if statement
end < num1 + num2 # Adds two numbers together
@jump < "end" # Skip the next if statements

>neg< # Make a new jump point
@if sign == "-" < "mul" # If the sign is - then continue, else go to the next if statement
end < num1 - num2 # Subtracts the two numbers together
@jump < "end" # Skip the next if statements

>mul< # Make a new jump point
@if sign == "*" < "div" # If the sign is * then continue, else go to the next if statement
end < num1 * num2 # Multiply the two numbers
@jump < "end" # Skip the next if statements

>div< # Make a new jump point
@if sign == "/" < "err" # If the sign is / then continue, else go to the error message
end < num1 / num2 # Divides the two numbers
@jump < "end" # Jump past the error

>err< # Make a new jump point
@print < "\n" < sign < " is an invalid sign" # Print the error message
@exit # Exit the program

>end< # Make a new jump point
@print < "=" < end # Print the ending result

@jump < "loop" # Loop the entire program again"""
}

decs = {
  "counting" : "A script that counts up to number 20 printing out each number",
  "inputmath" : "A script that takes 2 numbers and adds them together",
  "calculator" : "A script that you input 2 numbers and a sign (*,-,+,/) and it does the math"
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