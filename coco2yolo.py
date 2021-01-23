# coding=utf-8
from pycocotools.coco import COCO
import os
import random
import skimage.io as io
from progress.bar import Bar


HOMEDIR = os.path.dirname((os.path.realpath(__file__)))  # 当前目录
LIMIT = 2  # 每个类别的下载限制
datatype = 'train2017'  # json格式
ann_file = '%s/annotations/instances_%s.json' % (HOMEDIR, datatype)
SAVEDIR = os.path.join(HOMEDIR, 'dataset/train')  # 保存路径
img_dir = SAVEDIR


def get_classes():
    categories = {}
    with open('classes.txt', 'r') as f:
        for index, line in enumerate(f):
            line = line.rstrip("\n")
            categories[index] = line
        f.close()
    return categories


def convert(img, ann):
    '''
    转换为yolo格式
    yolo格式为返回的相对位置
    '''
    width = img['width']
    height = img['height']
    dw = 1.0/width
    dh = 1.0/height
    bbox = ann['bbox']  # 提前bounding box
    x_center = bbox[0]+bbox[2]/2.0
    y_center = bbox[1]+bbox[3]/2.0
    w = bbox[2]
    h = bbox[3]
    x_center = x_center*dw
    y_center = y_center*dh
    w = w*dw
    h = h*dh
    return (x_center, y_center, w, h)


if __name__ == '__main__':
    categories = get_classes()  # 类别

    # 创建目录
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    # 读取COCO
    coco = COCO(ann_file)

    for index in range(len(categories)):
        catIds = coco.getCatIds(catNms=[categories[index]]) #对应的分类id
        imgIds = coco.getImgIds(catIds=catIds) #图片id
        imgIds = random.sample(imgIds, min(LIMIT, len(imgIds))) #取一小部分图片id
        # 获取一个类别图的id
        for imgId in Bar('downloading and converting %s'%(categories[index])).iter(imgIds):
            img = coco.loadImgs(imgId)[0]  #获取图片信息
            I = io.imread(img['coco_url']) 
            #保存位置
            img_savepath = os.path.join(img_dir, categories[index])
            if not os.path.exists(img_savepath):
                os.makedirs(img_savepath)
            img_savepath = os.path.join(img_savepath, img['file_name']) #图片保存位置
            io.imsave(img_savepath, I) #保存
            #标签id
            annIds = coco.getAnnIds(
                imgIds=img['id'], catIds=catIds, iscrowd=None)
            #标签
            anns = coco.loadAnns(annIds)
            #标签保存
            label_savepath = img_savepath.replace('jpg', 'txt')
            with open(label_savepath, 'w') as f:
                for ann in anns:
                    #标签转换
                    yolo_ann = convert(img, ann)
                    f.write(str(index)+' ' +
                            ' '.join([str(a) for a in yolo_ann])+'\n')
                f.close()
