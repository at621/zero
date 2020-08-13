import tensorflow as tf
from datetime import datetime
from tensorflow.keras.mixed_precision import experimental as mixed_precision
import trainer.chessModel as cm
import trainer.sequencer as seq
import glob
import onnxmltools
import os

files = glob.glob('C:\\Projects\\ahla\\data\\modelinput\\input*.npz')

s = seq.SimpleFeeder(files, files_per_batch=1, batch_size=1024)
train = s.get_train()
val = s.get_validation()

# Create model
policy = mixed_precision.Policy('mixed_float16')
mixed_precision.set_policy(policy)
config = cm.ModelConfig()
model = cm.ChessModel(config)
model.build()

opt = tf.keras.optimizers.Adam()
losses = ['categorical_crossentropy', 'mean_squared_error']
model.compile(optimizer=opt, loss=losses, metrics=["mae"],
              loss_weights=[0.1, 0.9])

# Profiling and logging callback
logs = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=logs,
                                                      histogram_freq=1,
                                                      profile_batch='100,110')

# Include the epoch in the file name
checkpoint_path = "C:\\Projects\\ahla\\models\\training_2\\cp-{epoch:04d}.ckpt"
checkpoint_dir = os.path.dirname(checkpoint_path)

# Create a callback that saves the model's weights
cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path, 
    verbose=1, 
    save_weights_only=False,
    monitor='val_acc',
    mode='max',
    save_freq='epoch')

model = model.fit(dataset=train,
                 validation_data=val,
                 epochs=7,
                 shuffle=False,
                 callbacks=[tensorboard_callback, cp_callback])

model.save('..\\models\\watsonBrain_v1')

# Save as ONNX model
keras_model = tf.keras.models.load_model('..\\models\\\\watsonBrain_v1')
output_onnx_model = '..\\models\\model_v1.onnx'

# Convert the Keras model into ONNX
onnx_model = onnxmltools.convert_keras(keras_model)

# Save as protobuf
onnxmltools.utils.save_model(onnx_model, output_onnx_model)