## General algorithm outlines

1. Import or generate data
2. Transform and normalize data
3. Set algorithm parameters
4. Placeholders and Variables
5. Operations (model structure)
6. Loss functions
7. Optimizer
8. Initialize
9. Train
10. Eval and predict


## Summary

In tf we have to setup data, variables, placeholders and model before we tell the program to train and change the variables to improve the predictions.

Tf accomplishes this through the computational graph.

We tell tf to minimize a loss function and tf does it by modifying the variables in the model. Tf knows how to modify the variables because it automatically computes the gradients for every variable.

We setup this cycle as a computational graph and (1) feed in data through the placeholders, (2) calculate the output of the computational graph, (3) compare the output of the desired output with a loss function, (4) modify the model variables according to the automatic back propagation, and finally (5) repeat the process until a stopping criteria is met.

# index

### ch1

Tensors
Variables and Placeholders
Matrics
Operations
Activation Func

### ch2

# Additional Resources

###Official Resources:

- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials/)
- [Udacity Deep Learning Class](https://www.udacity.com/course/deep-learning--ud730)
- [TensorFlow Playground](http://playground.tensorflow.org/)
- [Tutorials by pkmital](https://github.com/pkmital/tensorflow_tutorials)
- [Tutorials by nlintz](https://github.com/nlintz/TensorFlow-Tutorials)
- [TensorFlow Workshop by amygdala](https://github.com/amygdala/tensorflow-workshop)

###Deep Learning Resources

- [Efficient Back Prop by Yann LeCun, et. al.](http://yann.lecun.com/exdb/publis/pdf/lecun-98b.pdf)
- [Online Deep Learning Book, MIT Press](http://www.deeplearningbook.org/)
- [An Overview of Gradient Descent Algorithms by Sebastian Ruder](http://sebastianruder.com/optimizing-gradient-descent/)
- [Stochastic Optimization by John Duchi, et. al.](http://www.jmlr.org/papers/volume12/duchi11a/duchi11a.pdf)
- [ADADELTA Method by Matthew Zeiler](http://arxiv.org/abs/1212.5701)
- [A Friendly Introduction to Cross-Entropy Loss by Rob DiPietro](http://rdipietro.github.io/friendly-intro-to-cross-entropy-loss/)

###Additional Resources

- [A Curated List of Dedicated TensorFlow Resources](https://github.com/jtoy/awesome-tensorflow/)
