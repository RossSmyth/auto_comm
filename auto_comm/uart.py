# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 14:09:32 2019

@author: Ross
"""
import serial
from configparser import ConfigParser as ini_parse
from validation import get_uart_options

class UART(serial.Serial):
    """The class for using a USB to UART cable
    
    """
    def __init__(self, ini_file):
        
        ini = ini_parse()
        ini.read(ini_file)
        
        # This better be a UART ini file or else...
        assert 'UART' in ini.sections()
                
        super().__init__(**get_uart_options(ini))
        
    def read(self, size: int = 1, hexa: bool = True):
        """Override of the serial.Serial superclass's read() method
        Returns an array of the read data seperated by byte.
        
        Positional Arguments:
        ---------------------
        size = The number of bytes to read - int (default = 1)
        hexa = Whether to spit out hex or not, if not it will not touch it.
        """
        out = super.read(size)
        
        log(out) # TODO
        
        return hex(out) if hexa else hex