#!/bin/bash

if [ "$1" = "sr" ]; then

  if [ "$2" = "" ]; then

    echo "pom: error: 'pom sr' needs a filename"
  
  else

    python3 -m pom --compile "$2" "pscf" && python3 -m pom "pscf" && rm "pscf"
  
  fi

else

  if [ "$1" = "sh" ]; then

    echo "Pom Simple Help Menu"
    echo "===================="
    echo "pom sr [filename] ......... Compile and run the filename"
    echo "pom sh .................... List this help menu"

  else

    python3 -m pom $@

  fi

fi
