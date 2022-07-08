# NLP Engine for Google Patents

## Introduction

This project involves a Google Patent PDF processor. The repository consists of all the code required to run the web application. You can use the pdf files available in the dataset to upload the pdf files, and you'd be able to see the parsed results. The NLP engine recognizes the variables and values, and it is also capable of recognizing variances between two patent pdf files, when it comes to their variables and the values. 

## Pre-requisites to run the project

#Install the project files, perferably ensure the project folder is on your desktop

Then, run the following command on your terminal:
```bash

cd Desktop
```

To run the virtual environment run this command on your terminal:
```bash
source nlp-server/server/venv/bin/activate
```

Now run the following commands to download the libraries, make sure you're on Desktop:

Also make sure to press the following keys:

1. Cmd/Ctrl + Shift + P
2. Search for "Python: Select Interpreter" 
3. Select the conda base intepreter

<img width="724" alt="Screen Shot 2022-07-07 at 11 53 51 PM" src="https://user-images.githubusercontent.com/87118726/177869719-8862418a-0980-4155-96b2-2cfe314af43c.png">

```
cd Desktop
```
``` bash
pip3 install flask \ pip3 install pdf2image \ pip3 install pathlib \ pip3 install flask_cors \
pip3 install spacypdfreader \ pip3 install -U pip setuptools wheel \ 
pip3 install -U spacy \ pip install pillow \ pip3 install spacy \ pip3 install pytesseract





```



``` bash
npm install axios
```

# Now that's finally out of the way, let's run the project!
# Run the following commands to run the web application:

``` bash
cd Desktop
```
``` bash
cd nlp-server/server/venv
```
``` bash
python3 server.py
```
# The backend is now running! Now for the frontend: 
``` bash
cd ~/Desktop/nlp-server/frontend-react 
```
``` bash
npm start
```
# The web application should be up and running!
# Now just upload the two google patent PDFs you wish to compare

