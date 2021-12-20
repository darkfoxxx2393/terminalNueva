import cmd2 
from cmd2 import (
Bg,
Fg,
style,
)
from os.path import isdir, isfile
from pathlib import Path
from posix import listdir
import subprocess
import sys
import readline
import getpass
import os
import socket
import time
import shutil
import hashlib
import psutil
from ftplib import FTP
from time import *

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

    def do_ir(self,dest):    
        print(dest)
        try:
            print(os.path.abspath(dest))
            os.chdir(os.path.abspath(dest))
            
        except:
            print("ERROR: Not a valid path")

    # Enable tab completion for cd command
    def complete_ir(self, text, line, begidx, endidx):
        return self.path_complete(text, line, begidx, endidx, path_filter=os.path.isdir)



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

    def do_listar(self, dest): 
        cami=dest       
        if dest == "":
            dest = os.listdir(os.path.join(os.getcwd()))
            for f in dest:
                if isdir(os.getcwd()+f):
                    self.stdout.write('📂 '+f)
                else:
                    self.stdout.write('🗃 '+f)
                self.stdout.write("    ")
        else:
            #self.poutput(dest) 
            #argc = os.listdir(os.path.join(os.getcwd(),command[1]))
            dest = os.listdir(os.path.abspath(dest))
            for f in dest:
                #print(str(os.path.abspath(cami))+f)
                if isdir(str(os.path.abspath(cami))+f): 
                    self.stdout.write('📂 '+f)
                else:
                    self.stdout.write('🗃 '+f)
                self.stdout.write("    ")    
        self.stdout.write("\n")    
        return 0

    def complete_listar(self, text, line, begidx, endidx):
        return self.path_complete(text, line, begidx, endidx, path_filter=os.path.isdir)

    def do_tiempoEncendido(self, line):
        self.poutput(strftime("%H:%M:%S", gmtime()))    
        self.poutput(strftime("%Hh%Mm", gmtime(round(time()-psutil.boot_time()))))
        #self.poutput("Carga promedio:",[str(x) for x in os.getloadavg()])  #FALTA FIXEAR ESTE NO LE GUSTA AL POUTPUT
        #    /var/run/utmp
        return 0

    
if __name__ == '__main__':
    shell=calceshell()
    sys.exit(shell.cmdloop())
    