functions = [None for _ in range(10)]
ret_functions = [None for _ in range(10)]
labels = {}
vars = {}
cmp = [None, None]
response = [None]

def preapre_data(line):
    if len(line) == 0 or line[0] ==";":
        return False
    return True

def instruction_interpreter(line):
        if ';' in line:
            komment_idx = line.index(';')
            line = line[:komment_idx]
        inst = list(filter(preapre_data, line.split(' ')))
        if inst[0] == 'mov':
            dest = inst[1].rstrip(',')
            val = inst[2]
            if val in vars:
                vars[dest] = vars[val]
            elif val.isnumeric():
                vars[dest] = float(val)
        elif inst[0] == 'inc':
            val = inst[1].rstrip(',')
            vars[val] += 1
        elif inst[0] == 'dec':
            val = inst[1].rstrip(',')
            vars[val] -= 1
        elif inst[0] == 'add':
            dest = inst[1].rstrip(',')
            val = inst[2]
            if val in vars:
                vars[dest] += vars[val]
            elif val.isnumeric():
                vars[dest] += float(val)
        elif inst[0] == 'sub':
            dest = inst[1].rstrip(',')
            val = inst[2]
            if val in vars:
                vars[dest] -= vars[val]
            elif val.isnumeric():
                vars[dest] -= float(val)
        elif inst[0] == 'mul':
            dest = inst[1].rstrip(',')
            val = inst[2]
            if val in vars:
                vars[dest] *= vars[val]
            elif val.isnumeric():
                vars[dest] *= float(val)
        elif inst[0] == 'div':
            dest = inst[1].rstrip(',')
            val = inst[2]
            if val in vars and vars[val] != 0:
                vars[dest] //= vars[val]
            elif val.isnumeric() and float(val) != 0:
                vars[dest] //= float(val)
            else:
                raise Exeption
        elif inst[0] == 'jmp':
            func = inst[1]
            if func in labels:
                for innet_inst in functions[labels[func]]:
                    if not instruction_interpreter(innet_inst):
                        break
            return ret_functions[labels[inst[1]]]  
        elif inst[0] == 'cmp':
            if inst[1].rstrip(',') in vars:
                first = vars[inst[1].rstrip(',')]
            if inst[2] in vars:
                second = vars[inst[2]]
            else:
                second = float(inst[2])
            cmp[0] = (first)
            cmp[1] = (second)

        elif inst[0] == 'jne':

            if cmp[0] != cmp[1]:
                for innet_inst in functions[labels[inst[1]]]:
                    if not instruction_interpreter(innet_inst):
                        break
                if not ret_functions[labels[inst[1]]]:
                    return False   
            
        elif inst[0] == 'je':

            if cmp[0] == cmp[1]:
                for innet_inst in functions[labels[inst[1]]]:
                    if not instruction_interpreter(innet_inst):
                        return False
                if not ret_functions[labels[inst[1]]]:
                    return False   
                    
        elif inst[0] == 'jge':

            if cmp[0] >= cmp[1]:
                for innet_inst in functions[labels[inst[1]]]:
                    if not instruction_interpreter(innet_inst):
                        break
                if not ret_functions[labels[inst[1]]]:
                    return False   
                  
        elif inst[0] == 'jg':
 
            if cmp[0] > cmp[1]:
                for innet_inst in functions[labels[inst[1]]]:
                    if not instruction_interpreter(innet_inst):
                        break
                if not ret_functions[labels[inst[1]]]:
                    return False   
                 
        elif inst[0] == 'jle':
            if cmp[0] <= cmp[1]:
                for innet_inst in functions[labels[inst[1]]]:
                    if not instruction_interpreter(innet_inst):
                        break

                if not ret_functions[labels[inst[1]]]:
                    return False                

        elif inst[0] == 'jl':
            if cmp[0] < cmp[1]:
                for innet_inst in functions[labels[inst[1]]]:
                    if not instruction_interpreter(innet_inst):
                        break
                if not ret_functions[labels[inst[1]]]:
                    return False


        elif inst[0] == 'msg':
            res = ""
            parts = line[line.index('g')+1:].strip().split(',')
            for idx, substr in enumerate(parts):
                if substr == " '" and parts[idx+1] == " '":
                    res += ", "
                    continue
                substr = substr.strip().strip("'")
                if substr in vars:
                    if int(vars[substr]) == vars[substr]:
                        res += str(int(vars[substr]))
                    else:
                        res += str(vars[substr])
                else:
                    res += substr
            response[0] = res
            print(res)
        elif inst[0] == 'ret':
            return False
        elif inst[0] == 'call':
            func = inst[1]
            if func in labels:
                for innet_inst in functions[labels[func]]:
                    res = instruction_interpreter(innet_inst)
                    if not res:
                        break
                if not ret_functions[labels[func]]:
                    return False
        return True


