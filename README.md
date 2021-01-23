## coco2yolo

coco2yolo(darknet)

using coco's json convert limited images and classes to yolo format 

## install
```python
pip install -r requirements.txt
```

for win10 user may need this to install `pycocotools`
```python
pip install git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI
```

### How to use
before use, you need to download [annotations](http://images.cocodataset.org/annotations/annotations_trainval2017.zip),then you need to change `LIMIT`、`datatype` and so on in`coco2yolo.py`，also change the categories which you want in `classes.txt`. using `generate_train.py` and `generate_val.py` to generate `train.txt` and `val.txt`

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
   generate_train.py
   generate_val.py

     
```