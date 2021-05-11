from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json
import sys
import matplotlib.pyplot as plt
import numpy as np

folder_name = sys.argv[1]

print("in python file 2")

image_generator = ImageDataGenerator(rotation_range=25,
                                    width_shift_range=0.2,
                                     height_shift_range=0.2,
                                     shear_range=0.1,
                                     zoom_range=0.2,
                                     horizontal_flip=True,
                                     fill_mode='nearest')

loaded_model = load_model('E:/Faculta/_LICENTA/_Aplicatie/pozeModel2SauModelCuToateBolile/checkPointComplexModel61Accuracy.h5')

path_test_imagine = 'C:/Users/Willestur/Desktop/test/' + folder_name
image_shape = (300, 300, 1)
batch_size = 1
test_images_generator = image_generator.flow_from_directory(path_test_imagine, target_size=image_shape[:2],
                                                  color_mode='grayscale',
                                                  batch_size=batch_size,
                                                  # class_mode='binary',
                                                  class_mode='categorical',
                                                  shuffle=False)

diagnosisResults = (loaded_model.predict(test_images_generator)*100)
outputJson = { "Atelectasis": str(diagnosisResults[0][0]),
               "Cardiomegaly": str(diagnosisResults[0][1]),
               "Consolidation": str(diagnosisResults[0][2]),
               "Edema": str(diagnosisResults[0][3]),
               "Effusion": str(diagnosisResults[0][4]),
               "Emphysema": str(diagnosisResults[0][5]),
               "Fibrosis": str(diagnosisResults[0][6]),
               "Hernia": str(diagnosisResults[0][7]),
               "Infiltration": str(diagnosisResults[0][8]),
               "Mass": str(diagnosisResults[0][9]),
               "Nodule": str(diagnosisResults[0][11]),
               "NoFindigs": str(diagnosisResults[0][10]),
               "PleuralFindings": str(diagnosisResults[0][12]),
               "Pneumonia": str(diagnosisResults[0][13]),
               "Pneumothorax": str(diagnosisResults[0][14])}

diseasesList = ["Atelectasis", "Cardiomegaly", "Consolidation", "Edema", "Effusion", "Emphysema", "Fibrosis", "Hernia",
                "Infiltration", "Mass", "NoFindigs", "Nodule", "PleuralFindings", "Pneumonia", "Pneumothorax"]

height = []
for i in range(15):
    height.append(diagnosisResults[0][i])

x_pos = np.arange(len(diseasesList))
plt.figure(figsize=(5, 7))
plt.bar(x_pos, height, color=(0.5, 0.1, 0.5, 0.6))
plt.title('% of having a specific disease')
plt.xlabel('diseases')
plt.ylabel('% of having the disease')
plt.xticks(x_pos, diseasesList, rotation=45, horizontalalignment='right')
plt.savefig("C:/Users/Willestur/Desktop/test/public/diagnosisCharts/" + folder_name + "DiagnosisChart.png")

with open('C:/Users/Willestur/Desktop/test/' + folder_name + '/' + folder_name + 'Rediagnose.json', 'w') as jsonFile:
    json.dump(outputJson, jsonFile)
