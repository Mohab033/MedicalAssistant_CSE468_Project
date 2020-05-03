import pytesseract
from pytesseract import Output
#pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'
import cv2
import pandas 
import numpy 
import tkinter as tk


#this is a function that is used to draw a bounding box on the name of the medicine
def Bounding_box_drawing(img):
    #Extract Text as pandas dataframe containing text, bounding box and confidence level
    Txt_Df = pytesseract.image_to_data(img, output_type='data.frame')
    #reject low confidence words 
    Txt_Df = Txt_Df[(Txt_Df.conf >80)]
    #drop off Whitespaces 
    for ind in Txt_Df.index:
        dr = Txt_Df['text'][ind].replace(" ","")
        if(dr == ""):
            Txt_Df = Txt_Df.drop([ind])


    #drop off NaN
    Txt_Df.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)

    ## Post Processing 

    #Count bounding boxes
    n_boxes = len(Txt_Df['level'])

    #Create a copy of the image to use as a mask
    overlay = img.copy()

    #Calculate the area of each bounding box 
    Txt_Df['area']=Txt_Df['width']*Txt_Df['height']

    #find bounding boxes with max area
    Cond=((Txt_Df['area']==Txt_Df['area'].max()))
    #print(Txt_Df)

    #Extract data of biggest bounding box (x,y,width,height)
    (x, y, w, h) = (int(Txt_Df[Cond]['left']), int(Txt_Df[Cond]['top']), int(Txt_Df[Cond]['width']), int(Txt_Df[Cond]['height']))
    nameofthedrug=Txt_Df['text'][Cond].to_string(index=False)
    #print(OCR_Text)
    #overlay a light shadow on the box 
    cv2.rectangle(overlay, (x, y), (x + w, y + h), (120, 120, 0), -1)

    #overlay edges 
    cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 240, 0),6)

    # Transparency factor.
    alpha = 0.6  

    #overlay transparent Rect. as a mask on the original img
    img_new = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0) 

    ##Final Resize to display image

    #resize images to a final size 
    dim = (800, 600) 
    res_img=cv2.resize(img_new,dim, interpolation = cv2.INTER_AREA)

    return (res_img,nameofthedrug)




