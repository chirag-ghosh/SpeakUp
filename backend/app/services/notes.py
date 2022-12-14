import requests
import cv2
import numpy as np
import math
import os
import shutil
from xml.etree import ElementTree

from ..utils.ocr import getOcrText
from ..utils.constants import ttsTokenURL, ttsURL

dir_path = os.path.dirname(os.path.realpath(__file__))


def testing():
    return {"message": "This is the Note endpoint."}


def gimme_text_and_bounding_boxs(img_path):
    pathToFileInDisk = img_path
    with open(pathToFileInDisk, 'rb') as f:
        data = f.read()
    return getOcrText(data)


def gimme_proper_text(text_bnd_boxs_result, column_len, row_len, inverted):
    lines = text_bnd_boxs_result['recognitionResult']['lines']
    my_str = []
    k = 0
    # begin_bullets = -1
    ymax = 0
    for i in range(len(lines)):
        line_str = ""
        words = lines[i]['words']
        prev_mag = 0
        this_head = False
        for j in range(len(words)):
            tl = [words[j]['boundingBox'][0], words[j]['boundingBox'][1]]
            tr = [words[j]['boundingBox'][2], words[j]['boundingBox'][3]]
            br = [words[j]['boundingBox'][4], words[j]['boundingBox'][5]]
            bl = [words[j]['boundingBox'][6], words[j]['boundingBox'][7]]
            text = words[j]['text']
            if (inverted):
                tl[0] = row_len - tl[0]
                tr[0] = row_len - tr[0]
                br[0] = row_len - br[0]
                bl[0] = row_len - bl[0]
                tl[1] = column_len - tl[1]
                tr[1] = column_len - tr[1]
                br[1] = column_len - br[1]
                bl[1] = column_len - bl[1]
            # print(tl)
            line_str += " " + text + " "
            font_size = math.sqrt(
                (tl[0] - bl[0]) * (tl[0] - bl[0]) + (tl[1] - bl[1]) * (tl[1] - bl[1]))
            font_size += math.sqrt((tr[0] - br[0]) * (tr[0] -
                                   br[0]) + (tr[1] - br[1]) * (tr[1] - br[1]))
            font_size = font_size / 2
            if k == 0 and j == 0 and tl[0] > 0.7 * row_len and tl[1] < 0.2 * column_len:
                this_head = False
                line_str = ""
                break
            if k == 0 and j == 0 and tl[0] > 0.3 * row_len:
                this_head = True
            if k == 0 and j == (len(words) - 1) and tl[0] < 0.8 * row_len:
                this_head = True
                break
            if k != 0 and this_head != True and (text.strip() in [':', '>', '='] or (prev_mag > font_size and (font_size - prev_mag) / font_size > 0.2)):
                spp = line_str.split()
                l = len(spp)
                if len(spp) < 3 or (spp[l - 3] != spp[l - 2] and spp[l - 2] != '.'):
                    my_str.append(["subtitle", line_str, words[0], words[j]])
                    line_str = ""
            if this_head == False and font_size > prev_mag:
                prev_mag = font_size
            if len(words) >= 2 and j == 0:
                text = text.strip()
                if len(words) > 3 and text[0] == '(':
                    tx = text + words[1]['text'] + words[2]['text']
                    tx.replace(" ", "")
                    if tx[2] == ')' or tx[3] == ')':
                        my_str.append(["bullet_begin", words[j]])
                elif len(text) <= 2 and (text.isnumeric() or text.isalpha()):
                    # print("I am here", text[0])
                    if text[0].isnumeric():
                        tx = text + words[1]['text']
                        tx.replace(" ", "")
                        if tx[1] == '.' or tx[1] == ')':
                            my_str.append(["bullet_begin", words[j]])
                    elif text[0] in ['a', 'b']:
                        tx = text + words[1]['text']
                        tx.replace(" ", "")
                        if tx[1] == '.' or tx[1] == ')':
                            my_str.append(["bullet_begin", words[j]])
                        # check subsequent lettrs
                    elif text[0] == 'i':
                        tx = text + words[1]['text']
                        tx.replace(" ", "")
                        if tx[1] == '.' or tx[1] == ')':
                            my_str.append(["bullet_begin", words[j]])
                        # check subsequent lettrs
        if this_head == True:
            if k == 0:
                my_str.append(
                    ["title", line_str, words[0], words[len(words) - 1]])
                k = 1
                line_str = ""
            elif words[0]['boundingBox'][1] > ymax and len(line_str.split()) < 6:
                my_str.append(
                    ["subtitle", line_str, words[0], words[len(words) - 1]])
                line_str = ""
        if len(line_str) != 0:
            my_str.append(["normal", line_str.strip(),
                          words[0], words[len(words) - 1]])
        i1 = words[0]['boundingBox'][5]
        i2 = words[0]['boundingBox'][7]
        _ymax = i2
        if i1 > i2:
            _ymax = i1
        if _ymax > ymax:
            ymax = _ymax
    # print([(item[0], item[1]) for item in my_str])
    return my_str


