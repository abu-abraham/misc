import tensorflow as tf
a = tf.constant(2)
b = tf.constant(3)
x = tf.add(a, b)
with tf.Session() as sess:
	print(sess.run(x))
writer = tf.summary.FileWriter('./graphs', tf.get_default_graph())
with tf.Session() as sess:
	# writer = tf.summary.FileWriter('./graphs', sess.graph) # if you prefer creating your writer using session's graph
	print(sess.run(x))
writer.close()