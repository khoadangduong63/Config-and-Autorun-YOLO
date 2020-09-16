import os
import sys
import glob
import matplotlib.pyplot as plt



def fcheckExistFile(folder_contains_YOLO, path):
    if os.path.isfile(path) == False:
        path = os.path.join(folder_contains_YOLO, path)
        return os.path.isfile(path), path
    return True, os.path.abspath(path)



def fcheckExistDir(folder_contains_YOLO, path):
    if os.path.isdir(path) == False:
        path = os.path.join(folder_contains_YOLO, path)
        return os.path.isdir(path), path
    return True, os.path.abspath(path)


def training(path_file_config, folder_contains_YOLO):
    fsource = open(path_file_config,"r")

    dont_show = ""
    choice = ""
    classes = ""
    batch = ""
    subdivisions = ""
    width = ""
    height = ""
    max_batches = ""
    steps = ""
    train = ""
    valid = ""
    names = ""
    backup = ""
    pretrained_weight = ""

    checkTrueInput = True
    for line in fsource.readlines():    
        line = line.strip() # Handle white space and \n
        if "#" in line:
            list_split = line.split("#")
            if len(list_split) == 1:
                continue
            else:
                line = list_split[0]
                
        if "dont_show" in line:
            dont_show = line.split("=")[1].strip()
        elif "cfgFile" in line:
            cfgFile = line.split("=")[1].strip()
            cfgFile = os.path.join(folder_contains_YOLO, cfgFile)
            if os.path.isdir(os.path.dirname(cfgFile)) == False:
                os.makedirs(os.path.dirname(cfgFile))
        elif "dataFile" in line:
            dataFile = line.split("=")[1].strip()
            dataFile = os.path.join(folder_contains_YOLO, dataFile)
            if os.path.isdir(os.path.dirname(dataFile)) == False:
                os.makedirs(os.path.dirname(dataFile))
        elif "choice" in line: # choice = 1
            choice = line.split("=")[1].strip()
            choices = ['full3', 'tiny3', 'tiny3-3l', 'full4', 'tiny4', 'tiny4-3l']
            if choice not in choices:
                print("Wrong input field choice")
                checkTrueInput = False
                break
        elif "classes" in line: # classes = 1
            classes = line.split("=")[1].strip()
            if (not classes.isdigit() or int(classes) < 1):
                print("Wrong input field classes")
                checkTrueInput = False
                break
        elif "batch" in line and "max_batches" not in line: # batch = 64
            batch = line.split("=")[1].strip()
            if (not batch.isdigit() or int(batch) < 1):
                print("Wrong input field batch")
                checkTrueInput = False
                break
        elif "subdivisions" in line: # subdivisions = 8
            subdivisions = line.split("=")[1].strip()
            if (not subdivisions.isdigit() or int(subdivisions) < 1):
                print("Wrong input field subdivisions")
                checkTrueInput = False
                break
        elif "width" in line: # width = 416
            width = line.split("=")[1].strip()
            if (not width.isdigit() or int(width) % 32 != 0):
                print("Wrong input field width")
                checkTrueInput = False
                break
        elif "height" in line: # height = 416
            height = line.split("=")[1].strip()
            if (not height.isdigit() or int(height) % 32 != 0):
                print("Wrong input field height")
                checkTrueInput = False
                break
        elif "max_batches" in line:
            max_batches = line.split("=")[1].strip()
            if (not max_batches.isdigit() or int(max_batches) < 1):
                print("Wrong input field max_batches")
                checkTrueInput = False
                break
        elif "steps" in line and "policy" not in line:
            steps = line.split("=")[1].strip()
            step1 = steps.split(",")[0].strip()
            step2 = steps.split(",")[1].strip()
            if (not step1.isdigit() or not step2.isdigit() or int(step1) < 1 or int(step2) < 1 or int(step1) >= int(step2) or int(step1) > int(max_batches) or int(step2) > int(max_batches)):
                print("Wrong input field steps")
                checkTrueInput = False
                break
        elif "train" in line: # train = NFPAdataset/train.txt
            train = line.split("=")[1].strip()
            checkTrueInput, train = fcheckExistFile(folder_contains_YOLO, train)
            if checkTrueInput == False:
                print("Wrong path input field train. The file does not exist")
                break
        elif "valid" in line:
            valid = line.split("=")[1].strip()
            checkTrueInput, valid = fcheckExistFile(folder_contains_YOLO, valid)
            if checkTrueInput == False:
                print("Wrong path input field valid. The file does not exist")
                break
        elif "names" in line:
            names = line.split("=")[1].strip()
            checkTrueInput, names = fcheckExistFile(folder_contains_YOLO, names)
            if checkTrueInput == False:
                print("Wrong path input field names. The file does not exist")
                break
        elif "backupFolder" in line:
            backup = line.split("=")[1].strip()
            checkTrueInput, backup = fcheckExistDir(folder_contains_YOLO, backup)
            if checkTrueInput == False:
                print("Wrong path input field backup. The directory does not exist")
                break
        elif "pre_weight" in line:
            pretrained_weight = line.split("=")[1].strip()
            if pretrained_weight != "":
                checkTrueInput, pretrained_weight = fcheckExistFile(folder_contains_YOLO, pretrained_weight)
            if checkTrueInput == False:
                print("Wrong path input field pre_weight. The file does not exist")
                break


    if checkTrueInput == True:
        if choice == 'full3':
            fin = open(os.path.join(folder_contains_YOLO,"cfg","yolov3.cfg"),"r")
        elif choice == 'tiny3':
            fin = open(os.path.join(folder_contains_YOLO,"cfg","yolov3-tiny.cfg"),"r")
        elif choice == 'tiny3-3l':
            fin = open(os.path.join(folder_contains_YOLO,"cfg","yolov3-tiny_3l.cfg"),"r")
        elif choice == 'full4':
            fin = open(os.path.join(folder_contains_YOLO,"cfg","yolov4.cfg"),"r")
        elif choice == 'tiny4':
            fin = open(os.path.join(folder_contains_YOLO,"cfg","yolov4-tiny-custom.cfg"),"r")
        elif choice == 'tiny4-3l':
            fin = open(os.path.join(folder_contains_YOLO,"cfg","yolov4-tiny-3l.cfg"),"r")
        
        answer = ""
        if os.path.isfile(dataFile):
            answer = input("Data file is exist, do you want to replace it? Y (Yes) or N (No): ") 
            while answer!= "Y" and answer != "y" and answer != "N" and answer != "n":
                answer = input("Please press Y or N. Your answer is: ")
        if answer == "Y" or answer == "y" or os.path.isfile(dataFile) == False:            
            fout_data = open(dataFile,"w")

            ################################ Modify file data ################################
            fout_data.write("classes = " + classes + "\n")
            fout_data.write("train = " + train + "\n")
            fout_data.write("valid = " + valid + "\n")
            fout_data.write("names = " + names + "\n")
            fout_data.write("backup = " + backup + "\n")
            fout_data.close()


        ################################ Modify file config ################################
        if os.path.isfile(cfgFile):
            answer = input("Cfg file is exist, do you want to replace it? Y (Yes) or N (No): ") 
            while answer!= "Y" and answer != "y" and answer != "N" and answer != "n":
                answer = input("Please press Y or N")
        if answer == "Y" or answer == "y" or os.path.isfile(cfgFile) == False:
            os.chdir(folder_contains_YOLO)
            if choice in ['full3','tiny3-3l','full4','tiny4-3l']:
                cmd = "./darknet detector calc_anchors " + dataFile + " -num_of_clusters 9 -width " + width + " -height " + height
            else:
                cmd = "./darknet detector calc_anchors " + dataFile + " -num_of_clusters 6 -width " + width + " -height " + height

            
            print("\n******* Notice: Please press Enter key to continue when you see the result of anchors!!! *******\n")
            input("Press Enter key to confirm that you read above notice...")
            os.system(cmd)

            if os.path.isfile("anchors.txt") == False:
                if choice in ['full3','tiny3-3l','full4','tiny4-3l']:
                    print("Your dataset is not enough label for each image, the program cannot calculate anchors. Anchors will set default original yolov3.cfg")
                    anchors = "10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326"
                else:
                    print("Your dataset is not enough label for each image, the program cannot calculate anchors. Anchors will set default original yolov3-tiny.cfg")
                    anchors = "10,14,  23,27,  37,58,  81,82,  135,169,  344,319"
            else:
                fanchors = open("anchors.txt", "r")
                for line in fanchors.readlines():
                    line = line.strip()
                    if line != "":
                        anchors = line
                fanchors.close()


            fout_cfg = open(cfgFile,"w")
            checkMiddleFile = False
            checkConvolutional = False
            checkSizeIsNextLine = False

            fin.seek(0,0)
            fout_cfg.seek(0,0)
            for line in fin.readlines():
                if checkMiddleFile == False:
                    # Modify batch
                    if "batch" in line and "#" not in line and "max_batches" not in line:
                        line = line.split("=")[0] + "=" + batch + "\n"
                        fout_cfg.write(line)    

                    # Modify subdivisions
                    elif "subdivisions" in line and "#" not in line:
                        line = line.split("=")[0] + "=" + subdivisions + "\n"
                        fout_cfg.write(line)

                    # Modify width
                    elif "width" in line:
                        line = "width=" + width + "\n"
                        fout_cfg.write(line)

                    # Modify height
                    elif "height" in line:
                        line = "height=" + height + "\n"
                        fout_cfg.write(line)
                    
                    elif "max_batches" in line:
                        line = "max_batches=" + max_batches + "\n"
                        fout_cfg.write(line)

                    elif "steps" in line and "policy" not in line:
                        line = "steps=" + step1 + "," + step2 + "\n"
                        fout_cfg.write(line)
                        checkMiddleFile = True

                    else:
                        fout_cfg.write(line)
                else:          
                    # Modify class
                    if "classes" in line:
                        line = "classes=" + classes + "\n"
                        fout_cfg.write(line)

                    # Modify anchors
                    elif "anchors" in line:
                        if len(anchors) != 0: 
                            line = "anchors = " + anchors + "\n"
                            fout_cfg.write(line) 

                    # Modify filters
                    elif checkSizeIsNextLine == False:
                        if "[convolutional]" in line:
                            checkConvolutional = True
                            fout_cfg.write(line)
                            continue

                        if checkConvolutional == False:
                            fout_cfg.write(line)
                        else:
                            if "size" not in line:
                                checkConvolutional = False    
                            elif "size" in line:
                                checkSizeIsNextLine = True
                            fout_cfg.write(line)
                    else:
                        if "filters" in line:
                            numOfFilters = (int(classes) + 5) * 3
                            line = "filters=" + str(numOfFilters) + "\n"
                            fout_cfg.write(line)
                            checkConvolutional = checkSizeIsNextLine = False
                        else:
                            fout_cfg.write(line)


            

            fsource.close()
            fin.close()
            fout_cfg.close()


        ##########################################################################################################
        #                                               RUN DARKNET                                              #
        ##########################################################################################################

        #./darknet detector train cfg/*.data cfg/*.cfg pretrained_weight
        os.chdir(folder_contains_YOLO)
        if dont_show == '0':
            command = "./darknet detector train " + dataFile + " " + cfgFile + " " + pretrained_weight + " -map"
        else:
            command = "./darknet detector train " + dataFile + " " + cfgFile + " " + pretrained_weight + " -map -dont_show" 
        os.system(command)
        print("Done")

    else:
        fsource.close()
        print("Something were wrong in your file config. Please check format of value and path again!")



