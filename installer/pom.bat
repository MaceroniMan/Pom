@ECHO OFF

if "%1" == "sr" (

  if "%2" == "" (

    echo pom: error: 'pom sr' needs a filename

  ) else (

    python -m pom --compile "%2" "pscf" && python -m pom "pscf" && del "pscf"

  )

) else (
  
  if "%1" == "sh" (

    echo Pom Simple Help Menu
    echo ====================
    echo pom sr [filename] ......... Compile and run the filename
    echo pom sh .................... List this help menu

  ) else (

    python -m pom %*

  )

)