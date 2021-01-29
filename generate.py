import os

def get_args():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-t','--type',help='the type of annotations',choices=['train','val'],default='train')

    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    dataset_path = 'dataset'
    img_path = args.type
    save_filename = args.type +'.txt'
    root_path = os.path.join(os.getcwd(),dataset_path)
    img_path = os.path.join(root_path,img_path)
    os.chdir(root_path)
    image_file = []
    for filename in os.listdir(img_path):
        if filename.endswith('.jpg'):
            image_filename = os.path.join(img_path,filename)
            image_file.append(image_filename)
    with open(save_filename,'w') as f:
        for image in image_file:
            f.write(image)
            f.write('\n')
        f.close()
    