import tensorflow as tf
hello = tf.constant('hello,tensorflo')
sess = tf.Session()
print(sess.run(hello))