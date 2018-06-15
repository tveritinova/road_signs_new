import os
import csv
from PIL import Image

IMAGE_SIZE = 416.

def get_data():
    res_data = {}
    res_data['LABELS'] = [
        '1_13', '7_4', '7_3', '7_7', '5_22', '2_3', '3_13_r4.3', '1_12', '4_1_5', '8_5_4', '4_2_2', '1_1', '2_3_3', 
        '3_12_n6', '8_5_2', '1_22', '8_2_1', '3_14_r3.5', '3_13_r5.2', '1_8', '8_3_2', '3_27', '3_13_r4.5', '3_24_n80', 
        '3_12_n3', '5_15_1', '2_2', '3_11_n9', '3_11_n13', '1_17', '8_6_2', '3_13_r4', '1_11', '4_1_6', '3_13_r3', '1_19', 
        '2_4', '5_6', '2_6', '7_11', '3_28', '8_8', '3_24_n70', '3_4_n5', '5_15_7', '8_4_4', '3_31', '8_6_4', '6_2_n20', 
        '4_1_1', '3_25_n20', '3_2', '3_14_r3.7', '8_2_3', '1_14', '8_17', '3_13_r3.9', '1_10', '5_15_3', '5_5', '4_1_2_1', 
        '1_11_1', '2_3_6', '6_8_3', '3_13_r3.5', '8_23', '3_13_r4.2', '3_11_n23', '6_6', '5_15_2', '5_17', '7_14', '5_16', 
        '3_1', '8_1_3', '8_3_1', '1_7', '3_16_n1', '3_21', '8_13', '5_11', '3_18_2', '3_30', '3_13_r3.7', '3_4_n8', 
        '3_16_n3', '5_3', '7_18', '6_2_n60', '4_1_2_2', '2_3_4', '3_4_n2', '8_15', '3_12_n10', '1_20', '1_15', '4_8_3', 
        '1_23', '1_31', '5_15_5', '8_2_2', '1_20_2', '6_3_1', '2_3_5', '8_4_1', '6_15_2', '3_13_r4.1', '1_5', '3_6', 
        '8_16', '4_8_2', '3_24_n10', '5_21', '2_1', '3_20', '3_14_r2.7', '7_5', '1_12_2', '5_20', '1_21', '6_8_1', '4_3', 
        '1_25', '3_14_r3', '3_25_n40', '7_6', '3_32', '3_25_n50', '3_24_n30', '4_5', '8_18', '7_1', '3_13_r3.3', 
        '3_11_n20', '4_1_2', '6_15_3', '4_2_3', '3_10', '3_11_n5', '3_11_n17', '3_13_r2.5', '7_2', '8_2_4', '5_14', 
        '6_16', '3_24_n5', '8_1_1', '3_24_n50', '8_13_1', '3_13_r5', '5_8', '3_33', '3_18', '3_4_1', '5_15_2_2', '1_27', 
        '1_18', '1_6', '3_24_n20', '3_29', '7_12', '4_1_4', '8_14', '5_18', '8_3_3', '2_7', '1_30', '6_2_n40', '6_7', 
        '6_8_2', '3_11_n8', '3_24_n60', '5_19_1', '1_33', '8_4_3', '3_19', '5_7_1', '3_25_n70', '4_2_1', '1_20_3', '6_4', 
        '3_12_n5', '4_1_3', '3_24_n40', '1_16', '1_2', '8_1_4', '5_12', '5_4', '6_2_n70', '3_25_n80', '7_15', '5_7_2', 
        '2_5', '6_15_1', '2_3_2', '6_2_n50', '1_26']
    
    data = {}
    
#     image_width = 1280.0
#     image_height = 720.0

    for filename in os.listdir('/jet/prs/russian_signs/rtsd/rtsd-frames'):
        filename = '/jet/prs/russian_signs/rtsd/rtsd-frames/'+filename
        data[filename] = {}
        data[filename]['xmins'] = []
        data[filename]['xmaxs'] = []
        data[filename]['ymins'] = []
        data[filename]['ymaxs'] = []
        data[filename]['classes_text'] = []   
        data[filename]['classes'] = []

    with open('/jet/prs/russian_signs/rtsd/full-gt.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            filename, x_from, y_from, w, h, text, label = row
            filename = '/jet/prs/russian_signs/rtsd/rtsd-frames/'+filename
            
            img = Image.open(filename)
            img_w, img_h = img.size
            
            if float(x_from) + float(w) > img_w or float(y_from) + float(h) > img_h:
                continue;
            
            coef = float(IMAGE_SIZE) / float(img_w)
            offset = (IMAGE_SIZE - img_h * coef) / 2.

            data[filename]['xmins'].append(float(x_from) / img_w)
            data[filename]['xmaxs'].append((float(x_from) + float(w)) / img_w)
            data[filename]['ymins'].append((offset + float(y_from) * coef) / IMAGE_SIZE)
            data[filename]['ymaxs'].append((offset + (float(y_from) + float(h)) * coef) / IMAGE_SIZE)
            data[filename]['classes_text'].append(text)
            
    images = []

    for filename in data:
        image = {}
        image['filename'] = filename
        image['signs'] = []

        for i, _ in enumerate(data[filename]['xmins']):
            sign = {}
            sign['name'] = data[filename]['classes_text'][i]
            sign['xmin'] = data[filename]['xmins'][i]
            sign['ymin'] = data[filename]['ymins'][i]
            sign['xmax'] = data[filename]['xmaxs'][i]
            sign['ymax'] = data[filename]['ymaxs'][i]
            image['signs'].append(sign)

        images.append(image)
        
    res_data['images'] = images
    res_data['input_shape'] = (40, 40, 3)
    
    return res_data