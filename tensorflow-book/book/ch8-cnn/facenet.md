人脸识别的技术难点： 人脸的结构相似，人脸的外形不稳定。

人脸识别的经典流程： 1.人脸检测，2.人脸对齐，3.人脸特征表示。

2015 年 google 的研究人员在 CVPR2015 发表 faceNet,并在 LFW (labeled faces in the wild) 人脸识别数据集上达到 99.63%精度。

人脸识别应用场景： 安防，安检，个人相册管理，支付，KYC。

典型数据集： LFW, youtube faces db, CASIA-WebFace, FDDB, WIDER FACE, CELEBA

## 算法简介

#### 人脸检测 (Face Detection)

发展阶段： 基于模板匹配的算法 -> 基于 adaboost 的框架 -> 基于深度学习的算法

基于深度学习的算法： Cascade CNN 和 MTCNN.

#### 人脸对齐 (Face Alignment)

#### 人脸特征表示 (Feature Representation)

## facebook DeepFace

2014 年发布。他们使用 3D 模型来解决人脸对齐问题，同时又使用了 9 层深度神经网络来做人脸特征表示。
损失函数使用了 softmax，最后通过特征嵌入(feature embedding)得到固定长度的人脸特征向量。

DeepFace 在 LFW 取得了 97.35%的 acc

## google FaceNet

google 创新地提出了使用三元组损失函数(Triplet loss)代替 softmax loss，在一个超球空间上进行优化使得类内距离更紧凑，类间距离更远，最后得到了一个紧凑的 128 维人脸。其网络使用 Inception 模型，模型参数量小，精度也更高。FaceNet 在 LFW 上取得了 99.63 的准确率。

## 小工具(face_recognition)