def compare_the_drugs(x1,x2):
    #match the OCR reading to have same Case
    targettake = x1.capitalize()
    alreadytaken = x2.capitalize()

    #print(type(targettake),alreadytaken)
    #Connect medicines to the corresponding active ingredient 
    paracetamol = ['Novaldol','Congestal']
    Ibuprofen = ['Flamotal','Profenazone']
    Fluvoxamine = ['Statomain','Faverin']
    diclofenac =['Declophen','Voltaren','Cataflam']
    Escitalopram = ['Cipralex','Escitalopram']
    Memantine = ['Ebixa','Esmirtal','Doneptin']
    Penicillin = ['Amoclawin','Phenoxymethylpenicillin']
    Levothyroxine = ['Euthyrox','Eltroxin']
    Sodium_Carboxymethyl_Cellulose = ['Lacritears','Moistine','Carmos']
    Nitrofurantoin = ['Macrofuran','Furadantin']
    Sysadoa = ['Piascledine','Chondroitin']
    #Logic For deciding whether the patient can take the 2 drugs together
    if  (alreadytaken in paracetamol) and (targettake in Ibuprofen):
        print('you can not take {} with {}'.format(alreadytaken,targettake))
    elif (alreadytaken in Fluvoxamine) and (targettake in Ibuprofen):
        print('you cannot take {} with {} , you must consult a doctor for this case'.format(alreadytaken,targettake))
    elif  (alreadytaken in Penicillin) and (targettake in Fluvoxamine):
        print('you cannot take {} with {} , you must consult a doctor for this case'.format(alreadytaken,targettake))
    elif  (alreadytaken in Penicillin) and (targettake in Escitalopram):
        print('you cannot take {} with {} , you must consult a doctor for this case'.format(alreadytaken,targettake))
    elif  (alreadytaken in diclofenac) and (targettake in Escitalopram):
        print('you cannot take {} with {} , you must consult a doctor for this case'.format(alreadytaken,targettake))
    elif  (alreadytaken in Ibuprofen) and (targettake in Escitalopram):
        print('you cannot take {} with {} , you must consult a doctor for this case'.format(alreadytaken,targettake))
    elif  (alreadytaken in Levothyroxine) and (targettake in Penicillin):
        print('you cannot take {} with {} , you must consult a doctor for this case'.format(alreadytaken,targettake))
    else:
        print('No Drug interaction detected between {} and {}'.format(targettake,alreadytaken))
    #Extra Notes for Each Drug
    if ( targettake in paracetamol):
        print('{} is anti inflammatory medicine \n'.format(targettake))
        print('the dosage is 2 times per day')
        print('Do not take these if you are drinking alcohol')
        print('if not available there are some alternatives for {} like'.format(targettake))
        for i in range(len(paracetamol)):
            if (paracetamol[i] == targettake):
                continue
            print('Such as {}'.format(paracetamol[i]))
    
    elif(targettake in Fluvoxamine): 
        print('{} is anti depression, you must consult your doctor for dosage'.format(targettake))
        print('if not available there are some alternatives for {}'.format(targettake))
        for i in range(len(Fluvoxamine)):
            if (Fluvoxamine[i] == targettake):
                continue
            print('Such as {}'.format(Fluvoxamine[i]))
        
    elif(targettake in Memantine): 
        print('{} is used to treat patients with moderate to severe Alzheimer’s disease, it should be given once a day at the same time every day'.format(targettake))
        print('if not available there are some alternatives for {}'.format(targettake))
        for i in range(len(Memantine)):
            if (Memantine[i] == targettake):
                continue
            print('Such as {}'.format(Memantine[i]))     
        
    elif(targettake in Escitalopram): 
        print('{} is an anti depressant, you must consult your doctor for dosage'.format(targettake))
        print('if not available there are some alternatives for {}'.format(targettake))
        for i in range(len(Escitalopram)):
            if (Escitalopram[i] == targettake):
                continue
            print('Such as {}'.format(Escitalopram[i]))

    elif(targettake in Levothyroxine): 
        print('The timing of meals relative to your {} dose can affect absorption of the medication. Therefore, levothyroxine should be taken on a consistent schedule with regard to time of day and relation to meals to avoid large fluctuations in blood levels'.format(targettake))
        print('if not available there are some alternatives for {}'.format(targettake))
        for i in range(len(Levothyroxine)):
            if (Levothyroxine[i] == targettake):
                continue
            print('Such as {}'.format(Levothyroxine[i]))
     
    elif(targettake in Ibuprofen): 
        print('{} is used to reduce fever and treat pain or inflammation,Ibuprofen can increase your risk of fatal heart attack or stroke, especially if you use it long term or take high doses, or if you have heart disease. Do not use this medicine just before or after heart bypass surgery'.format(targettake))
        print('if not available there are some alternatives for {}'.format(targettake))
        for i in range(len(Ibuprofen)):
            if (Ibuprofen[i] == targettake):
                continue
            print('Such as {}'.format(Ibuprofen[i]))
    
    elif(targettake in diclofenac): 
        print('{} works by reducing substances in the body that cause pain and inflammation, You should not use diclofenac if you have a history of allergic reaction to aspirin'.format(targettake))
        print('if not available there are some alternatives for {}'.format(targettake))
        for i in range(len(diclofenac)):
            if (diclofenac[i] == targettake):
                continue
            print('Such as {}'.format(diclofenac[i]))

    elif(targettake in Nitrofurantoin): 
        print('{} is used to treat urinary tract infections, Do not take this medicine if you are in the last 2 to 4 weeks of pregnancy.'.format(targettake))
        print('if not available there are some alternatives for {}'.format(targettake))
        for i in range(len(Nitrofurantoin)):
            if (Nitrofurantoin[i] == targettake):
                continue
            print(Nitrofurantoin[i])

    elif(targettake in Penicillin): 
        print('{} contains pencillin'.format(targettake))
        print('if not available there are some alternatives for {}'.format(targettake))
        for i in range(len(Penicillin)):
            if (Penicillin[i] == targettake):
                continue
            print('Such as {}'.format(Penicillin[i]))

    elif(targettake in Sodium_Carboxymethyl_Cellulose): 
        print('it`s used for the temporary relief of burning , irritation and discomfort due to dryness of the eye or expouse to wind or sun . May be used as a protectant against future irritation ')
        print('if not available there are some alternatives for {}'.format(targettake))
        for i in range(0,len(Sodium_Carboxymethyl_Cellulose)):
            if (Sodium_Carboxymethyl_Cellulose[i] == targettake):
                continue
            print('Such as {}'.format(Sodium_Carboxymethyl_Cellulose[i]))
            
    elif(targettake in Sysadoa): 
        print('PIASCLEDINE capsule is indicated for the symptomatic slow-acting treatment of hip and knee osteoarthritis.')
        print('if not available there are some alternatives for {}'.format(targettake))
        for i in range(len(Sysadoa)):
            if (Sysadoa[i] == targettake):
                continue
            print('Such as {}'.format(Sysadoa[i]))




####user changes here 
def my_program(a1,a2):
## change the names of the images you want 
    #Load image
    img = cv2.imread(a1)
    #Convert 2 grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Gaussian filter to remove the noise
    img = cv2.GaussianBlur(img, (5, 5), 0)

    cv2.imshow('img', img)
    #tk.Label(master, image=img)

    #canvas.create_image(20, 20,  image=img) 
    #cv2.waitKey(0)
    #Load image
    img2 = cv2.imread(a2)
    #Convert 2 grayscale
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    #Gaussian filter to remove the noise
    img2 = cv2.GaussianBlur(img2, (5, 5), 0)

    cv2.imshow('img2', img2)
    #canvas.create_image(20, 20, image=img2)
    #tk.Label(master, image=img2)
    cv2.waitKey(0)

    #cv2.waitKey(0)

    ##call the function that used to draw a bounding box

    (img3,x1)=Bounding_box_drawing(img)
    (img4,x2)=Bounding_box_drawing(img2)
    cv2.imshow('img3', img3)
    cv2.imshow('img4', img4)
    #print(x1.strip())
    #print(type(x1))
    print('You inserted {} & {}'.format(x1,x2))
    compare_the_drugs(x1.strip(),x2.strip())
    #tk.Label(master, image=ImageTk.PhotoImage(img3),anchor='se')

def show_entry_fields():
    print("First file: %s\nSecond file: %s" %(img.get(), img2.get()))
    my_program(img.get(),img2.get())
    img.delete(0, tk.END)
    img2.delete(0, tk.END)

master = tk.Tk() 
#canvas = tk.Canvas(master)
#canvas.pack()
tk.Label(master, text='Image1_path').grid(row=0) 
tk.Label(master, text='Image2_path').grid(row=1) 
img = tk.Entry(master) 
img2 = tk.Entry(master) 
tk.Button(master, text='Enter', command=show_entry_fields).grid(row=3, column=1, sticky=tk.W,pady=4)
img.grid(row=0, column=1) 
img2.grid(row=1, column=1) 
tk.mainloop()