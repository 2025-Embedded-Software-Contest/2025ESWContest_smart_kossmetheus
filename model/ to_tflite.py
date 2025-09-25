import tensorflow as tf
m = tf.keras.models.load_model('model/c1001_lstm_corrector.h5')
conv = tf.lite.TFLiteConverter.from_keras_model(m)
conv.optimizations = [tf.lite.Optimize.DEFAULT]
open('model/c1001_lstm_corrector.tflite','wb').write(conv.convert())
