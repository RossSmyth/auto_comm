# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:30:00 2019

@author: Ross

This is a library for validating and option options from ini files, and also
 validating independent of programs.
"""
import configparser
import os
import fileinput


def _uart_options_validator(ini_options: configparser.SectionProxy) -> dict:
    """validates the data in the ini file and then packs it into a dict
    
    I know using assertions is "bad" but it's nice.
    """
    if not isinstance(ini_options, configparser.SectionProxy):
        raise TypeError('Needs to be configparser.SectionProxy')
    
    options = {}
    
    port = ini_options.get('port')
    # Make sure this is a USB port or NoneType
    if port is not None:
        if 'COM' in port or '/dev/ttyUSB' in port:
            options['port'] = port
        else:
            raise ValueError('Needs to be either "COM*" or "/dev/ttyUSB*"')
    
    # As long as this is an int it is probably fine
    options['baudrate'] = int(ini_options.get('baudrate', 9600))
    
    bytesize = ini_options.get('bytesize', 8)
    assert bytesize in [5, 6, 7, 8]
    options['bytesize'] = bytesize
    
    parity = ini_options.get('parity', 'None').title()
    assert parity in ['None', 'Even', 'Odd', 'Mark', 'Space']
    options['parity'] = parity[0]
    
    stopbits = int(ini_options.get('stopbits', 1))
    assert stopbits in [1, 1.5, 2]
    options['stopbits'] = stopbits
    
    timeout = ini_options.get('timeout', None)
    assert 0 < timeout or timeout is None
    options['timeout'] = timeout if not None else float(timeout)
    
    options['xonxoff'] = bool(ini_options.get('xonxoff ', False))
    
    options['rtscts'] = bool(ini_options.get('rtscts', False))
    
    options['dsrdtr'] = bool(ini_options.get('dsrdtr', False))
    
    write_timeout = ini_options.get('write_timeout', None)
    assert 0 < write_timeout or write_timeout is None
    options['write_timeout'] = write_timeout if not None else float(write_timeout)
    
    inter_byte_timeout = ini_options.get('inter_byte_timeout', None)
    assert 0 < inter_byte_timeout or inter_byte_timeout is None
    options['inter_byte_timeout'] = inter_byte_timeout if not None else float(inter_byte_timeout)
    
    exclusive = ini_options.get('exclusive', None)
    assert exclusive is None or os.name == 'posix'
    options['exclusive'] = exclusive
    
    return options
    
def get_uart_options(file: configparser.SectionProxy) -> dict:
    """Options to pass to pySerial
    
    This function takes in an ini file and outputs a uart option dict() for 
    packing into the pySerial serial.Serial object. It also validates the file.
    """
    return _uart_options_validator(file['UART'])

if __name__ == '__main__':
    
    ini_validators = {
                     "UART" : _uart_options_validator,
                     }
    
    for file in fileinput.input():
        config = configparser.ConfigParser().read(file)
        for protocol in ini_validators:
            if protocol in config.sections():
                ini_validators[protocol](config[protocol])
    print("These files are good")