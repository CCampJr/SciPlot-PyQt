./make.bat clean
sphinx-apidoc.exe -f -o ./source/ .. ../setup.py
./make.bat html
