from flask import Flask, send_file, request
import spacy
from spacypdfreader import pdf_reader
from spacy import displacy
from flask_cors import CORS
import difflib
from pdf2image import convert_from_path, convert_from_bytes

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
import pytesseract as pt


app = Flask(__name__)
CORS(app)
# NLP-Engine

root_location = "/Users/mohammadannan/Desktop/Dataset/"
nlp = spacy.blank("en")

# Image Cropper Function
# Checks counter and crops dimensions accordingly.

# This is for image cropping, to manipulate the .jpg
# of the .pdf for parsing


def imageCropper(counter, img, width, height):
    if counter == 1:
        box1 = (0, 0, width/2, height)
        img2 = img.crop(box1)
        ret = pt.image_to_string(img2)
        box2 = (width/2, 0, width, height)
        img3 = img.crop(box2)
        ret2 = pt.image_to_string(img3)
        doc = nlp(ret)
        doc2 = nlp(ret2)
        return [doc, doc2]
    elif counter == 2:
        # (12) and (19) var extract
        box1 = (0, 0, width/1.9144144144144144, height/7.746478873239437)
        img2 = img.crop(box1)
        ret1 = pt.image_to_string(img2)
        # (10) and (45) var extract
        # width-2_2_2_0
        box2 = (width/1.9, 0, width, height/7.746478873239437)
        img3 = img.crop(box2)
        ret2 = pt.image_to_string(img3)
        doc = nlp(ret1)
        doc2 = nlp(ret2)
        # Left screenshot
        box3 = (300, height/7.5, width/2, height)
        img4 = img.crop(box3)
        # img4.show()
        ret3 = pt.image_to_string(img4)
        print(ret3)
        box4 = (width/2, height/7.746478873239437, width, height)
        img5 = img.crop(box4)
        img5.show()
        ret4 = pt.image_to_string(img5)
        doc3 = nlp(ret3)
        doc4 = nlp(ret4)
        return [doc, doc2, doc3, doc4]
    elif counter == 3:
        # (12) and (19) var extract
        box1 = (0, 0, width/1.9144144144144144, height/7.746478873239437)
        img2 = img.crop(box1)
        # img2.show()
        ret1 = pt.image_to_string(img2)
        # print(ret1)
        # (10) and (45) var extract
        # width-2_2_2_0
        box2 = (width/1.9, 0, width, height/7.746478873239437)
        img3 = img.crop(box2)
        ret2 = pt.image_to_string(img3)
        doc = nlp(ret1)
        doc2 = nlp(ret2)
        # Left screenshot
        box3 = (300, height/7.5, width/2, height)
        img4 = img.crop(box3)
        # img4.show()
        ret3 = pt.image_to_string(img4)
        print(ret3)
        # print(ret3)
        box4 = (width/2, height/7.746478873239437, width, height)
        img5 = img.crop(box4)
        # img5.show()
        ret4 = pt.image_to_string(img5)
        doc3 = nlp(ret3)
        doc4 = nlp(ret4)
        return [doc, doc2, doc3, doc4]


def recursiveExtract(doc, i=0, counter=0, d={}, s=''):
    if i >= len(doc)-3:
        return d
    else:

        if doc[i].text == 'as' and doc[i+1].text == ')':
            index = i+2
            s = '(19)'
            if s not in d:
                d[s] = ''
            return recursiveExtract(doc, i=index, counter=0, d=d, s=s)
        if doc[i].text == 'a2' and doc[i+1].text == ')':
            index = i+2
            s = '(12)'
            if s not in d:
                d[s] = ''
            return recursiveExtract(doc, i=index, counter=0, d=d, s=s)

        elif doc[i].text == '(' and doc[i+1].text.isdigit() and doc[i+2].text == ')':
            index = i+3
            s = doc[i].text + doc[i+1].text + doc[i+2].text
            if s not in d:
                d[s] = ''
            return recursiveExtract(doc, i=index, counter=0, d=d, s=s)
        elif doc[i].text == '(' and doc[i+1].text == '*' and doc[i+2].text == '*' and doc[i+3].text == ')':
            s = doc[i].text + doc[i+1].text + doc[i+2].text + doc[i+3].text
            index = i + 4
            if s not in d:
                d[s] = ''
            return recursiveExtract(doc, i=index, counter=0, d=d, s=s)
        elif len(d) >= 1:
            if doc[i].text != '\n' and doc[i].text.isspace():
                d[s] += ' '
            elif doc[i].text != '\n':
                d[s] += doc[i].text
                d[s] += ' '

            index = i+1
            # print(i)

            return recursiveExtract(doc, i=i+1, counter=0, d=d, s=s)
        else:
            index = i + 1
            return recursiveExtract(doc, i=i+1, counter=0, d=d, s=s)

# This is the compare aspect, it compares each article and it's contents


def wordSimiliar(key, sentence1, sentence2):
    d = difflib.Differ()
    diff = d.compare(sentence1.split(), sentence2.split())
    rotate = ' '.join(diff)
    rotate = rotate.split()
    # print(rotate)
    sen1 = ''
    sen2 = ''
    same = ''
    for i in range(len(rotate)):
        if rotate[i-1] == '-':
            sen1 += rotate[i]
            sen1 += ' '
            i += 1
        elif rotate[i-1] == '+':
            sen2 += rotate[i]
            sen2 += ' '
            i += 1
        elif rotate[i] != '-' or rotate[i] != '+':
            same += rotate[i]
            same += " "
            i += 1
    checker1 = sen1
    checker2 = sen2

    returned = key + '\n' + "Sentence 1 difference: " + sen1 + \
        '\nSentence 2 difference: ' + sen2 + '\nSame results: ' + same + '\n'
    return [returned, checker1, checker2]