def gimme_the_final_text(text_with_types):
    text_to_be_spoken = ""
    for text_block in text_with_types:
        if text_block[0] == "title":
            text_to_be_spoken += ". The title of the text is: "
            text_to_be_spoken += text_block[1] + ".\n "
        elif text_block[0] == "subtitle":
            text_to_be_spoken += ". The subtitle is"
            text_to_be_spoken += text_block[1] + ".\n "
        elif text_block[0] == "bullet_begin":
            text_to_be_spoken += ". Begin of the next point: "
        else:
            text_to_be_spoken += text_block[1]
    return text_to_be_spoken


def show_result_on_image(img_path, text_with_types, inverted):
    img = cv2.imread(img_path)
    font = cv2.FONT_HERSHEY_SIMPLEX
    k = 15
    if inverted:
        k = -k
    for t in text_with_types:
        if t[0] == "bullet_begin":
            cv2.putText(img, "bullet", (t[1]['boundingBox'][0] - 50, t[1]
                        ['boundingBox'][1]), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
        elif t[0] != "normal":
            cv2.rectangle(img, (t[2]['boundingBox'][0], t[2]['boundingBox'][1] - k),
                          (t[3]['boundingBox'][4], t[3]['boundingBox'][5] + k), (0, 0, 255), 2)
            cv2.putText(img, t[0], (t[3]['boundingBox'][0] - 10, t[3]
                        ['boundingBox'][1] + 5), font, 2, (0, 0, 255), 1, cv2.LINE_AA)
        else:
            cv2.rectangle(img, (t[2]['boundingBox'][0], t[2]['boundingBox'][1] - k),
                          (t[3]['boundingBox'][4], t[3]['boundingBox'][5] + k), (0, 0, 255), 2)
    cv2.imwrite(os.path.join(dir_path, 'notes_output_image.jpg'), img)


def get_my_audio_token():
    headers = {
        'Ocp-Apim-Subscription-Key': os.getenv('SpeechKey') or ""
    }
    response = requests.post(ttsTokenURL, headers=headers)
    return str(response.text)


def save_audio(access_token, text_to_be_spoken):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/ssml+xml',
        'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
        'User-Agent': 'YOUR_RESOURCE_NAME'
    }
    xml_body = ElementTree.Element('speak', version='1.0')
    xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
    voice = ElementTree.SubElement(xml_body, 'voice')
    voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
    
    voice.set('name', 'en-IN-NeerjaNeural')
    voice.text = text_to_be_spoken
    body = ElementTree.tostring(xml_body)
    response = requests.post(ttsURL, headers=headers, data=body)
    if response.status_code == 200:
        with open(os.path.join(dir_path, 'notes_audio.wav'), 'wb') as audio:
            audio.write(response.content)
            # all_audio.append('sample-' + self.timestr + '.wav')
            print("\nStatus code: " + str(response.status_code) +
                  "\nYour TTS is ready for playback.\n")
        return True
    else:
        print("\nStatus code: " + str(response.status_code) +
              "\nSomething went wrong. Check your subscription key and headers.\n")
        print("Reason: " + str(response.reason) + "\n")
        return False


def tell_me_if_its_inverted(text_bnd_boxs_result):
    lines = text_bnd_boxs_result['recognitionResult']['lines']
    first = lines[0]['words'][0]
    last = lines[len(lines) - 1]['words'][0]
    top_x = first['boundingBox'][1]
    bottom_x = last['boundingBox'][1]
    if top_x >= bottom_x:
        return True
    return False


def note_make(url, img_path="notes_input_img.jpg", sound = False):
    img_path = os.path.join(dir_path, img_path)
    resp = requests.get(url, stream=True)
    local_file = open(img_path, "wb")
    resp.raw.decode_content = True
    print(resp.raw)
    shutil.copyfileobj(resp.raw, local_file)
    print(local_file)
    shp = cv2.imread(img_path).shape
    column_len = shp[0]
    row_len = shp[1]
    text_bnd_boxs_result = gimme_text_and_bounding_boxs(img_path)
    inverted = tell_me_if_its_inverted(text_bnd_boxs_result)
    text_with_types = gimme_proper_text(
        text_bnd_boxs_result, column_len, row_len, inverted)
    show_result_on_image(img_path, text_with_types, inverted)
    text_to_be_spoken = gimme_the_final_text(text_with_types)
    if sound == False:
        return text_to_be_spoken
    access_token = get_my_audio_token()
    save_audio(access_token, text_to_be_spoken)
    return text_to_be_spoken, os.path.join(dir_path, 'notes_audio.wav')
