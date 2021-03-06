# coding=utf-8
from collections import defaultdict
from pycocotools.coco import COCO
import os
import random
import skimage.io as io
from tqdm import tqdm


classes = ['person',
           'bicycle',
           'car',
           'motorcycle',
           'bus',
           'truck'
           ]

counter = {}

for c in classes:
    counter[c] = 0


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


def get_args():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-l', '--limit', help="download images number of each categories", type=int, default=2)
    parser.add_argument('-t', '--type', help='the type of annotations',
                        choices=['train', 'val'], default='train')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    if args.limit <= 0:
        print('download limits must larger than zero')
        exit(1)

    limit = args.limit
    HOMEDIR = os.path.dirname((os.path.realpath(__file__)))  # 当前目录
    datatype = args.type + '2017'  # json格式
    ann_file = '%s/annotations/instances_%s.json' % (HOMEDIR, datatype)
    SAVEDIR = os.path.join(HOMEDIR, 'dataset/'+args.type)  # 保存路径
    img_dir = SAVEDIR

    categories = classes  # 类别

    # 创建目录
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    # 读取COCO
    coco = COCO(ann_file)

    for index, cat in enumerate(categories):
        catIds = coco.getCatIds(catNms=[cat])  # 对应的分类id
        imgIds = coco.getImgIds(catIds=catIds)  # 图片id
        imgIds = random.sample(imgIds, min(limit, len(imgIds)))  # 取一小部分图片id
        # 获取一个类别图的id
        pbar = tqdm(imgIds)
        pbar.set_description("Processing %s" % cat)
        for imgId in pbar:
            img = coco.loadImgs(imgId)[0]  # 获取图片信息
            I = io.imread(img['coco_url'])
            # 保存位置
            img_savepath = os.path.join(
                img_dir, img['file_name'])  # 图片保存位置
            io.imsave(img_savepath, I)  # 保存
            # 获取所有可能的标签id
            catIds = coco.getCatIds(catNms=categories)
            # 标签id 不要crowd
            annIds = coco.getAnnIds(
                imgIds=img['id'], catIds=catIds, iscrowd=0)
            # 标签
            anns = coco.loadAnns(annIds)
            # 标签保存
            label_savepath = img_savepath.replace('jpg', 'txt')
            with open(label_savepath, 'w') as f:
                for ann in anns:
                    # 标签转换
                    yolo_ann = convert(img, ann)
                    category_id = ann['category_id']
                    cat_name = coco.loadCats(category_id)[0]['name']
                    counter[cat_name] += 1
                    cat_index = categories.index(cat_name)
                    f.write(str(cat_index)+' ' +
                            ' '.join([str(a) for a in yolo_ann])+'\n')
                f.close()

    print(counter)
    filename = 'counter.txt'
    with open(filename, 'w') as f:
        for k, v in counter.items():
            f.write("{}:{}\n".format(k, v))
