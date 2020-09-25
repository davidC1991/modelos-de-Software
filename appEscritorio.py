# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 12:26:46 2020

@author: Admin
"""

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication,QWidget,QLabel
from PyQt5.QtGui import QIcon, QPixmap
import speech_recognition as sr
from textblob import TextBlob
from googletrans import Translator
import mariadb
import time
import matplotlib.pyplot as plot
from PIL import Image
from PyQt5.QtCore import QThread

etiquetasSentimiento=['Positivos','Negativos','Neutro']
etiquetasSentimiento1=['Positivos','Negativos','Neutro']
valoresProductosA=[]
valoresProductosB=[]
valoresProductosC=[]


class analizar(QThread):
     def __init__(self,producto):
        super().__init__()
        self.producto=producto
     def iniciar(self):
        r=sr.Recognizer()
        with sr.Microphone() as source:
            
           
            r.adjust_for_ambient_noise(source,duration=2)
            print('Ruido Ambiente')
            print('Empiece a hablar sobre el',self.producto)
            audio=r.listen(source,phrase_time_limit=(5))
            print('tengo el audio')
    
            try:
                text=r.recognize_google(audio,language="es-CO")
                print('traducire')
                print('tu dijiste: \n '+text)
                self.labelResultado.setText('Tu dijiste: '+text)
            except Exception as e:
                print('Lo siento no se pudo traducir el texto')
                print(str(e))
            
        translation=Translator(service_urls=["translate.google.com"])
        textEnglish= translation.translate(text,dest="en")
        print(textEnglish.text)
        text=textEnglish.text

        edu=TextBlob(text)  
        valor=edu.sentiment.polarity

        if valor<0:
            print('Sentimiento negativo')
            sentimiento='Sentimiento negativo'
           # self.labelSentimiento.setText('Sentimiento negativo')
        elif valor==0:
            print('Sentimiento Neutral')
            sentimiento='Sentimiento Neutral'
           # self.labelSentimiento.setText('Sentimiento Neutral')
        elif valor>0 and valor<=1:
            print('Sentimiento Positivo')
            sentimiento='Sentimiento Positivo'
            #self.labelSentimiento.setText('Sentimiento Positivo')
    
        print(valor)
        time.sleep(1)
       
        self.insertarDatos(self.producto,valor,sentimiento,text)
        time.sleep(1)
        self.mostrarDatos()
        
        #--------------------------
        plot.clf()
        if(self.producto=='productoA'):
            
            print('grafica A')
            plot.bar(etiquetasSentimiento,valoresProductosA)
            plot.title('Estadisticas Producto A')
            plot.plot(30)
            plot.savefig("productoA.jpg")
            img = Image.open("productoA.jpg")
            new_img = img.resize((256,256))
            new_img.save('productoA.png','png')
        #--------------------------
        
         #--------------------------
        if(self.producto=='productoB'):
            print('grafica B')
           
            plot.bar(etiquetasSentimiento1,valoresProductosB,)
            plot.title('Estadisticas Producto B')
            plot.plot(30)
            plot.savefig("productoB.jpg")
            img1 = Image.open("productoB.jpg")
            new_img1 = img1.resize((256,256))
            new_img1.save('productoB.png','png')
        #--------------------------
        
         #--------------------------
        if(self.producto=='productoC'):
            print('grafica C')
            plot.bar(etiquetasSentimiento,valoresProductosC)
            plot.title('Estadisticas Producto C')
            plot.plot(30)
            plot.savefig("productoC.jpg")
            img2 = Image.open("productoC.jpg")
            new_img2 = img2.resize((256,256))
            new_img2.save('productoC.png','png')
        #--------------------------
        #plot.show()
        
        #imagen = QWidget.QPixmap('productoA.jpg')
        return sentimiento
        
        
     
     def insertarDatos(self,producto,valor,sentimiento,mensaje):
        try: 
            conn=mariadb.connect(
                host="localhost",
                user="root",
                password="",
                database="sentimientosdb"
            )
        except mariadb.Error as e:
            print('Error al conectarse a la base de datos',e)
        
        cur=conn.cursor()
        print('entro aca...')
        cur.execute("INSERT INTO `datos`(`producto`, `valor`, `sentimiento`,`mensaje`) VALUES (%s,%s,%s,%s)",        (producto,valor,sentimiento,mensaje))
        conn.commit()
        cur.close()
        conn.close()   
     
     def consultaDatos(self,query):
        try:
            conn=mariadb.connect(
                host="localhost",
                user="root",
                password="",
                database="sentimientosdb"
            )
        except mariadb.Error as e:
            print('Error al conectarse a la base de datos',e)
        
        cur=conn.cursor()
        cur.execute(query)
        #cur.close()
        #conn.close()
        return cur
    
     def mostrarDatos(self):
        cur=self.consultaDatos("SELECT `producto`,`valor`,`sentimiento`,`mensaje` FROM `datos`")
        #print(cur)
        cont_PA_Positivo=0
        cont_PA_Negativo=0
        cont_PA_Neutro=0
        
        cont_PB_Positivo=0
        cont_PB_Negativo=0
        cont_PB_Neutro=0
        
        cont_PC_Positivo=0
        cont_PC_Negativo=0
        cont_PC_Neutro=0
       
        valoresProductosA.clear()  
        valoresProductosB.clear()  
        valoresProductosC.clear() 
        
        for(producto,valor,sentimiento,mensaje) in cur:
           
          print(producto,valor,sentimiento,mensaje)
          if valor<0:
            if(producto=='productoA'):
              cont_PA_Negativo=cont_PA_Negativo+1
            if(producto=='productoB'):
              cont_PB_Negativo=cont_PB_Negativo+1
            if(producto=='productoC'):
              cont_PC_Negativo=cont_PC_Negativo+1  
          elif valor==0:
             if(producto=='productoA'):
              cont_PA_Neutro=cont_PA_Neutro+1
             if(producto=='productoB'):
              cont_PB_Neutro=cont_PB_Neutro+1
             if(producto=='productoB'):
              cont_PC_Neutro=cont_PC_Neutro+1 
            # self.labelSentimiento.setText('Sentimiento Neutral')
          elif valor>0 and valor<=1:
             if(producto=='productoA'):
              cont_PA_Positivo=cont_PA_Positivo+1
             if(producto=='productoB'):
              cont_PB_Positivo=cont_PB_Positivo+1
             if(producto=='productoC'):
              cont_PC_Positivo=cont_PC_Positivo+1 
             #   self.labelSentimiento.setText('Sentimiento Positivo')
          
          #listaProductos.append(producto)   
        valoresProductosA.append(cont_PA_Positivo) 
        valoresProductosA.append(cont_PA_Negativo)
        valoresProductosA.append(cont_PA_Neutro)
        
        valoresProductosB.append(cont_PB_Positivo) 
        valoresProductosB.append(cont_PB_Negativo)
        valoresProductosB.append(cont_PB_Neutro)
        
        valoresProductosC.append(cont_PC_Positivo) 
        valoresProductosC.append(cont_PC_Negativo)
        valoresProductosC.append(cont_PC_Neutro)
        
        print(valoresProductosA)
        print(valoresProductosB)
        print(valoresProductosC)
        
       
        
    
class gui(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("interface.ui",self)
        self.botonProductoA.clicked.connect(lambda: self.grabar("productoA"))
        self.botonProductoB.clicked.connect(lambda: self.grabar("productoB"))
        self.botonProductoC.clicked.connect(lambda: self.grabar("productoC"))
        
        
    def grabar(self,_str):
        
        
        a=analizar(_str)
        sentimiento=a.iniciar()
        self.labelHablar.setText(sentimiento+' para el '+_str)
        del a
        self.labelGraficoC.setText('hola')
        #--------------------------
        if(_str=='productoA'):
            pixmap = QPixmap('productoA.png')
            self.labelGraficoC.setPixmap(pixmap)
        #--------------------------   
         #--------------------------
        if(_str=='productoB'):
            pixmap1 = QPixmap('productoB.png')
            self.labelGraficoC.setPixmap(pixmap1)
        #--------------------------    
         #--------------------------
        if(_str=='productoC'):
            pixmap2 = QPixmap('productoC.png')
            self.labelGraficoC.setPixmap(pixmap2)
        #--------------------------    
             
        
        
        #for(producto,valor) in datos:
        #    listaProductos.append(producto)
        #    valores.append(valor)
        
        #print(datos)
        #print(listaProductos)
        #print(valores)
        
        
    
    
        
        
    
           
           
              
            
        
if __name__== '__main__':
    app= QApplication(sys.argv)
    GUI=gui()
    GUI.show()
    sys.exit(app.exec_())        