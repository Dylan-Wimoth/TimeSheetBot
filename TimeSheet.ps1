$filepath = ".\"
Set-Location -Path $filepath
try{
    #Try to use python
    python config.py
}
Catch{
    #Else use python3
    Write-Error "An Error calling python config.py"
}
try{
    #Try to use python
    python3 config.py
}
Catch{
    #Else use python3
    Write-Error "An Error calling python3 config.py"
}
try{
    #Try to use python
    python main.py
}
Catch{
    #Else use python3
    Write-Error "An Error calling python main.py"
}
try{
    #Try to use python
    python3 config.py
}
Catch{
    #Else use python3
    Write-Error "An Error calling python3 main.py"
}

    