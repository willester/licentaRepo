from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import sys
import cv2

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

photoToBeResized = cv2.imread('C:/Users/Willestur/Desktop/test/' + folder_name + '/folderSecundar/' + folder_name + '.png')
resizeImg = cv2.resize(photoToBeResized, (300, 300))
cv2.imwrite('C:/Users/Willestur/Desktop/test/' + folder_name + '/folderSecundar/' + folder_name + '.png', resizeImg)

image_shape = (300, 300, 1)
batch_size = 1
test_images_generator = image_generator.flow_from_directory(path_test_imagine, target_size=image_shape[:2],
                                                  color_mode='grayscale',
                                                  batch_size=batch_size,
                                                  class_mode='binary',
                                                  shuffle=False)
print(loaded_model.predict(test_images_generator))
tupple = ()
prob_list = list(tupple)
for i in range(50):
    prob_list.append(loaded_model.predict(test_images_generator))

sick_pred_number = 0
healthy_pred_number = 0
biggest_prediction_arr = 0
biggest_sick_prediction_arr = 0


for i in prob_list:
    if biggest_prediction_arr < i:
        biggest_prediction_arr = i
    if i <= 0.5:
        sick_pred_number = sick_pred_number + 1
        if biggest_sick_prediction_arr < i:
            biggest_sick_prediction_arr = i
    else:
        healthy_pred_number = healthy_pred_number + 1

isSick = False
final_biggest_prediction = biggest_prediction_arr[0][0]
diagnosis = "After several tests, there are no certain signs of a present disease, the accuracy of the prediction being " + str(round(final_biggest_prediction*100)) + "%"
if sick_pred_number >= healthy_pred_number:
    isSick = True
    final_biggest_prediction = biggest_sick_prediction_arr[0][0]
    diagnosis = "After several tests, there are certain signs of a present disease"


outputJson = { "diagnosis": diagnosis,
                # "predictionScore": str(final_biggest_prediction),
               "folderName": str(folder_name)}

with open('C:/Users/Willestur/Desktop/test/' + folder_name + '/' + folder_name + '.json', 'w') as jsonFile:
    json.dump(outputJson, jsonFile)