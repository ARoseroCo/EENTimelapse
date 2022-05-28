from tkinter import *
from tkinter import ttk as ttk
from tkinter import messagebox as MessageBox
from EagleEye import *

een = EagleEye()  

root = Tk()

nombreUsuario = StringVar()
contraUsuario = StringVar()
cameraESN = StringVar()
startDate = StringVar()
endDate = StringVar()
videoLength = StringVar()

usuarios = []

mainFrame = Frame(root)
    
def createGUI():

    # ventana principal
    #root = Tk()
    root.title("Login")

    # mainFrame

    mainFrame.pack()
    mainFrame.config(width=480,height=320)#,bg="lightblue")

    # textos y titulos
    titulo = Label(mainFrame,text="EEN API Login",font=("Arial",24))
    titulo.grid(column=0,row=0,padx=10,pady=10,columnspan=2)

    nombreLabel = Label(mainFrame,text="User Name: ")
    nombreLabel.grid(column=0,row=1)
    passLabel = Label(mainFrame,text="Pasword: ")
    passLabel.grid(column=0,row=2)

    # entradas de texto
    # nombreUsuario = StringVar()
    nombreUsuario.set("xxxxx@xxxx.com") #Nombre de Usuairo
    nombreEntry = Entry(mainFrame,textvariable=nombreUsuario)
    nombreEntry.grid(column=1,row=1)
    

    # contraUsuario = StringVar()
    contraUsuario.set("XXXXXX") #Contraeña
    contraEntry = Entry(mainFrame,textvariable=contraUsuario,show="*")
    contraEntry.grid(column=1,row=2)

    # botones
    iniciarSesionButton = ttk.Button(mainFrame,text="Login",command=iniciarSesion)
    iniciarSesionButton.grid(column=1,row=3,ipadx=5,ipady=5,padx=10,pady=10)
    cerrarSesionButton = ttk.Button(mainFrame,text="Cerrar Sesion",command=cerrarSesion)
    #registrarButton = ttk.Button(mainFrame,text="Register",command=registrarUsuario)
    #registrarButton.grid(column=0,row=3,ipadx=5,ipady=5,padx=10,pady=10)
    
          
        
    root.mainloop()

def createGUI2():
    
 

    
    startDateLabel = Label(mainFrame,text="Start Time (UTC): ")
    startDateLabel.grid(column=0,row=4)
    endDateLabel = Label(mainFrame,text="End Time (UTC): ")
    endDateLabel.grid(column=0,row=5)
    cameraESNLabel = Label(mainFrame,text="Camera ESN:")
    cameraESNLabel.grid(column=0,row=6)
    videoLengthLabel = Label(mainFrame,text="Video Length (Minutes): ")
    videoLengthLabel.grid(column=0,row=7)
    
    startDate.set("20220526225001.000")
    startDateEntry = Entry(mainFrame,textvariable=startDate)
    startDateEntry.grid(column=1,row=4)
    
    endDate.set("20220526235901.000")
    endDateEntry = Entry(mainFrame,textvariable=endDate)
    endDateEntry.grid(column=1,row=5)
    
    cameraESN.set("") #Camera ESN
    cameraESNEntry = Entry(mainFrame,textvariable=cameraESN)
    cameraESNEntry.grid(column=1,row=6)
    
    videoLength.set("1")
    videoLengthEntry = Entry(mainFrame,textvariable=videoLength)
    videoLengthEntry.grid(column=1,row=7)
    
    createTimeFrameButton = ttk.Button(mainFrame,text="Create TimeFrame",command=createTimeFrame)
    createTimeFrameButton.grid(column=1,row=8,ipadx=5,ipady=5,padx=10,pady=10)
    
def createTimeFrame():    
    this_camera = een.find_by_esn(cameraESN.get()) 
    this_camera.get_preview_list(instance=een, start_timestamp=startDate.get(), end_timestamp=endDate.get(), asset_class="pre") 

    # Figure out how to get to the desired video length assuming input at 10 FPS.
    # Get the total number of images devides by the desired video length in seconds.
    # The result is how man images we need to skip in order to represent the time period.
    number_of_previews = len(this_camera.previews)
    VIDEO_LENGTH = int(videoLength.get())*600
    CAMERA_ESN = int(cameraESN.get())
    
    steps = number_of_previews / VIDEO_LENGTH
    
    #steps = number_of_previews / VIDEO_LENGTH
    import math
    steps = math.ceil(steps)

    #Quedamos por aca , dejar la cámara grabando para terminar y hacer pruebas
    print( f"Total images: {number_of_previews}" )
    print( f"Length of video: {VIDEO_LENGTH}" )
    print( f"Steps: {steps}" )
    
    # Only download the iamges that are going to be used.

    for pre in sorted(this_camera.previews)[0::steps]:
        img = this_camera.download_image(instance=een, timestamp=pre, asset_class="pre")
        if img:
            local_filename = f"tmp/{this_camera.camera_id}-{pre}.jpg"
            open(local_filename, 'wb').write(img)
        else: 
            print(f"{local_filename} failed")

    #pendiente poner barra de estado.
    
    frameSize = (500, 500)

    import subprocess

    subprocess.run(["ffmpeg", "-framerate", "10", "-pattern_type", "glob", "-i", f"tmp/{CAMERA_ESN}-*.jpg", "-y", "-r", "30", "-pix_fmt", "yuv420p", f"tmp/{CAMERA_ESN}.mp4"])
    
    MessageBox.showinfo(title="Sucess", message="Timeframe created successfully.")
    
    
def iniciarSesion():
    
    if een.login(username=nombreUsuario.get(), password=contraUsuario.get()):
        MessageBox.showinfo(title="Sucess", message="Login successful")
        createGUI2()
        
def cerrarSesion():
    pass


if __name__=="__main__":
    createGUI()