def testing(path_file_config, folder_contains_YOLO, mode):
    dont_show = ""
    cfgFile = ""
    dataFile = ""
    weight = ""
    conf_thresh = ""
    iou_thresh = ""
    
    input_list_images = ""
    output_list_images = ""

    input_video = ""
    output_video = ""

    f = open(path_file_config,"r")
    checkTrueInput = True
    for line in f.readlines():
        line = line.strip() # Handle white space and \n
        if "#" in line:
            list_split = line.split("#")
            if len(list_split) == 1:
                continue
            else:
                line = list_split[0]
        
        if "dont_show" in line:
            dont_show = line.split("=")[1].strip()
        elif "cfgFile" in line:
            cfgFile = line.split("=")[1].strip()
            checkTrueInput, cfgFile = fcheckExistFile(folder_contains_YOLO, cfgFile)
            if checkTrueInput == False:
                break
        elif "dataFile" in line:
            dataFile = line.split("=")[1].strip()
            checkTrueInput, dataFile = fcheckExistFile(folder_contains_YOLO, dataFile)
            if checkTrueInput == False:
                break
        elif "testWeight" in line:
            weight = line.split("=")[1].strip()
            checkTrueInput, weight = fcheckExistFile(folder_contains_YOLO, weight)
            if checkTrueInput == False:
                break
        elif "conf_thresh" in line:
            conf_thresh = line.split("=")[1].strip()
            try:
                float(conf_thresh)
            except ValueError:
                conf_thresh = ""
        elif "iou_thresh" in line:
            iou_thresh = line.split("=")[1].strip()
            try:
                float(iou_thresh)
            except ValueError:
                iou_thresh = ""

        elif "input_list_images" in line and mode == "test_list_images":
            input_list_images = line.split("=")[1].strip()
            checkTrueInput, input_list_images = fcheckExistFile(folder_contains_YOLO, input_list_images)
            if checkTrueInput == False:
                break
        elif "output_list_images" in line and mode == "test_list_images":
            output_list_images = line.split("=")[1].strip()
            if os.path.isdir(os.path.dirname(output_list_images)) == False:
                print(output_list_images)
                os.makedirs(os.path.dirname(output_list_images))
        elif "input_video" in line and mode == "test_video":
            input_video = line.split("=")[1].strip()
            checkTrueInput, input_video = fcheckExistFile(folder_contains_YOLO, input_video)
            if checkTrueInput == False:
                break
        elif "output_video" in line and mode == "test_video":
            output_video = line.split("=")[1].strip()
            if os.path.isdir(os.path.dirname(output_video)) == False:
                os.makedirs(os.path.dirname(output_video))

    if checkTrueInput == True:
        os.chdir(folder_contains_YOLO)

        if conf_thresh == "" and iou_thresh == "":
            set_thresh = ""
        else:
            if conf_thresh == "":
                set_thresh = " -iou_thresh " + iou_thresh
            elif iou_thresh == "":
                set_thresh = " -thresh " + conf_thresh
            else:
                set_thresh = " -thresh " + conf_thresh + " -iou_thresh " + iou_thresh

        if dont_show == '0':
            dont_show = ""
        else:
            dont_show = " -dont_show "

        if mode == "test_image":
            command = "./darknet detector test " + dataFile + " " + cfgFile + " " + weight + set_thresh + dont_show
        elif mode == "test_list_images":
            command = "./darknet detector test " + dataFile + " " + cfgFile + " " + weight + set_thresh + dont_show + " -ext_output < " + input_list_images + " > " + output_list_images
        elif mode == "test_video":
            command = "./darknet detector demo " + dataFile + " " + cfgFile + " " + weight + set_thresh + dont_show + " -ext_output " + input_video + " -out_filename  " + output_video
        elif mode == "map":
            command = "./darknet detector map " + dataFile + " " + cfgFile + " " + weight + set_thresh

        print(command)
        os.system(command)
        f.close()
    else:
        f.close()
        print("Something were wrong in your file config. Please check format of value and path again!")


