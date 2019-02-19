python ../generator/generate.py ../docker/Dockerfile.tensorflow-py37-cpu tensorflow python==3.7
python ../generator/generate.py ../docker/Dockerfile.sonnet-py37-cpu sonnet python==3.7
python ../generator/generate.py ../docker/Dockerfile.mxnet-py37-cpu mxnet python==3.7
python ../generator/generate.py ../docker/Dockerfile.cntk-py37-cpu cntk python==3.7
python ../generator/generate.py ../docker/Dockerfile.keras-py37-cpu keras python==3.7
python ../generator/generate.py ../docker/Dockerfile.pytorch-py37-cpu pytorch python==3.7
python ../generator/generate.py ../docker/Dockerfile.chainer-py37-cpu chainer python==3.7
python ../generator/generate.py ../docker/Dockerfile.theano-py37-cpu theano python==3.7
python ../generator/generate.py ../docker/Dockerfile.lasagne-py37-cpu lasagne python==3.7
python ../generator/generate.py ../docker/Dockerfile.caffe-py37-cpu caffe python==3.7
python ../generator/generate.py ../docker/Dockerfile.torch-cpu torch
python ../generator/generate.py ../docker/Dockerfile.darknet-cpu darknet
python ../generator/generate.py ../docker/Dockerfile.all-py37-cpu tensorflow sonnet mxnet cntk keras pytorch chainer theano lasagne caffe torch darknet python==3.7 onnx
python ../generator/generate.py ../docker/Dockerfile.all-jupyter-py37-cpu tensorflow sonnet mxnet cntk keras pytorch chainer theano lasagne caffe torch darknet python==3.7 onnx jupyter
python ../generator/generate.py ../docker/Dockerfile.tensorflow-py37-cu100 tensorflow python==3.7 --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.sonnet-py37-cu100 sonnet python==3.7 --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.mxnet-py37-cu100 mxnet python==3.7 --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.cntk-py37-cu100 cntk python==3.7 --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.keras-py37-cu100 keras python==3.7 --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.pytorch-py37-cu100 pytorch python==3.7 --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.chainer-py37-cu100 chainer python==3.7 --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.theano-py37-cu100 theano python==3.7 --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.lasagne-py37-cu100 lasagne python==3.7 --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.caffe-py37-cu100 caffe python==3.7 --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.torch-cu100 torch --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.darknet-cu100 darknet --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.all-py37-cu100 tensorflow sonnet mxnet cntk keras pytorch chainer theano lasagne caffe torch darknet python==3.7 onnx --cuda-ver 10.0 --cudnn-ver 7
python ../generator/generate.py ../docker/Dockerfile.all-jupyter-py37-cu100 tensorflow sonnet mxnet cntk keras pytorch chainer theano lasagne caffe torch darknet python==3.7 onnx jupyter --cuda-ver 10.0 --cudnn-ver 7
