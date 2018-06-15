import os
from PIL import Image

IMAGE_SIZE = 416

def remove_space(word):
    if word[0] == ' ':
        return word[1:]
    return word

def parse_annotation(annotation, img_dir, labels=[]):
  
    f = open(annotation, 'r')

    eps = 10**(-6)
    content = []

    for line in f:
        arr = line.split(':')

        img_name = arr[0]
        name = img_name
        signs = []

#         if not os.path.isfile(img_dir+'/'+img_name):
#             continue

        if arr[1] != '\r\n':
            img = Image.open(img_dir+'/'+img_name)
            w, h = img.size
            
            coef = float(IMAGE_SIZE) / float(w)
            offset = (IMAGE_SIZE - h * coef) / 2.
                                    
            for part in arr[1].split(';')[:-1]:

                if part != 'MISC_SIGNS':
                    sign = {}

                    data = part.split(',')

                    visibility = data[0]
                    lrx = float(data[1])
                    lry = float(data[2])
                    ulx = float(data[3])
                    uly = float(data[4])
                    sign_type = remove_space(data[5])
                    sign_name = remove_space(data[6])

                    sign['name'] = sign_name
                    
                    sign['xmin'] = ulx / w
                    sign['ymin'] = (offset + uly * coef) / IMAGE_SIZE
                    sign['xmax'] = lrx / w
                    sign['ymax'] = (offset + lry * coef) / IMAGE_SIZE

                    signs.append(sign)

        img = {}
        img['filename'] = img_dir+'/'+img_name
        img['signs'] = signs
        content.append(img)

    return content

def get_data():
    
    data = {}
    
    data['LABELS'] = [ 
        '100_SIGN', '110_SIGN', '120_SIGN', '30_SIGN', '50_SIGN', '60_SIGN', 
        '70_SIGN', '80_SIGN', '90_SIGN', 'GIVE_WAY', 'NO_PARKING', 'NO_STOPPING_NO_STANDING', 
        'OTHER', 'PASS_EITHER_SIDE', 'PASS_LEFT_SIDE', 'PASS_RIGHT_SIDE', 'PEDESTRIAN_CROSSING', 
        'PRIORITY_ROAD', 'STOP', 'URDBL']
    
    images = []

    for folder in ['Set1Part0', 'Set2Part0']:
        images += parse_annotation('/jet/prs/swedish_signs/annotations_'+folder+'.txt', 
                                   '/jet/prs/swedish_signs/'+folder)
        
    data['input_shape'] = (30, 30, 3)
    data['images'] = images
    
    return data