def runMode(mode, path_file_config, folder_contains_YOLO):
    if mode == "train":
        training(path_file_config, folder_contains_YOLO)
    elif mode == "test_image" or mode == "test_list_images" or mode == "test_video" or mode == "map":
        testing(path_file_config, folder_contains_YOLO, mode)
    else:
        print("Enter wrong mode. Please check the format again!")



def makeProject(path_file_config):
    #####################################################################################################
    #                                       Clone darknet and make                                      #
    #####################################################################################################
    folder_contains_YOLO = ""
    make_yet = ""

    with open(path_file_config,"r") as file_config:
        config = file_config.readlines()
    for i, line in enumerate(config):
        line = line.strip()
        if "#" in line:
            continue
        if "folder_contains_YOLO" in line:
            folder_contains_YOLO = line.split("=")[1].strip()
            if folder_contains_YOLO == "":
                os.system("git clone https://github.com/AlexeyAB/darknet.git")
                folder_contains_YOLO = os.path.join(os.path.dirname(path_file_config), "darknet")
                line = " ".join([line, folder_contains_YOLO])
                config[i] = line + "\n"
        if "make_yet" in line:
            make_yet = line.split("=")[1].strip()
            if ((int(make_yet) != 0 and int(make_yet) != 1) or int(make_yet) == 0):
                make_yet = 0
                line = " ".join([line.split("=")[0].strip(),"= 1"])
                config[i] = line + "\n"
            break
    
    with open(path_file_config,"w") as file_config:
        for line in config:
            file_config.write(line)

    
    if int(make_yet) == 0:
        os.chdir(folder_contains_YOLO)
        f = open("Makefile","r+")
        while True:
            line = f.readline()
            pointer = f.tell()
            if "#" in line:
                break
            elif ("GPU=" in line) or ("CUDNN=" in line) or ("CUDNN_HALF=" in line) or ("OPENCV=" in line) or ("AVX=" in line) or ("OPENMP=" in line) or ("LIBSO=" in line):
                f.seek(pointer-2, os.SEEK_SET)
                f.write("1\n")
                f.seek(pointer)

        f.close()

        os.system("make -j8")
        os.chdir(os.path.dirname(path_file_config))

    return folder_contains_YOLO
    


def main():
    #####################################################################################################
    #                                           Handle project                                          #
    #####################################################################################################
    
    path_file_config = os.path.abspath("config.txt")
    folder_contains_YOLO = ""
    if len(sys.argv) == 1:
        folder_contains_YOLO = makeProject(path_file_config)
        print("Clone and make project done")
    elif len(sys.argv) == 2:
        folder_contains_YOLO = makeProject(path_file_config)
        runMode(sys.argv[1], path_file_config, folder_contains_YOLO)
        
    elif len(sys.argv) == 3:
        if os.path.isfile(sys.argv[2]) == True:
            path_file_config = os.path.abspath(sys.argv[2])
            folder_contains_YOLO = makeProject(path_file_config)
            runMode(sys.argv[1], path_file_config,folder_contains_YOLO)
        else:
            print("Enter wrong path. Please check the path of file again!")
    else:
        print("Enter wrong format. Please check the format again!")



if __name__ == "__main__":
    main()