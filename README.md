## coco2yolo

coco2yolo(darknet)

using coco's json convert limited images and classes to yolo format 

## install
```python
git clone https://github.com/qxdn/coco2yolo.git
pip install -r requirements.txt
```

for win10 user may need this to install `pycocotools`
```python
pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI
```

### How to use
changed `classes.txt`
```python
python coco2yolo.py -l 100 -t train
python generate.py -t train
```

```
- HOMEDIR/
   - annotaions/
   |    instances_train2017.json
   |    instances_val2017.json
   - dataset/
   |    - train
   |    |   ******.jpg
   |    |   ******.txt
   |    - val
   |    |   ******.jpg
   |    |   ******.txt
   |    train.txt
   |    val.txt
   classes.txt
   coco2yolo.py
   generate.py
```