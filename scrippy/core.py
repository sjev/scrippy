#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core functions of the scrippy module

@author: Jev Kuznetsov
"""

import subprocess
import shlex
import sys
import string

         
def run(command, verbose=True, **kwargs):
    """ run shell command 
    Parameters
    --------------
    command : str or list
        command to run
        
    Returns
    ---------
    result of subprocess.run
    
    """
    
    if isinstance(command,str):
        command = shlex.split(command)
    
    res = subprocess.run(command, 
                         capture_output=True, 
                         text=True, 
                         **kwargs)
    
    if verbose:
        print(res.stdout)
        
    res.check_returncode()
    return res

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    
    prompts = {None:" [y/n] ",
               "yes":" [Y/n] ",
               "no":" [y/N] "}
    
   

    while True:
        sys.stdout.write(question + prompts[default])
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
 
class Template(string.Template):
    """ extension of the string.Template class """
    
    def __init__(self,args,**kwargs):
        super().__init__(args,**kwargs)
        
    def variables(self):
        """Extract the variable names from a string.Template.
        
        Returns a tuple of all variable names found in the template, in the order
        in which they occur.  If an invalid escape sequence occurs, the same
        error will be raised as if an attempt was made to expand the template.
        """
        result = []
        for match in self.pattern.finditer (self.template):
            if match.group ('invalid') is not None:
                # Raises ValueError
                self._invalid (match)
            if match.group ('escaped') is not None:
                continue
            # The "or None" should be moot.  It is there to ensure equivalent
            # treatment for an empty 'named' and an empty 'braced'.
            result.append (match.group ('named') or match.group ('braced') or None)
        return tuple (set(result))
    
    def fill(self, mapping={}):
        """ fill template with user values, ask user to input variables that are missing """

        dict_tpl = {}
        # read variables (if needed)
        for key in self.variables() :
            
            if key in mapping.keys():
                dict_tpl[key] = mapping[key]
            else:
                dict_tpl[key] = input(key + ':')
                
        return self.substitute(dict_tpl)