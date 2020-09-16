## PART 0 - PREPARE
+ Folder contains dataset, include: data, train.txt (path of data to train), valid.txt (path of data to validation), test.txt (path of data to test)
+ File *.names (names of classes)
+ File pre_weight following these links download:
    + for yolov3.cfg (154 MB): https://pjreddie.com/media/files/darknet53.conv.74
    + for yolov3-tiny.cfg (6 MB): https://drive.google.com/file/d/18v36esoXCh-PsOKwyP2GWrpYDptDY8Zf/view?usp=sharing
    + for yolov4.cfg (162 MB): https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137
    + for yolov4-tiny.cfg (19 MB): https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29

+ Reference: https://github.com/AlexeyAB/darknet
+ Train with letter_box: https://github.com/AlexeyAB/darknet/issues/232#issuecomment-336955485
## PART 1 - EXPLAIN CONFIG FIGURES
### GENERAL
folder_contains_YOLO = path/darknet
+ Type: String
+ Path of folder contains yolo darknet. If you don't have darknet, you leave this section blank. The program will clone darknet on github automatically. 

make_yet = 1
+ Type: Integer 
+ 1 (made) or 0 (not make yet). If make_yet = 1, the program won't make again. If folder_contains_YOLO is blank, please set make_yet = 0 to make file.

dont_show = 0
+ Type: Integer
+ 1 (show plot) or 0 (not show plot, usually apply for using ssh train on the other PC)

cfgFile = cfg/yolov3-tiny-custom.cfg
+ Type: String
+ Path of file *.cfg. Set address and name of file config if it isn't available

dataFile = cfg/yolov3-tiny-custom.data
+ Type: String
+ Path of file *.cfg. Set address and name of file config if it isn't available


### TRAINING
choice = tiny3-3l
+ Type: String
+ List model supported: 'full3', 'tiny3', 'tiny3-3l', 'full4', 'tiny4', 'tiny4-3l'

classes = 1
+ Type: Integer 
+ Number of classes to train

batch = 64		
+ Type: Integer
+ Number of images chosen in each batch

subdivisions = 8	
+ Type: Integer
+ Number of images split from batch to ran on GPU. Number of images train = batch / subdivision

width = 416
+ Type: Integer (value multiple of 32)
+ Resize width of images

height = 416
+ Type: Integer (value multiple of 32)
+ Resize height of images

max_batches = 500200
+ Type: Integer
+ Maximum of iterations

steps = 400000,450000
+ Type: Integer
+ When model run to above iteration, it updates learning rate

train = path/train.txt
+ Type: String
+ Path of file train

valid = path/test.txt		
+ Type: String
+ Path of file validation

names = path/custom.names
+ Type: String
+ Path of file *.names

pre_weight = path/darknet53.conv.74		
+ Type: String
+ Path of file pre-weight

backupFolder = path/backup				
+ Type: String
+ Path of folder backup saves weights


### TESTING
testWeight = path/yolov3-tiny-custom_final.weights
+ Type: String
+ Path of file *.weight

conf_thresh = 0.25
+ Type: Float
+ Confident threshold

iou_thresh = 0.5
+ Type: Float
+ IOU threshold

input_list_images = 
+ Type: String
+ Path of file .txt save list images

output_list_images = ./result.txt
+ Type: String
+ Path of file .txt save results of list images

input_video =
+ Type: String
+ Path of file video

output_video = ./result.mp4
+ Type: String
+ Path of file video output

## PART 2 - RUN
### TRAINING PROCESS
Command on terminal: Enter this script 
* Option 1: $ python run.py train (use default config.txt)
* Option 2: $ python run.py train path/other_config.txt

Next, the program will load model, weight, ... and calculate anchors box, please press "Enter key" when you see the result of anchors (Ex: anchors = 6,4, 130,582, )

Then, the program will run to train automatically and show a chart to illustrate loss, mAP. If you want to save the chart, please press "s". The chart will save in folder "results"


### TESTING PROCESS
Command on terminal: Enter this script 
* Option 1: $ python run.py \<mode\> (use default config.txt)
* Option 2: $ python run.py \<mode\> path/other_config.txt

\<mode\> : 4 modes inference
+ test_image: Test with 1 image
+ test_list_images: Test with list images. The list is file *.txt save path of images
+ test_video: Test with video
+ map: Calculate mAP 

Next, the program will load model, weight,... and show on Terminal request enter the path file to test. If you want to escape, please press Ctrl + "C"

Note: Consider variable dont_show in file config.txt to display or non-display result on monitor