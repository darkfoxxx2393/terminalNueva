from re import S
import cmd2 
from cmd2 import (
Bg,
Fg,
style,
)
from cmd2 import Cmd2ArgumentParser, with_argparser
from os.path import isdir, isfile
from pathlib import Path
import subprocess
import sys
import readline
import getpass
import os
import socket
import time
import shutil
import hashlib
from cmd2.table_creator import EMPTY
import psutil
from ftplib import FTP
from time import *
import argparse

readline.parse_and_bind("tab: complete")


class calceshell(cmd2.Cmd):

    def __init__(self):
        super().__init__(multiline_commands=['orate'])
        #SE PUEDE METER ESTOS DOS PARA TENER ARCHIVO DE HISTORIA Y SCRIPT PARA CONFIGURAR TIPO calceshell.rc
        #persistent_history_file='cmd2_history.dat',startup_script='scripts/startup.txt'
        self.default_to_shell = True
        self.intro = style('calceShell 2021 para SO1!', fg=Fg.RED, bg=Bg.BLACK, bold=True) + ' 😀📁📂🗃🗎🖻🖹🖿🗀🗁'
        self.prompt=prompt = getpass.getuser()+"@"+socket.gethostname()+":"+str(os.getcwd())+"$ \n>"

    def postcmd(self, stop: bool, line: str) -> bool: #FUNCION QUE SE EJECUTA LUEGO DE CADA COMANDO AQUI SE PUEDE HOOCKEAR EL CAMBIO DE PROMPT!!!!!
        #wd=getpass.getuser()+"@"+socket.gethostname()+":"+str(os.getcwd())+"$ \n"
        #self.prompt = style('{!r} $ '.format(wd), fg = Fg.DARK_GRAY, bg = Bg.BLUE,bold=True) #para dejarle chururu
        self.prompt = getpass.getuser()+"@"+socket.gethostname()+":"+str(os.getcwd())+"$ \n>"       
        return stop


    irParser = Cmd2ArgumentParser()
    irParser.add_argument('dst', nargs=(0,1), default=" ", help='Directorio al cual se quiere ir, para subir un ..')
    @with_argparser(irParser)
    def do_ir(self,dest): 

        #si se pone sin argumentos
        if dest.dst == " ":            
            os.chdir(os.path.expanduser("~")) #ir al directorio $HOME del usuario
        else:
            
            dest.dst=os.path.abspath(os.path.expanduser(dest.dst))
            
            if not isdir(dest.dst):
                self.perror("No es un directorio valido")
                
            elif not os.access(dest.dst,  os.R_OK):
                self.perror("No se tiene acceso de lectura al directorio")
                
            else:
                try:
                    os.chdir(dest.dst)
                except Exception as ex:
                    self.perror(ex)
            
        return

    # Enable tab completion for cd command
    def complete_ir(self, text, line, begidx, endidx):
        return self.path_complete(text, line, begidx, endidx)



    def do_limpiar(self, line):
        #print("\033[H\033[J", end="")
        self.poutput("\033[H\033[J", end="")

    #este hay que hacer el override de forma correcta! sino no funca ya que el flag de default_to_shell solo va a la shell si no se encuentra entre los comandos
    #y pasa por este antes de salir

    # def default(self, line):
    #     self.poutput("Error comando fail")
    #     self.poutput(line)
    #     #
    

    def do_salir(self, line):        
        self.poutput("Bye")
        return True

    def do_super(self, line):
        #es una herramienta que usaremos mas tarde V:
        #args = ['sudo', sys.executable] + sys.argv + [os.environ]
        file_path = os.path.dirname(__file__)
        self.poutput(sys.executable)
        proc = subprocess.call(['sudo',sys.executable,file_path+"/calceshell.py"])
        return 0

    do_cd=do_ir  #cd es interno de la shell y un proceso no puede cambiar el cwd de otro proceso

    listarParser = Cmd2ArgumentParser()
    listarParser.add_argument('dir', nargs=(0,1),default=" ", help='ruta al directorio')

    @with_argparser(listarParser)
    def do_listar(self, opt):
        #fix por si se meta la virgula :V
        opt.dir=os.path.expanduser(opt.dir) 
        #print(os.path.abspath(opt.dir))
        if opt.dir==" ":            
            archivos = os.listdir(os.getcwd())
            for f in archivos:
                if isdir(f):
                    self.stdout.write('📂 '+f)
                else:
                    self.stdout.write('🗃 '+f)
                self.stdout.write("    ")
        else:
            if isfile(opt.dir):
                self.perror("La ruta especificada no es un directorio válido o el directorio no existe")
                return
        #lista los archivos y directorios correspondientes a la ruta especificada           
            archivos = os.listdir(os.path.abspath(opt.dir))
            for f in archivos:
                #print(os.path.abspath(opt.dir))                
                if isdir((os.path.abspath(opt.dir))+"/"+f): 
                    self.stdout.write('📂 '+f)
                else:
                    self.stdout.write('🗃 '+f)
                self.stdout.write("    ")  
                  
        self.stdout.write("\n")    
        return

    def complete_listar(self, text, line, begidx, endidx):
        return self.path_complete(text, line, begidx, endidx)

    def do_tiempoEncendido(self, line):
        self.poutput(strftime("%H:%M:%S", gmtime()))    
        self.poutput(strftime("%Hh%Mm", gmtime(round(time()-psutil.boot_time()))))
        #self.poutput("Carga promedio:",[str(x) for x in os.getloadavg()])  #FALTA FIXEAR ESTE NO LE GUSTA AL POUTPUT
        #    /var/run/utmp
        return



    copiarparser = Cmd2ArgumentParser()
    #copiarparser.add_argument('files', nargs=2, help='copiar $src $dst, copiar el archivo/directorio src al directorio dst')
    copiarparser.add_argument('src',nargs=1,type=str,help='El archivo o directorio fuente')
    copiarparser.add_argument('dst',nargs=1,type=str,help='El archivo o directorio destino')
    @with_argparser(copiarparser)
    def do_copiar(self, opt):
        
        #if isdir(str(opt.src)):
        opt.src=os.path.abspath(os.path.expanduser(opt.src[0]))
        #if isdir(str(opt.dst)):
        opt.dst=os.path.abspath(os.path.expanduser(opt.dst[0]))
        #opt.dst=os.path.abspath(os.path.expanduser(opt.dst))
        print(opt.src)
        print(opt.dst)

        if not os.path.exists(opt.src):
            self.perror("ALV no se puede copiar algo que no existe :V")
        
        
        # origin = os.path.join(os.getcwd(),command[1])
        # destiny = os.path.join(os.getcwd(),command[2])
        #try:
        if isdir(opt.src):
            shutil.copytree(opt.src,opt.dst,dirs_exist_ok=True)
            self.poutput(f"Se copio el directorio {os.path.basename(opt.src)} a {opt.dst}")
        else:        
            shutil.copy(opt.src,opt.dst)
            self.poutput(f"Se copio el archivo {os.path.basename(opt.src)} a {opt.dst}")
        #except:
            #self.perror("No se pudo realizar la copia")
        return
    def complete_copiar(self, text, line, begidx, endidx):
        return self.path_complete(text, line, begidx, endidx)
if __name__ == '__main__':
    shell=calceshell()
    sys.exit(shell.cmdloop())
    