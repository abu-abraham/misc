import tensorflow as tf
import os

def basic_ops():
    x = 2
    y = 3
    op1 = tf.add(x,y)
    op2 = tf.multiply(x,y)
    op3 = tf.pow(op2,op1)
    with tf.Session() as sess:
        print sess.run(op3)

def graph_trial():
    g = tf.Graph()
    x = None
    with g.as_default():
        a = 3
        b = 5
        x = tf.add(a,b)
    sess = tf.Session(graph=g)
    print sess.run(x)
    sess.close()

def file_writter1():
    a = tf.constant(2)
    b = tf.constant(3)
    x = tf.add(a, b)
    with tf.Session() as sess:
        writer = tf.summary.FileWriter('./graphs', sess.graph)
        print sess.run(x)
    writer.close()

def file_writter2():
    a = tf.constant(2, name = "a")
    b = tf.constant(3, name = "b")
    x = tf.add(a, b, name = "add")
    with tf.Session() as sess:
        writer = tf.summary.FileWriter('./graphs', sess.graph)
        print sess.run(x)
    writer.close() 
    

def constants_trial():
    a = tf.constant([2,2], name = "a",shape = [1,2])
    b = tf.constant([[0,1],[2,3]],name = "b",shape=[2,2])
    x = tf.add(a,b, name = "add")
    y = tf.multiply(a,b, name = "mul")
    with tf.Session() as sess:
        x,y = sess.run([x,y])
        print x

def constants_trial1():
    a = tf.constant([2,2], name = "a",shape = [1,2])
    b = tf.constant([[0,1],[2,3]],name = "b",shape=[2,2])
    c = tf.zeros_like(b)
    with tf.Session() as sess:
        print sess.run(c)
    
        
def variable_trial():
    a = tf.Variable(2, name = "scalr")
    b = tf.Variable(3, name = "sc")
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        print sess.run(tf.add(a,b))

def session_sep_copy_ex():
    W = tf.Variable(10)
    sess1 = tf.Session()
    sess2 = tf.Session()

    sess1.run(W.initializer)
    sess2.run(W.initializer)

    print sess1.run(W.assign_add(10))
    print sess2.run(W.assign_sub(2))

    sess1.close()
    sess2.close()


def placeholder_trial():
    a = tf.placeholder(tf.float32,shape = [3])
    b = tf.constant([5,5,5], tf.float32)
    c = a+b #short for tf.add
    with tf.Session() as sess:
        print sess.run(c,{a:[1,2,3]})

def placeholder_trial_feed():
    a = tf.add(1,1)
    b = tf.multiply(a,3)
    with tf.Session() as sess:
        replace_dict = {a:15}
        print sess.run(b,feed_dict=replace_dict)

def lazy_loading_example():
    x = tf.Variable(10, name='x')
    y = tf.Variable(20, name='y')

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for _ in range(2):
            sess.run(tf.add(x, y))
        print(tf.get_default_graph().as_graph_def()) 

