# import torch
# import numpy as np

# x= torch.empty(1)
# y = torch.empty(2,1)
# print(x)
# print(y)

# a = torch.rand(4,4)
# b = a.view(16)
# print(a)
# print(b)

# c= a.view(-1, 2)
# print(c)

# x = np.ones(5)
# print(x)
# y= torch.from_numpy(x)
# print(y)

#Gradient with autocad

# weights = torch.ones(4, requires_grad=True)

# for ep in range(2):
#     model_output = (weights*5).sum()
    
#     model_output.backward()
    
#     print(weights.grad)


#CLASSES IN PYTHON


class Employee:
    
    raise_amount = 1.06
    
    def __init__(self,first,last,pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'
        
    def display(self):
        # print('{}{}'.format(self.first,self.last)) 
        return '{}{}'.format(self.first,self.last) 
    
    def apply_raise(self):
        self.pay = int(self.pay + self.raise_amount)
        # self.pay = int(self.pay + Employee.raise_amount)  
    
    def fullname(self):
        return'{} {}'.format(self.first, self.last)    
    
    @classmethod
    def set_raise_amt(cls , amount):
        cls.raise_amount = amount  
        
    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split('-')
        return cls(first, last, pay)      
    
    @staticmethod
    def is_workingday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False    
        return True
    

class Devloper(Employee):
    raise_amount = 2.12
    
    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay)
        self.prog_lang = prog_lang
    
class Manager(Employee):
    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else :
            self.employees = employees
            
    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
                
    def remove_app(self, emp):
        if emp  in self.employees:
            self.employees.remove(emp)
            
    def print_emps(self):
        for emp in self.employees:
            print('--->',emp.first)
                    
emp_1 = Employee('Samir', 'Rai', 5000)
emp_2 = Employee('Saugat','Rai', 6000)

emp_string_1 = 'Summit-Gurung-10000000'

#INHERITANCE

dev_1 = Devloper('Summit', 'Gurung', 8000, 'Python')
dev_2 = Devloper('Aman', 'Shrestha', 12000, 'JAVA') 

Mngr_1 = Manager('Allen', 'Maharjan', 12000, [dev_1])

print(Mngr_1.first)
Mngr_1.add_emp(dev_1)
Mngr_1.add_emp(dev_2)

Mngr_1.print_emps()
# print(emp_1.pay)
# emp_1.apply_raise()
# print(emp_1.pay)


# print(dev_1.pay)
# dev_1.apply_raise()
# print(dev_1.pay)


# x = emp_2.display()
# print(x)

# y = Employee.display(emp_1)
# print(y)

# print(emp_1.first)
# print(emp_2.first)

# Employee.raise_amount = 1.04
# emp_1.raise_amount = 2.04

# print(emp_1.raise_amount)
# print(emp_2.raise_amount) 
 
# emp_1.apply_raise()
# emp_2.apply_raise()

# print(emp_1.pay) 
# print(emp_2.pay) 

#print(Employee.__dict__)
#print(emp_1.__dict__)

#CLASS METHOD

# Employee.set_raise_amt(2)
# emp_1.set_raise_amt(3)
# print(Employee.raise_amount)

#CLASS METHOD AS ALTERNATIVE CONSTRUCTOR

# new_emp = Employee.from_string(emp_string_1)
# print(new_emp.first)
# print(new_emp.last)
# print(new_emp.pay)

#STATIC METHOD

# import datetime
# my_day_1 = datetime.date(2023,12,29)
# my_day_2 = datetime.date(2023,12,23)
# print(Employee.is_workingday(my_day_1))
# print(Employee.is_workingday(my_day_2))


        
       
 
 