import os
import tensorflow as tf
from object_detection.utils import dataset_util

def remove_space(word):
    if word[0] == ' ':
        return word[1:]
    return word

def parse_annotation(annotation, img_dir):
  
  f = open(annotation, 'r')

  eps = 10**(-6)
  content = []
  
  for line in f:
    arr = line.split(':')

    img_name = arr[0]
    name = img_name
    signs = []
    
    if not os.path.isfile(img_dir+'/'+img_name):
      continue

    if arr[1] != '\r\n':
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
            sign['xmin'] = ulx
            sign['ymin'] = uly
            sign['xmax'] = lrx
            sign['ymax'] = lry

        if sign != {}:
            signs.append(sign)

    img = {}
    img['filename'] = img_dir+'/'+img_name
    img['signs'] = signs
    content.append(img)
                        
  return content

train_imgs = parse_annotation('../../../road_signs/annotations.txt', '../../../road_signs/images/train')

flags = tf.app.flags
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS

LABELS = ['100_SIGN', '110_SIGN', '120_SIGN', '30_SIGN', '50_SIGN', '60_SIGN', 
          '70_SIGN', '80_SIGN', '90_SIGN', 'GIVE_WAY', 'NO_PARKING', 'NO_STOPPING_NO_STANDING', 
          'OTHER', 'PASS_EITHER_SIDE', 'PASS_LEFT_SIDE', 'PASS_RIGHT_SIDE', 'PEDESTRIAN_CROSSING', 
          'PRIORITY_ROAD', 'STOP', 'URDBL']

def create_tf_example(image):
  # Bosch
    height = 960 # Image height
    width = 1280 # Image width

    filename = image['filename']
    filename = filename.encode()

    with tf.gfile.GFile(filename, 'rb') as fid:
        encoded_image = fid.read()

    image_format = 'png'.encode() 

    xmins = [] # List of normalized left x coordinates in bounding box (1 per box)
    xmaxs = [] # List of normalized right x coordinates in bounding box
                # (1 per box)
    ymins = [] # List of normalized top y coordinates in bounding box (1 per box)
    ymaxs = [] # List of normalized bottom y coordinates in bounding box
                # (1 per box)
    classes_text = [] # List of string class name of bounding box (1 per box)
    classes = [] # List of integer class id of bounding box (1 per box)

    for sign in example['signs']:
        xmins.append(float(sign['xmin'] / width))
        xmaxs.append(float(sign['xmax'] / width))
        ymins.append(float(sign['ymin'] / height))
        ymaxs.append(float(sign['ymax'] / height))
        classes_text.append(sign['name'].encode())
        classes.append(LABELS.index(sign['name']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_image),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))

    return tf_example

writer = tf.python_io.TFRecordWriter(FLAGS.output_path)

for data_and_label_info in train_imgs:
    tf_example = create_tf_example(data_and_label_info)
    writer.write(tf_example.SerializeToString())

writer.close()