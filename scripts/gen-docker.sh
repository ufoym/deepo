python ../generator/generate.py ../docker/Dockerfile.tensorflow-py38-cpu tensorflow python==3.8
python ../generator/generate.py ../docker/Dockerfile.mxnet-py38-cpu mxnet python==3.8
python ../generator/generate.py ../docker/Dockerfile.keras-py38-cpu keras python==3.8
python ../generator/generate.py ../docker/Dockerfile.pytorch-py38-cpu pytorch python==3.8
python ../generator/generate.py ../docker/Dockerfile.chainer-py38-cpu chainer python==3.8
python ../generator/generate.py ../docker/Dockerfile.darknet-cpu darknet
python ../generator/generate.py ../docker/Dockerfile.paddle-py38-cpu paddle python==3.8
python ../generator/generate.py ../docker/Dockerfile.all-py38-cpu tensorflow mxnet keras pytorch chainer darknet paddle python==3.8 onnx jupyterlab
python ../generator/generate.py ../docker/Dockerfile.tensorflow-py38-cu113 tensorflow python==3.8 --cuda-ver 11.3.1 --cudnn-ver 8
python ../generator/generate.py ../docker/Dockerfile.mxnet-py38-cu113 mxnet python==3.8 --cuda-ver 11.3.1 --cudnn-ver 8
python ../generator/generate.py ../docker/Dockerfile.keras-py38-cu113 keras python==3.8 --cuda-ver 11.3.1 --cudnn-ver 8
python ../generator/generate.py ../docker/Dockerfile.pytorch-py38-cu113 pytorch python==3.8 --cuda-ver 11.3.1 --cudnn-ver 8
python ../generator/generate.py ../docker/Dockerfile.chainer-py38-cu113 chainer python==3.8 --cuda-ver 11.3.1 --cudnn-ver 8
python ../generator/generate.py ../docker/Dockerfile.darknet-cu113 darknet --cuda-ver 11.3.1 --cudnn-ver 8
python ../generator/generate.py ../docker/Dockerfile.paddle-py38-cu113 paddle python==3.8 --cuda-ver 11.3.1 --cudnn-ver 8
python ../generator/generate.py ../docker/Dockerfile.all-py38-cu113 tensorflow mxnet keras pytorch chainer darknet paddle python==3.8 onnx jupyterlab --cuda-ver 11.3.1 --cudnn-ver 8
