import tensorflow as tf

print("Cheking TF GPUs")
print(tf.config.list_physical_devices("GPU"))