# This converts the .pdf to .jpg for parsing purposes


@app.route('/getImage/<image_path>')
def getImage(image_path):
    pdf = Path(root_location + image_path)
    save_dir = Path('../assets')
    print(save_dir / f'{pdf.stem}-page{0}.jpg')
    pages = convert_from_path(pdf, 500)
    for num, page in enumerate(pages, start=1):
        if num == 1:
            print(save_dir / f'{pdf.stem}-page{num}.jpg')
            page.save(save_dir / f'{pdf.stem}-page{num}.jpg', 'JPEG')

            path = save_dir / f'{pdf.stem}-page{num}.jpg'
            break

    return send_file(path)

# This recursive function parses the pdf


@app.route('/engine/process/<pdf_path>')
def recursiveFunc(pdf_path):
    pdf = Path(root_location + pdf_path)
    save_dir = Path('../assets')
    print(save_dir / f'{pdf.stem}-page{0}.jpg')
    pages = convert_from_path(pdf, 500)
    for num, page in enumerate(pages, start=1):
        if num == 1:
            print(save_dir / f'{pdf.stem}-page{num}.jpg')
            page.save(save_dir / f'{pdf.stem}-page{num}.jpg', 'JPEG')

            path = save_dir / f'{pdf.stem}-page{num}.jpg'
            print(path)
            break
    img_obj = Image.open(path)
    width, height = img_obj.size
    docList = imageCropper(counter=1, img=img_obj, width=width, height=height)
    doc = docList[0]
    for i in range(len(doc)-2):
        # print(doc[i].text)
        if doc[i].text == "United" and doc[i+1].text == "States" and doc[i+2].text == "Design":
            counter = 2
            break
        elif doc[i].text == "Patent" and doc[i+1].text == "Application":
            counter = 3
            break
    else:
        counter = 1
    docList = imageCropper(counter, img=img_obj, width=width, height=height)
    doc = docList[0]
    # print(doc)
    doc2 = docList[1]

    if counter == 1:  # United States Patent
        d1 = recursiveExtract(doc, i=0, counter=0, d={}, s='')
        d2 = recursiveExtract(doc2, i=0, counter=0, d={}, s='')
        # print(d1['(12)'])
        d1.update(d2)
        print(d1)
    elif counter == 2:  # United States Design Patent
        d1 = recursiveExtract(doc, i=0, counter=0, d={}, s='')
        # print(d1)
        d2 = recursiveExtract(doc2, i=0, counter=0, d={}, s='')
        doc3 = docList[2]
        d3 = recursiveExtract(doc3, i=0, counter=0, d={}, s='')
        docPDF = pdf_reader(root_location + pdf_path, nlp)
        docPDF = docPDF._.page(1)
        dM = recursiveExtract(docPDF, i=0, counter=0, d={}, s='')

        compare = []
        for i in d3:
            for k in dM:
                if i == k:
                    d3[i] = dM[k]

        doc4 = docList[3]

        d4 = recursiveExtract(doc4, i=0, counter=0, d={}, s='')
        # print(d4)
        d1.update(d2)
        d1.update(d3)
        d1.update(d4)
        print(d1)
    elif counter == 3:  # Publication Patent
        d1 = recursiveExtract(doc, i=0, counter=0, d={}, s='')
        # print(d1)
        d2 = recursiveExtract(doc2, i=0, counter=0, d={}, s='')
        doc3 = docList[2]
        d3 = recursiveExtract(doc3, i=0, counter=0, d={}, s='')  # left side
        docPDF = pdf_reader(root_location + pdf_path, nlp)
        print(docPDF)
        docPDF = docPDF._.page(1)
        dM = recursiveExtract(docPDF, i=0, counter=0, d={}, s='')

        compare = []
        for i in d3:
            for k in dM:
                if i == k:
                    d3[i] = dM[k]

        doc4 = docList[3]

        d4 = recursiveExtract(doc4, i=0, counter=0, d={}, s='')
        # print(d4)
        d1.update(d2)
        d1.update(d3)
        d1.update(d4)
        print(d1)

    storage = []
    for i in d1:
        storage = d1[i]
        changed = storage.replace('-', '')
        another = changed.replace('+', '')

        d1[i] = another
    d1['name'] = pdf_path

    return d1


@app.route('/engine/comparison/', methods=["POST"])
def comparison():
    d1 = request.get_json()['d1']
    d2 = request.get_json()['d2']
    print(d1, d2)
    storage = {}
    for i in d1:
        for k in d2:
            if i == k:
                check = wordSimiliar(i, d1[i], d2[k])

                if i not in storage:
                    if len(check[1]) != 0 or len(check[2]) != 0:
                        storage[i] = check[0]
                    #print(wordSimiliar(i, d1[i], d2[k]))
    return storage


if __name__ == '__main__':
    app.run(debug=True)
