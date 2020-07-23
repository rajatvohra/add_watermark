import cv2
import numpy as np
import os

def input_type():
    file_type=input("which type of file do you have, image or video \n")
    quantity_type=input("do you have single or multiple files, reply with single or multiple\n")
    return file_type,quantity_type
file_type,quantity_type=input_type()

def take_input():
    path_file=input("input path of video \n")
    path_logo=input("input path of the water mark \n")
    pos=input("position from (bottom left/bottom right/top left/top right)\n")
    return path_file,path_logo,pos
path_file,path_logo,pos=take_input()
#####"",r"C:\Users\rajat vohra\Desktop\logo_r.png","top left"
def logo_resize(path):
    logo=cv2.imread(path,cv2.IMREAD_COLOR)
    cv2.imshow("logo in real-time",logo)
    cv2.waitKey(1)
    x=int(input("enter new x dimensions "))
    y=int(input("enter new y dimensions "))
    logo=cv2.resize(logo,(y,x))
    cv2.imshow("logo in real-time",logo)
    cv2.waitKey(1)
    if(input("do you want  to make further changes\n")=="yes"):
        logo_resize(path)
    else:
        print("saving this as logo_resized.png")
        cv2.imwrite("logo_resized.png",logo)
        return logo       
if(input("do you want to make any changes to size of the logo? reply wiht a yes or no \n")=='yes'):
    logo=logo_resize(path_logo) 
else:
    logo=cv2.imread(path_logo,cv2.IMREAD_COLOR)

def convert(img,logo,x,y,pos):
    if(pos.lower()=="bottom right"):
        img[-x:,-y:,:]=logo[-x:,-y:,:]
    elif(pos.lower()=="top right"):
        img[:x,-y:,:]=logo[:x,-y:,:]
    elif(pos.lower()=="top left"):
        img[:x,:y,:]=logo[:x,:y,:]
    elif(pos.lower()=="bottom left"):
        img[-x:,:y,:]=logo[-x:,:y,:]
    return img



def logo_on_photos(folder,logo,pos):
    x,y,_=logo.shape
    count=0
    new_path=os.path.join(folder,"logo_photos\\")
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    for filename in os.listdir(folder):
        img=cv2.imread(os.path.join(folder,filename),cv2.IMREAD_COLOR)
        
        if img is not None:
            count=count+1
            img=convert(img,logo,x,y,pos)
            cv2.imwrite(os.path.join(new_path,filename),img)
    print("saved {} photos with logo in {}".format(count,new_path))
    return count

def logo_on_single_photo(path,logo,pos):
    x,y,_=logo.shape
    img=cv2.imread(path,cv2.IMREAD_COLOR)
    img=convert(img,logo,x,y,pos)
    path_split=os.path.split(path) 
    head_path=path_split[0]
    tail_path=path_split[1]
    cv2.imwrite(os.path.join(head_path,"logo_"+tail_path),img)
    print(os.path.join(head_path,"logo_"+tail_path))
    
    print("saved the file with the same name")

def logo_on_video(cap,logo,pos,path):
    frame_width = int(cap.get(3)) 
    frame_height = int(cap.get(4)) 
    size = (frame_width, frame_height) 
    fps = int(cap.get(5))
    result = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'MJPG'),  fps, size) 
    while cap.isOpened():
        ret, frame1 =cap.read()
        if not ret:
            print("finished with it \n")
            break
        x,y,_=logo.shape
        frame1=convert(frame1,logo,x,y,pos)
        result.write(frame1)
    cap.release()
    result.release()
    
def logo_on_multiple_videos(folder):
    new_path=os.path.join(folder,"logo_videos\\")
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    
    for filename in os.listdir(folder):
        path_for_file=os.path.join(new_path,filename)
        cap = cv2.VideoCapture(filename)
        logo_on_video(cap,logo,pos,path_for_file)


  
def main():
    if(file_type.lower()=='image' or file_type.lower()=='images'):
        if(quantity_type.lower()=='single'or quantity_type.lower()=='one' ):
            logo_on_single_photo(path_file,logo,pos)
        else:
            logo_on_photos(path_file,logo,pos)
    else:
        if(quantity_type.lower()=='single' or quantity_type.lower()=='one' ):
            cap=cv2.VideoCapture(path_file)
            path_split=os.path.split(path_file) 
            head_path=path_split[0]
            tail_path=path_split[1]
            path=os.path.join(head_path,"logo_"+tail_path)
            logo_on_video(cap,logo,pos,path)
        else:
            logo_on_multiple_videos(path_file)

main()