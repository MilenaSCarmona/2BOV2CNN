import os
from sys import argv
from keras import applications
from numpy import resize, expand_dims, argmax
from keras.preprocessing.image import load_img, img_to_array
from keras.models import load_model
from sklearn.metrics import confusion_matrix, accuracy_score

dict_preprocessing = {}
dict_preprocessing['xception'] = applications.xception.preprocess_input, applications.xception.decode_predictions
dict_preprocessing['vgg16'] = applications.vgg16.preprocess_input, applications.vgg16.decode_predictions
dict_preprocessing['vgg19'] = applications.vgg19.preprocess_input, applications.vgg19.decode_predictions
dict_preprocessing['resnet50'] = applications.resnet50.preprocess_input, applications.resnet50.decode_predictions
dict_preprocessing['inception'] = applications.inception_v3.preprocess_input, applications.inception_v3.decode_predictions

h5_path = argv[1]
app = argv[2]
model = load_model(h5_path)
test_dir = '../data/test/'
classes = os.listdir(test_dir)
classes.sort()

def single_classify(image_path):
    preprocess_input, decode_predictions = dict_preprocessing[app]
    pil_image = load_img(image_path)
    np_image = img_to_array(pil_image)
    res_image = resize(np_image, (256, 256, 3))
    tensor = expand_dims(res_image, axis=0)
    tensor = preprocess_input(tensor)
    predict = model.predict(tensor)
    predict = argmax(predict, axis=1)
    return predict[0]
    
def get_predicted():
    for class_ in classes:
        imgs = os.listdir(test_dir + class_)
        imgs.sort()
        for img in imgs:
            image_path = test_dir + class_ + '/' + img
            yield single_classify(image_path)

real = []
for i, class_ in enumerate(classes):
    imgs = os.listdir(test_dir + class_)
    real.extend([i]*len(imgs))
predicted = list(get_predicted())

print ('acc:')
print round(100.*accuracy_score(real, predicted), 2)
