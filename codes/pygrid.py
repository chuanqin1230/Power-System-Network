# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 16:11:01 2018

@author: lusha
"""

import sys
import os

class gridlabObject:
    def __init__(self, filename="default.glm", workingDirectory="", solver_method = "NR", header_file = ""):
        self.objects = {}
        self.reference = {}         #This appears to be unused
        if workingDirectory == "":
            self.workingDir = os.getcwd()
        else:
            self.workingDir = workingDirectory
        self.outFileName = os.path.join(self.workingDir, filename)
        if header_file == "":
            header = ["clock {\n", "\ttimestamp \'2000-01-01 0:00:00';\n", "\ttimezone EST+5EDT;\n", "}\n\n",
        "module powerflow {\n", "\tsolver_method " + solver_method + ";\n", "}\n\n", 
        "module tape;\n", "#set profiler=1;\n", "#set relax_naming_rules=1;\n\n"]
        else: 
            headerFileName = os.path.join(self.workingDir, header_file)
            with open(headerFileName, 'r') as headerFile:
                header = headerFile.readlines()
        with open(self.outFileName, 'w') as outFile:
            outFile.write("".join(header) + "\n")
    
    def create_conductor(self, itemname, gmr, resistance):
        return_obj = {"object": "overhead_line_conductor", "name": itemname, "geometric_mean_radius": gmr, "resistance": resistance}
        return(return_obj)
    
    def create_underground_conductor(self, itemname, out_diam, cond_gmr, cond_diam, cond_resist, neutral_gmr, neutral_resist, neutral_diam, neutral_strands):
        return_obj = {"object": "underground_line_conductor", "name": itemname, "outer_diameter": out_diam, "conductor_gmr": cond_gmr, "conductor_diameter": cond_diam, "conductor_resistance": cond_resist, "neutral_gmr": neutral_gmr, "neutral_resistance": neutral_resist, "neutral_diameter": neutral_diam, "neutral_strands": neutral_strands}
        return(return_obj)
    
    def create_linespacing(self, itemname, spacings): # AB=0, BC=0, AC=0, AN=0, BN=0, CN=0):
        #if 0, line doesn't exist
        return_obj = {"object": "line_spacing", "name": itemname}
        for spacing in spacings.keys():
            return_obj[spacing] = spacings[spacing]
        return(return_obj)
        
    def create_lineconfig(self, name, conductors, linespacing):
        #conductors dict of A, B, C, N, for each that exist
        #conductor names follow phase
        return_obj = {"object": "line_configuration", "name": name, "spacing": linespacing}
        for conductor in conductors.keys():
            return_obj[conductor] = conductors[conductor]
        return(return_obj)
        
    def create_transformerconfig(self, name, connect_type, rating, source_volt, load_volt, resistance, reactance):
        return_obj = {"object": "transformer_configuration", "name": name, "connect_type": connect_type, "power_rating": rating, "primary_voltage": source_volt, "secondary_voltage": load_volt, "resistance": resistance, "reactance": reactance}
        return(return_obj)
       
    def create_load(self, name, phaseloads, nominal_volt="4160"):
        return_obj = {"object": "load", "name": name, "nominal_voltage": nominal_volt}
        phases = []
        for key in phaseloads.keys():
            return_obj[key] = phaseloads[key]
            phases.append(key.split("_")[-1])
        if phases[-1] != "N":
            phases.append("N")
        phases.sort()
        return_obj["phases"] = ''.join(phases)
        return(return_obj)
    
    def create_node(self, name, phases, nominal_volt="4160"):
        return_obj = {"object": "node", "name": name, "phasevals": phases, "nominal_voltage": nominal_volt}
        return(return_obj)

    def create_line(self, name, phases, fromnode, tonode, length, lineconfig):
        return_obj = {"object": "overhead_line", "name" : name, "phases": phases, "from": fromnode, "to": tonode, "length": length, "configuration": lineconfig}
        return(return_obj)
    
    def object_string(self, object_dict, objType):
        if ":" in object_dict["name"]:
            return_string =  "object " + objType + ":" + object_dict["name"].split(":")[1] +  " {\n"
        else:
            return_string =  "object " + objType + " {\n"
            return_string = return_string + "\tname " + object_dict["name"] + ";\n"
        for key in object_dict.keys():
            if key == "name" or key == "object":
                pass
            elif key == "phases":
                if object_dict[key][0] != "\"":
                    return_string = return_string + "\t" + key + " \"" + object_dict[key] + "\";\n"
                else:
                    return_string = return_string + "\t" + key + " " + object_dict[key] + ";\n"
            else:
                return_string = return_string + "\t" + key + " " + object_dict[key] + ";\n"
        return_string = return_string + "}\n"
        return(return_string)
        
    def check_header(self, line):
        #unused function?
        current = line.strip()[0:4]
        if current == "Over" or current == "Line" or current == "Unde" or current == "Spot":
            return(current)
        else:
            return(False)
            
    def get_load_mode(self, code):
        modes = {"Y-PQ": "constant_power", "Y-I": "constant_current", "Y-Z": 'constant_impedance', "D-PQ": "constant_power", "D-I": "constant_current", "D-Z": "constant_impedance"}
        return(modes[code])
        
    def read_glm_file(self, filename):
        objBuffer = {}
        FileToOpen = os.path.join(self.workingDir, filename)
        with open(FileToOpen, 'r') as inFile:
            currentObjType = ""
            currentObj = ""
            for line in inFile:
                if line.strip().startswith("object"):
                    currentObjType, nickname = self.get_glm_object_type(line)
                    if currentObjType not in objBuffer.keys():
                        objBuffer[currentObjType] = {}
                elif line.strip().startswith("}"):
                    currentObjType = ""
                    currentObj = ""
                elif line.strip().startswith("name"):
                    objAttrb = self.get_glm_object_attrbs(line.strip())
                    currentObj = objAttrb[1]
                    objBuffer[currentObjType][currentObj] = {objAttrb[0]: objAttrb[1]}
                elif line.strip() == "" or line.strip().startswith('//'):
                    pass
                else:
                    #catch un-named objects
                    if currentObj == "":
                        currentObj = ":".join([currentObjType, nickname])
                        objBuffer[currentObjType][currentObj] = {"name": currentObj}
                    #add attribute
                    objAttrb = self.get_glm_object_attrbs(line.strip())
                    objBuffer[currentObjType][currentObj][objAttrb[0]] = objAttrb[1]
        return(objBuffer)
        
    def get_glm_object_attrbs(self, strin):
        if '//' in strin:
            strin = strin.split('//')[0]    #strip comments
        tokens = strin.strip().split(" ")
        attrb = tokens[0]
        if len(tokens) > 2:
            tokens[-1] = tokens[-1].rstrip(";")
            value = " ".join(tokens[1:])
        else:
            value = tokens[1].rstrip(";")
        return([attrb, value])
    
    def get_glm_object_type(self, strin):
        tokens = strin.strip().split(" ")
        if ":" in tokens[1]:
            objType, nickname = tokens[1].split(":")
        else:
            objType = tokens[1]
            nickname = ''
        return(objType, nickname)
        
    def convert_load(self, loadType, power, voltage):
        outval = 0.0
        try:
            if loadType == "constant_current":
                outval = float(pow(voltage, 2) / (power * 1000))
            if loadType == "constant_impedance":
                outval = float((power * 1000 )/voltage)
            if loadType == "constant_power":
                outval = float(power * 1000)
            return(outval)
        except:
            print("zero value exception in load conversion")
            return(0.0)

    def get_phases_from_vals_node(self, phasedata, loadType, nominal):
        phasevals = [ float(phasedata[i]) for i in range(6) ]
        values = {}
        #presumes 0 value means phase isn't carried, this is wrong
        if phasevals[0] != 0.0 or phasevals[1] != 0.0:
            real = str(self.convert_load(loadType, phasevals[0], nominal))
            img = str(self.convert_load(loadType, phasevals[1], nominal))
            values["A"] = real + "+" + img + "j"
        if phasevals[2] != 0.0 or phasevals[3] != 0.0:
            real = str(self.convert_load(loadType, phasevals[2], nominal))
            img = str(self.convert_load(loadType, phasevals[3], nominal))
            values["B"] = real + "+" + img + "j"
        if phasevals[4] != 0.0 or phasevals[5] != 0.0:
            real = str(self.convert_load(loadType, phasevals[4], nominal))
            img = str(self.convert_load(loadType, phasevals[5], nominal))
            values["C"] = real + "+" + img + "j"
        return(values)  