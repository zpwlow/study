from PyQt5 import QtCore
import tr

class AnswerJob(QtCore.QThread):
    updated = QtCore.pyqtSignal()
    def __init__(self,path):
        super(AnswerJob, self).__init__()
        self.path = path
        self.answer = []
        self.operator_precedence = {
            '(': 0,
            ')': 0,
            '+': 1,
            '-': 1,
            '/': 2,
            '*': 2,
        }

    def run(self):
        try:
            answer = tr.recognize(self.path)
            print(answer)
            answer = answer[0].replace('I', '1').replace('l', '1').replace('b', '6').replace('q', '9').replace('x', '*').replace(':', '/')
            postfix = self.postfix_convert(answer)
            da = self.cal_expression_tree(postfix)
        except:
            pass
        self.updated.emit()

    def postfix_convert(self,exp):
        '''
        将表达式字符串，转为后缀表达式
        如exp = "1+2*(3-1)-4"
        转换为：postfix = ['1', '2', '3', '1', '-', '*', '+', '4', '-']
        '''
        stack = []  # 运算符栈，存放运算符
        postfix = []  # 后缀表达式栈
        x = 0
        for char in exp:
            if char not in self.operator_precedence:  # 非符号，直接进栈
                if x == 1:
                    ch = postfix.pop()
                    char = ch + char
                    postfix.append(char)
                else:
                    postfix.append(char)
                x = 1
            else:
                x = 0
                if len(stack) == 0:  # 若是运算符栈啥也没有，直接将运算符进栈
                    stack.append(char)
                else:
                    if char == "(":
                        stack.append(char)
                    elif char == ")":  # 遇到了右括号，运算符出栈到postfix中，并且将左括号出栈
                        while stack[-1] != "(":
                            postfix.append(stack.pop())
                        stack.pop()

                    elif self.operator_precedence[char] > self.operator_precedence[stack[-1]]:
                        # 只要优先级数字大，那么就继续追加
                        stack.append(char)
                    else:
                        while len(stack) != 0:
                            if stack[-1] == "(":  # 运算符栈一直出栈，直到遇到了左括号或者长度为0
                                break
                            postfix.append(stack.pop())  # 将运算符栈的运算符，依次出栈放到表达式栈里面
                        stack.append(char)  # 并且将当前符号追放到符号栈里面

        while len(stack) != 0:  # 如果符号站里面还有元素，就直接将其出栈到表达式栈里面
            postfix.append(stack.pop())
        return postfix

    def calculate(self,num1, op, num2):
        if not num1.isdigit() and not num2.isdigit():
            raise ("num error")
        else:
            num1 = int(num1)
            num2 = int(num2)
        if op == "+":
            return num1 + num2
        elif op == "-":
            return num1 - num2
        elif op == "*":
            return num1 * num2
        elif op == "/":
            if num2 == 0:
                raise ("zeros error")
            else:
                return num1 / num2
        else:
            raise ("op error")

    def returnchar(self,num1, op, num2):
        if not num1.isdigit() and not num2.isdigit():
            raise ("num error")
        if op == "+":
            return num1 + '+' + num2
        elif op == "-":
            return num1 + '-' + num2
        elif op == "*":
            if num1.find('+') >= 0 or num1.find("-") >= 0:
                num1 = '(' + num1 + ')'
            if num2.find('+') >= 0 or num2.find("-") >= 0:
                num2 = '(' + num2 + ')'
            return num1 + '×' + num2
        elif op == "/":
            if num2 == 0:
                raise ("zeros error")
            else:
                if num1.find('+') >= 0 or num1.find("-") >= 0:
                    num1 = '(' + num1 + ')'
                if num2.find('+') >= 0 or num2.find("-") >= 0:
                    num2 = '(' + num2 + ')'
                return num1 + '÷' + num2
        else:
            raise ("op error")

    def cal_expression_tree(self,postfix):
        stack = []
        x = 1
        self.getmath(postfix)
        for char in postfix:
            stack.append(char)
            if char in "+-*/":
                op = stack.pop()
                num2 = stack.pop()
                num1 = stack.pop()
                value = self.calculate(num1, op, num2)
                value = str(value)  # 计算结果是数值类型，将其化为字符串类型
                stack.append(value)
                data = []
                for s in stack:
                    data.append(s)
                for p in postfix[x:]:
                    data.append(p)
                self.getmath(data)
            x = x + 1
        return stack[0]

    def getmath(self,data):
        ch = []
        for da in data:
            ch.append(da)
            if da in "+-*/":
                op = ch.pop()
                num2 = ch.pop()
                num1 = ch.pop()
                value = self.returnchar(num1, op, num2)
                ch.append(value)
        self.answer.append(ch[0])

    def getanswer(self):
        print(self.answer)
        return self.answer