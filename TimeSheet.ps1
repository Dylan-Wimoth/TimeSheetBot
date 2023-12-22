$filepath = ".\"
Set-Location -Path $filepath
try{
    #Try to use python
    python config.py
}
Catch{
    #Else use python3
   python3 config.py
}
try{
    #Try to use python
    python main.py
}
Catch{
    #Else use python3
    python3 main.py
}

    