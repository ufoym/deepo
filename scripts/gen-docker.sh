python ../generator/generate.py ../docker/Dockerfile.tensorflow-py27 tensorflow python==2.7
python ../generator/generate.py ../docker/Dockerfile.tensorflow-py36 tensorflow python==3.6
python ../generator/generate.py ../docker/Dockerfile.sonnet-py27 sonnet python==2.7
python ../generator/generate.py ../docker/Dockerfile.sonnet-py36 sonnet python==3.6
python ../generator/generate.py ../docker/Dockerfile.mxnet-py27 mxnet python==2.7
python ../generator/generate.py ../docker/Dockerfile.mxnet-py36 mxnet python==3.6
python ../generator/generate.py ../docker/Dockerfile.cntk-py27 cntk python==2.7
python ../generator/generate.py ../docker/Dockerfile.cntk-py36 cntk python==3.6
python ../generator/generate.py ../docker/Dockerfile.keras-py27 keras python==2.7
python ../generator/generate.py ../docker/Dockerfile.keras-py36 keras python==3.6
python ../generator/generate.py ../docker/Dockerfile.pytorch-py27 pytorch python==2.7
python ../generator/generate.py ../docker/Dockerfile.pytorch-py36 pytorch python==3.6
python ../generator/generate.py ../docker/Dockerfile.chainer-py27 chainer python==2.7
python ../generator/generate.py ../docker/Dockerfile.chainer-py36 chainer python==3.6
python ../generator/generate.py ../docker/Dockerfile.theano-py27 theano python==2.7
python ../generator/generate.py ../docker/Dockerfile.theano-py36 theano python==3.6
python ../generator/generate.py ../docker/Dockerfile.lasagne-py27 lasagne python==2.7
python ../generator/generate.py ../docker/Dockerfile.lasagne-py36 lasagne python==3.6
python ../generator/generate.py ../docker/Dockerfile.caffe-py27 caffe python==2.7
python ../generator/generate.py ../docker/Dockerfile.caffe-py36 caffe python==3.6
python ../generator/generate.py ../docker/Dockerfile.torch torch
python ../generator/generate.py ../docker/Dockerfile.all-py27 tensorflow sonnet mxnet cntk keras pytorch chainer theano lasagne caffe torch python==2.7
python ../generator/generate.py ../docker/Dockerfile.all-py36 tensorflow sonnet mxnet cntk keras pytorch chainer theano lasagne caffe torch python==3.6
python ../generator/generate.py ../docker/Dockerfile.all-py27-jupyter tensorflow sonnet mxnet cntk keras pytorch chainer theano lasagne caffe torch python==2.7 jupyter
python ../generator/generate.py ../docker/Dockerfile.all-py36-jupyter tensorflow sonnet mxnet cntk keras pytorch chainer theano lasagne caffe torch python==3.6 jupyter
