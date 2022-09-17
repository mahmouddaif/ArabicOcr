
import re
import cv2
import numpy as np
from PIL import Image

def read_custum_html(file_name):
    with open(file_name) as f:
        return f.read()

def get_lines(result):
  lines_dict = {}
  l=0
  lines_dict[0]=[]
  cord = result[0][0]
  x_min, y_min = [int(min(idx)) for idx in zip(*cord)]
  x_max, y_max = [int(max(idx)) for idx in zip(*cord)]
  lines_dict[0].append([[x_max, y_min], result[0][1]])
  y_min_prev = lines_dict[0][0][0][1]
  for i in range(1, len(result)):
    cord = result[i][0]
    x_min, y_min = [int(min(idx)) for idx in zip(*cord)]
    x_max, y_max = [int(max(idx)) for idx in zip(*cord)]
    if y_min-y_min_prev<18:
      lines_dict[l].append([[x_max, y_min], result[i][1]])
      y_min_prev = y_min
    else:
      l= l+1
      lines_dict[l]=[]
      lines_dict[l].append([[x_max, y_min], result[i][1]])
      y_min_prev = y_max
  return lines_dict
def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image

def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def annotate_image(image, result): 
  #image = pil2cv(image)
  for i in range(len(result)):
    cord = result[i][0]
    x_min, y_min = [int(min(idx)) for idx in zip(*cord)]
    x_max, y_max = [int(max(idx)) for idx in zip(*cord)]
    image = cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,255,0),5)
  cv2.imwrite("./image.jpg", image)
  return image

def arrange_words_in_line(lines_dict):
  if isinstance(lines_dict, dict):
    arranged_dict = {}
    for key, values in lines_dict.items():
      line = lines_dict[key]
      sorted_line = sorted(line,key=lambda x:x[0][0], reverse=True)
      arranged_dict[key] = sorted_line
    return arranged_dict
  else:
    raise TypeError("The arg must be dict of lines")

def get_raw_text(result):
  lines_dict = get_lines(result)
  arranged_lines_dict = arrange_words_in_line(lines_dict)
  text_list = []
  for i in range(len(arranged_lines_dict.keys())):
    for j in range (len(arranged_lines_dict[i])):
      line_text = arranged_lines_dict[i][j][1]
      text_list.append(line_text)
    text_list.append('\n')
    raw_text = ' '.join(text_list)
    raw_text = replace_en_num(raw_text)
  return raw_text

def replace_en_num(text):
   text = re.sub("0", "\u0660", text)
   text = re.sub("1", "\u0661", text)
   text = re.sub("2", "\u0662", text)
   text = re.sub("3", "\u0663", text)
   text = re.sub("4", "\u0664", text)
   text = re.sub("5", "\u0665", text)
   text = re.sub("6", "\u0666", text)
   text = re.sub("6", "\u0667", text)
   text = re.sub("8", "\u0668", text)
   text = re.sub("9", "\u0669", text)
   return text