from intbase import InterpreterBase as IB, ErrorType as ET
from util import remove_line_num
from MethodDef import MethodDef
from VariableDef import VariableDef

class ObjectDef:
    def __init__(self, category, fields:set[VariableDef], methods:set[MethodDef], interpreter):
        self.category = category
        self.fields = fields
        self.methods = methods
        self.int = interpreter

        self.vars = {name:value for name, value in zip([x.name for x in fields], [x.value for x in fields])}

    def __str__(self):
        return f'Category {self.category}\nFields: {self.fields}\nMethods: {self.methods}\n'

    def __repr__(self):
        return self.__str__()

    
    def call_method(self, method_name, params):
        method = self.find_method(method_name)
        if not method:
            self.int.error(ET.NAME_ERROR, "Method not found")
        
        if len(params) != len(method.args):
            self.int.error(ET.TYPE_ERROR, "Incorrent number of parameters were given")

        statement = method.statement
        res = self.run_statement(statement, params)
        return res


    def run_statement(self, statement, params):
        match statement[0]:
            case self.int.PRINT_DEF:
                res = ''
                for i in range(1,len(statement)):
                    next = self.resolve_exp(statement[i])
                    if next is True:
                        next = 'true'
                    if next is False:
                        next = 'false'
                    res += str(next)
                
                self.int.output(res)


    def resolve_exp(self, exp):
        if type(exp) is not list:
            # exp, isVar = remove_line_num(exp)
            # # valid variable
            # if isVar and  exp in self.vars.keys():
            #     exp = self.vars[exp]
            # #invalid variable
            # elif isVar and exp not in self.vars.keys():
            #     self.int.error(ET.NAME_ERROR, "Undefined variable")
            # return exp
            return self.unwrap_simp_exp(exp)

        res = None
        match exp[0]:
            case '+':
                arg1 = self.resolve_exp(exp[1])
                arg2 = self.resolve_exp(exp[2])
                if self.both_str(arg1, arg2) or self.both_int(arg1, arg2):
                    res = arg1 + arg2
                else:
                    self.int.error(ET.TYPE_ERROR, "Incompatible types using the + operator")
            case '-':
                arg1 = self.resolve_exp(exp[1])
                arg2 = self.resolve_exp(exp[2])
                if self.both_int(arg1, arg2):
                    res = arg1 - arg2
                else:
                    self.int.error(ET.TYPE_ERROR, "Incompatible types using the - operation")
            case '*':
                arg1 = self.resolve_exp(exp[1])
                arg2 = self.resolve_exp(exp[2])
                if self.both_int(arg1, arg2):
                    res = arg1 * arg2
                else:
                    self.int.error(ET.TYPE_ERROR, "Incompatible types using the * operation")
            case '/':
                arg1 = self.resolve_exp(exp[1])
                arg2 = self.resolve_exp(exp[2])
                if self.both_int(arg1, arg2):
                    res = arg1 / arg2
                else:
                    self.int.error(ET.TYPE_ERROR, "Incompatible types using the / operation")
            case '%':
                arg1 = self.resolve_exp(exp[1])
                arg2 = self.resolve_exp(exp[2])
                if self.both_int(arg1, arg2):
                    res = arg1 % arg2
                else:
                    self.int.error(ET.TYPE_ERROR, "Incompatible types using the / operation")

        return res


    def unwrap_simp_exp(self,exp):
        exp, isVar = remove_line_num(exp)
        # valid variable
        if isVar and  exp in self.vars.keys():
            exp = self.vars[exp]
        #invalid variable
        elif isVar and exp not in self.vars.keys():
            self.int.error(ET.NAME_ERROR, "Undefined variable")
        return exp


    def both_str(self, arg1, arg2):
        return isinstance(arg1, str) and isinstance(arg2, str)


    def both_int(self, arg1, arg2):
        return isinstance(arg1, int) and isinstance(arg2, int)


    def find_method(self, method_name):
        for m in self.methods:
            if m.name == method_name:
                return m

        return None
