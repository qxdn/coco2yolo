import os

train_path = 'dataset'
train_img_path='val'

if __name__ == '__main__':
    root_path = os.path.join(os.getcwd(),train_path)
    train_img_path = os.path.join(root_path,train_img_path)
    os.chdir(root_path)
    image_file = []
    for dir in os.listdir(train_img_path):
        for filename in os.listdir(train_img_path):
            if filename.endswith('.jpg'):
                image_filename = os.path.join(train_img_path,filename)
                image_file.append(image_filename)
    with open('val.txt','w') as f:
        for image in image_file:
            f.write(image)
            f.write('\n')
        f.close()
    