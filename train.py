# coding=utf-8

# test sample images
from keras.callbacks import Callback, ModelCheckpoint

from tools import ModelController

# get the model controller
model_controller = ModelController()
model_controller.show_sample()

# get the model
model = model_controller.get_model()


class LossHistory(Callback):
    def on_train_begin(self, logs={}):
        self.losses = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))


history = LossHistory()
checkpointer = ModelCheckpoint('./model.hdf5', monitor='val_loss', verbose=1, save_best_only=True,
                               save_weights_only=False, mode='auto')

# train the model
model.fit_generator(
    model_controller.get_image_generator(),
    samples_per_epoch=model_controller.BATCH_SIZE,
    nb_epoch=10000,
    validation_data=model_controller.get_image_generator(mode='valid'),
    nb_val_samples=model_controller.VALID_SIZE,
    callbacks=[history, checkpointer]
)

with open('./losses.txt', 'w') as f:
    f.write(history.losses)
