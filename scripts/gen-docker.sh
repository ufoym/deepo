python ../generator/generate.py ../docker/Dockerfile.tensorflow-py36-cpu tensorflow python==3.6
python ../generator/generate.py ../docker/Dockerfile.sonnet-py36-cpu sonnet python==3.6
python ../generator/generate.py ../docker/Dockerfile.mxnet-py36-cpu mxnet python==3.6
python ../generator/generate.py ../docker/Dockerfile.cntk-py36-cpu cntk python==3.6
python ../generator/generate.py ../docker/Dockerfile.keras-py36-cpu keras python==3.6
python ../generator/generate.py ../docker/Dockerfile.pytorch-py36-cpu pytorch python==3.6
python ../generator/generate.py ../docker/Dockerfile.chainer-py36-cpu chainer python==3.6
python ../generator/generate.py ../docker/Dockerfile.theano-py36-cpu theano python==3.6
python ../generator/generate.py ../docker/Dockerfile.lasagne-py36-cpu lasagne python==3.6
python ../generator/generate.py ../docker/Dockerfile.caffe-py36-cpu caffe python==3.6
python ../generator/generate.py ../docker/Dockerfile.torch-cpu torch
python ../generator/generate.py ../docker/Dockerfile.darknet-cpu darknet
python ../generator/generate.py ../docker/Dockerfile.all-py36-cpu tensorflow sonnet mxnet cntk keras pytorch chainer theano lasagne caffe torch darknet python==3.6 onnx jupyter
python ../generator/generate.py ../docker/Dockerfile.tensorflow-py36-cu101 tensorflow python==3.6 --cuda-ver 10.1 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.sonnet-py36-cu101 sonnet python==3.6 --cuda-ver 10.1 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.mxnet-py36-cu101 mxnet python==3.6 --cuda-ver 10.1 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.cntk-py36-cu101 cntk python==3.6 --cuda-ver 10.1 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.keras-py36-cu101 keras python==3.6 --cuda-ver 10.1 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.pytorch-py36-cu101 pytorch python==3.6 --cuda-ver 10.1 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.chainer-py36-cu101 chainer python==3.6 --cuda-ver 10.1 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.theano-py36-cu101 theano python==3.6 --cuda-ver 10.1 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.lasagne-py36-cu101 lasagne python==3.6 --cuda-ver 10.1 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.caffe-py36-cu101 caffe python==3.6 --cuda-ver 10.1 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.torch-cu101 torch --cuda-ver 10.1 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.darknet-cu101 darknet --cuda-ver 10.1 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.all-py36-cu101 tensorflow sonnet mxnet cntk keras pytorch chainer theano lasagne caffe torch darknet python==3.6 onnx jupyter --cuda-ver 10.1 --cudnn-ver 7