def assembler_interpreter(program):
    data = list(filter(preapre_data, program.split('\n')))
    end_idx = data.index('end')
    current_program = data[:end_idx+1]
    functions_defs = data[end_idx + 1:]
    cnt = 0

    start = None
    for idx, line in enumerate(functions_defs):
        if ":" in line and "msg" not in line:
            labels[line.rstrip(':')] = cnt
            functions[cnt-1] = functions_defs[start:idx]
            cnt += 1
            start = idx
    functions[cnt-1] = functions_defs[start:]

    for idx, func in enumerate(functions[:cnt]):
        if "ret" == func[-1].strip():
            ret_functions[idx] = True
        else:
            ret_functions[idx] = False

           
    end = None
    for idx, line in enumerate(current_program):
        res = instruction_interpreter(line)

        if "end" in line:
            end = 1
        
    if end is not None:
        return response[0] # output
    else:
        return -1


assembler_interpreter('''
mov   a, 2            ; value1
mov   b, 10           ; value2
mov   c, a            ; temp1
mov   d, b            ; temp2
call  proc_func
call  print
end

proc_func:
    cmp   d, 1
    je    continue
    mul   c, a
    dec   d
    call  proc_func

continue:
    ret

print:
    msg a, '^', b, ' = ', c
    ret
''')

functions = [None for _ in range(10)]
ret_functions = [None for _ in range(10)]
labels = {}
vars = {}
cmp = [None, None]
response = [None]

def preapre_data(line):
    if len(line) == 0 or line[0] ==";":
        return False
    return True

