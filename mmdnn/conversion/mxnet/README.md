# MXNet README

## Usage

### Extract MXNET model

You can download some pre-trained models from [MXNet Model Gallery](https://github.com/dmlc/mxnet-model-gallery).

### Convert architecture from MXNET to IR

You can convert only network structure to IR for visualization or training in other frameworks.

```bash
~/ModelConverter$ python -m conversion._script.convertToIR -f mxnet -n mxnet/models/resnet-50-symbol.json -d resnet50 --inputShape 3 224 224
.
.
.
IR network structure is saved as [resnet50.json].
IR network structure is saved as [resnet50.pb].
Warning: weights are not loaded.
```

### Convert model (including architecture and weights) from MXNet to IR

You can use following bash command to convert both the network architecture and with weights to IR files.

> The input data shape is not in the architecture description of MXNet, we need to specify the data shape in conversion command.

```bash
~/ModelConverter$ python -m conversion._script.convertToIR -f mxnet -n mxnet/models/resnet-50-symbol.json -w mxnet/models/resnet-50-0000.params -d resnet50 --inputShape 3 224 224
.
.
.
IR network structure is saved as [resnet50.json].
IR network structure is saved as [resnet50.pb].
IR weights are saved as [resnet50.npy].
```

### Convert models from IR to MXNet code snippet and weights

We need to generate both MXNet architecture code snippet and weights file to build the MXNet network.

> Arugment 'dw' is used to specify the converted MXNet model file name for next step use.

```bash
~/ModelConverter$ python -m conversion._script.IRToCode -f mxnet --IRModelPath inception_v3.pb --dstModelPath mxnet_inception_v3.py --IRWeightPath inception_v3.npy -dw mxnet_inception_v3-0000.params

Parse file [inception_v3.pb] with binary format successfully.
Detect input layer [input_1] using infer batch size, set it as default value [1]
Target network code snippet is saved as [mxnet_inception_v3.py].
```

### Convert models from IR to MXNet checkpoint file

After generating the MXNet code snippet and weights, you can take a  further step to generate an original MXNet checkpoint file.

```bash
~/ModelConverter$ python3 -m conversion.examples.mxnet.imagenet_test -n mxnet_inception_v3 -w mxnet_inception_v3-0000.params --dump inception_v3
.
.
.
MXNet checkpoint file is saved as [inception_v3], generated by [mxnet_inception_v3.py] and [mxnet_inception_v3-0000.params].
```

Then the output files *inception_v3-symbol.json* and *inception_v3-0000.params* can be loaded by MXNet directly.

---

## Limitation

- Currently no RNN related operations support