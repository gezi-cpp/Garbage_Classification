from ast import increment_lineno
import matplotlib
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.python.keras import activations
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Conv2D,Flatten,MaxPooling2D,Dense,GlobalAveragePooling2D

#主要调整参数
train_file_path=r'D:\python_work\Garbage_Classification\neural_network\dataset\image_train'
validation_file_path=r'D:\python_work\Garbage_Classification\neural_network\dataset\image_val'
img_width,img_height = 256,256
batch_size = 16
label_num=8
train_epochs=5

train_datagen = ImageDataGenerator(
       rescale=1./255,          #归一化
       rotation_range=40,       #旋转
       width_shift_range=0.2,
       height_shift_range=0.2,
       zoom_range=0.2,
       shear_range=0.2,         #错切变换角度
       horizontal_flip=True,    #水平翻转
       )
val_datagen = ImageDataGenerator(
       rescale=1./255,
       )

train_generator = train_datagen.flow_from_directory(
       train_file_path,
       target_size=(img_width, img_height),
       batch_size=batch_size,
       shuffle=True,
       class_mode="categorical", #对类型进行热编码："categorical",返回one-hot 编码标签
       save_format="jpg"
       )

val_generator=val_datagen.flow_from_directory(
       validation_file_path,
       target_size=(img_width,img_height), 
       batch_size=batch_size,
       class_mode='categorical',
       save_format="jpg"
)


from tensorflow.keras.applications.xception import Xception
base_model=Xception(
       include_top=False,
       weights="imagenet",
       input_shape=(img_height,img_width,3),
       pooling='avg'
)
base_model.trainable=False
base_model.summary()
print("模型网络定义：{}层".format(len(base_model.layers)))

model=keras.Sequential()
model.add(base_model)
model.add(Dense(512,activation='relu'))
model.add(Dense(label_num,activation='softmax'))
model.summary()

# model=tf.keras.Sequential()
# model.add(Conv2D(filters=32,kernel_size=3,padding='same',activation='relu',input_shape=(256,256,3))) #多维数据扁平化，变成一维  
# model.add(MaxPooling2D(pool_size=2))

# model.add(Conv2D(filters=64,kernel_size=3,padding='same',activation='relu'))
# model.add(MaxPooling2D(pool_size=2))

# # model.add(Conv2D(filters=32,kernel_size=3,padding='same',activation='relu'))
# # model.add(MaxPooling2D(pool_size=2))

# # model.add(Conv2D(filters=32,kernel_size=3,padding='same',activation='relu'))
# # model.add(MaxPooling2D(pool_size=2))

# model.add(Flatten())
# #model.add(Dense(400,activation='relu'))
# model.add(Dense(1024,activation='relu'))
# model.add(tf.keras.layers.Dropout(0.2)) #添加dropout层，抑制过拟合
# model.add(Dense(84,activation='relu'))
# model.add(tf.keras.layers.Dropout(0.2)) #添加dropout层，抑制过拟合
# model.add(Dense(label_num,activation='softmax'))
# model.summary()

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),loss='categorical_crossentropy',metrics=['acc'])
print("model training...")
history=model.fit(train_generator,epochs=train_epochs,validation_data=val_generator) 

#model saved
model_path=r'D:\python_work\Garbage_Classification\neural_network\model_saved\%s'
model_json=model.to_json()
with open(model_path %"model_json.json",'w') as json_file:
    print("model saving...")
    json_file.write(model_json)
model.save_weights(model_path %"model_weight.h5")
model.save(model_path %"model.h5")
print('model saved.')


#训练过程可视化
print(history.history.keys())
plt.plot(history.epoch,history.history.get('loss'),label='loss')
plt.plot(history.epoch,history.history.get('val_loss'),label='val_loss')
plt.title('loss')
plt.legend()
plt.grid()
plt.show() 

plt.plot(history.epoch,history.history.get('acc'),label='acc')
plt.plot(history.epoch,history.history.get('val_acc'),label='val_acc')
plt.title('accuracy')
plt.legend()
plt.grid()
plt.show()