def instruction_interpreter(line):
        if ';' in line:
            komment_idx = line.index(';')
            line = line[:komment_idx]
        inst = list(filter(preapre_data, line.split(' ')))
        if inst[0] == 'mov':
            dest = inst[1].rstrip(',')
            val = inst[2]
            if val in vars:
                vars[dest] = vars[val]
            elif val.isnumeric():
                vars[dest] = float(val)
        elif inst[0] == 'inc':
            val = inst[1].rstrip(',')
            vars[val] += 1
        elif inst[0] == 'dec':
            val = inst[1].rstrip(',')
            vars[val] -= 1
        elif inst[0] == 'add':
            dest = inst[1].rstrip(',')
            val = inst[2]
            if val in vars:
                vars[dest] += vars[val]
            elif val.isnumeric():
                vars[dest] += float(val)
        elif inst[0] == 'sub':
            dest = inst[1].rstrip(',')
            val = inst[2]
            if val in vars:
                vars[dest] -= vars[val]
            elif val.isnumeric():
                vars[dest] -= float(val)
        elif inst[0] == 'mul':
            dest = inst[1].rstrip(',')
            val = inst[2]
            if val in vars:
                vars[dest] *= vars[val]
            elif val.isnumeric():
                vars[dest] *= float(val)
        elif inst[0] == 'div':
            dest = inst[1].rstrip(',')
            val = inst[2]
            if val in vars and vars[val] != 0:
                vars[dest] //= vars[val]
            elif val.isnumeric() and float(val) != 0:
                vars[dest] //= float(val)
            else:
                raise Exeption
        elif inst[0] == 'jmp':
            func = inst[1]
            if func in labels:
                for innet_inst in functions[labels[func]]:
                    if not instruction_interpreter(innet_inst):
                        break
            return ret_functions[labels[inst[1]]]  
        elif inst[0] == 'cmp':
            if inst[1].rstrip(',') in vars:
                first = vars[inst[1].rstrip(',')]
            if inst[2] in vars:
                second = vars[inst[2]]
            else:
                second = float(inst[2])
            cmp[0] = (first)
            cmp[1] = (second)

        elif inst[0] == 'jne':

            if cmp[0] != cmp[1]:
                for innet_inst in functions[labels[inst[1]]]:
                    if not instruction_interpreter(innet_inst):
                        break
                if not ret_functions[labels[inst[1]]]:
                    return False   
            
        elif inst[0] == 'je':

            if cmp[0] == cmp[1]:
                for innet_inst in functions[labels[inst[1]]]:
                    if not instruction_interpreter(innet_inst):
                        break
                if not ret_functions[labels[inst[1]]]:
                    return False   
                    
        elif inst[0] == 'jge':

            if cmp[0] >= cmp[1]:
                for innet_inst in functions[labels[inst[1]]]:
                    if not instruction_interpreter(innet_inst):
                        break
                if not ret_functions[labels[inst[1]]]:
                    return False   
                  
        elif inst[0] == 'jg':
 
            if cmp[0] > cmp[1]:
                for innet_inst in functions[labels[inst[1]]]:
                    if not instruction_interpreter(innet_inst):
                        break
                if not ret_functions[labels[inst[1]]]:
                    return False   
                 
        elif inst[0] == 'jle':
            if cmp[0] <= cmp[1]:
                for innet_inst in functions[labels[inst[1]]]:
                    if not instruction_interpreter(innet_inst):
                        break

                if not ret_functions[labels[inst[1]]]:
                    return False                

        elif inst[0] == 'jl':
            if cmp[0] < cmp[1]:
                for innet_inst in functions[labels[inst[1]]]:
                    if not instruction_interpreter(innet_inst):
                        break
                if not ret_functions[labels[inst[1]]]:
                    return False


        elif inst[0] == 'msg':
            res = ""
            parts = line[line.index('g')+1:].strip().split(',')
            for idx, substr in enumerate(parts):
                if substr == " '" and parts[idx+1] == " '":
                    res += ", "
                    continue
                substr = substr.strip().strip("'")
                if substr in vars:
                    if int(vars[substr]) == vars[substr]:
                        res += str(int(vars[substr]))
                    else:
                        res += str(vars[substr])
                else:
                    res += substr
            response[0] = res
        elif inst[0] == 'ret':
            return False
        elif inst[0] == 'call':
            func = inst[1]
            if func in labels:
                for innet_inst in functions[labels[func]]:
                    if not instruction_interpreter(innet_inst):
                        break
                if not ret_functions[labels[func]]:
                    return False
        return True


def assembler_interpreter(program):
    data = list(filter(preapre_data, program.split('\n')))
    end_idx = data.index('end')
    current_program = data[:end_idx+1]
    functions_defs = data[end_idx + 1:]
    cnt = 0

    start = None
    for idx, line in enumerate(functions_defs):
        if ":" in line and "msg" not in line:
            labels[line.rstrip(':')] = cnt
            functions[cnt-1] = functions_defs[start:idx]
            cnt += 1
            start = idx
    functions[cnt-1] = functions_defs[start:]

    for idx, func in enumerate(functions[:cnt]):
        if "ret" == func[-1].strip():
            ret_functions[idx] = True
        else:
            ret_functions[idx] = False

           
    end = None
    for idx, line in enumerate(current_program):
        res = instruction_interpreter(line)
        print(line, res)
        if not res:
            break
        if "end" in line:
            end = 1
        
    if end is not None:
        return response[0] # output
    else:
        return -1