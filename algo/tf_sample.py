# Import TensorFlow
import tensorflow as tf

# Define a and b as placeholders
a = tf.placeholder(dtype=tf.int8)
b = tf.placeholder(dtype=tf.int8)

# Define the addition
c = tf.add(a, b)

# Initialize the graph
graph = tf.Session()

# Run the graph
x = graph.run(c, feed_dict={a: 5, b: 4})
print(x)
