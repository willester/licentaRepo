from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import sys

folder_name = sys.argv[1]

image_generator = ImageDataGenerator(rotation_range=25,
                                    width_shift_range=0.2,
                                     height_shift_range=0.2,
                                     shear_range=0.1,
                                     zoom_range=0.2,
                                     horizontal_flip=True,
                                     fill_mode='nearest')

loaded_model = load_model('E:/Faculta/_LICENTA/_Aplicatie/pozeModel1SauBinaryModel/binaryModel3_5.h5')

print('incarcat model')

path_test_imagine = 'C:/Users/Willestur/Desktop/test/' + folder_name
image_shape = (300,300,1)
batch_size = 1
test_images_generator = image_generator.flow_from_directory(path_test_imagine,target_size=image_shape[:2],
                                                  color_mode='grayscale',
                                                  batch_size=batch_size,
                                                  class_mode='binary',
                                                  shuffle=False)

print(loaded_model.predict(test_images_generator))
tupple = ()
prob_list = list(tupple)
for i in range(50):
    prob_list.append(loaded_model.predict(test_images_generator))
## de verificat printurile acm i se pare ca e ceva gresit da logica e ok in mare

sick_pred_number = 0
healthy_pred_number = 0
biggest_prediction_arr = 0
for i in prob_list:
    if (biggest_prediction_arr < i):
        biggest_prediction_arr = i
    if (i < 0.5):
        sick_pred_number = sick_pred_number + 1
    else:
        healthy_pred_number = healthy_pred_number + 1

isSick = False
final_biggest_prediction = biggest_prediction_arr[0][0]
if (sick_pred_number < healthy_pred_number):
    reverse_predic_value = 1 - final_biggest_prediction
    print("debug purposes " + str(reverse_predic_value))
    print('You are not sick ||| you have a change of ' + str(
        reverse_predic_value * 100) + '% of not having a respiratory disease')
else:
    isSick = True
    print('You are sick ||| you have a change of ' + str(
        final_biggest_prediction * 100) + '% of having a respiratory disease')

outputJson = { "isSick" : str(isSick),
                "predictionScore" : str(final_biggest_prediction)}

with open('C:/Users/Willestur/Desktop/test/' + folder_name + '/' + folder_name + '.json', 'w') as jsonFile:
    json.dump(outputJson, jsonFile)