import json
import urllib.request



class NumericProcessor:
    def __init__(self, computations_list):
        self.computations_list = computations_list
        
        # You can add more initialization code here if you'd like.

    def run_computations(self):
        for computation in self.computations_list:
            self.run_one_computation(computation)
           
    
    def run_one_computation(self, computation):
        operation = computation["operation"]
        values = computation["values"]
        if operation == "add":
            self.add(values)
        elif operation == "subtract":
            self.subtract(values)
        elif operation == "multiply":
            self.multiply(values)
        elif operation == "divide":
            self.divide(values)
        elif operation == "display":
            self.display(values)
        elif operation == "api-compute":
            expression = values[0]
            self.send_to_api(expression)
    def add(self, values):
            total = 0
            for number in values:
                 if number == "ANS":
                    number = self.ans
                 else:
                    number = float(number)
                 total += number
            self.ans = total
      
    def subtract(self, values):
            total = 0
            for number in values:
                 if number == "ANS":
                    number = self.ans
                 else:
                    number = float(number)
                 total -= number
                 abs_total = abs(total)
            self.ans = abs_total
         
    def multiply(self, values):
            total = 1
            for number in values:
                 if number == "ANS":
                    number = self.ans
                 else:
                    number = float(number)
                 total *= number
            self.ans = total
           
    def divide(self, values):
            total = 1
            for number in values:
                 if number == "ANS":
                    number = self.ans
                 else:
                    number = float(number)
                 total /= number
            self.ans = total
            
    def display(self, values):
            first_number = values[0]
            if first_number == "ANS":
                print(self.ans)
            else:
                print(first_number)
    def send_to_api(self, expression):
        url = get_mathjs_api_url(expression)
        response = urllib.request.urlopen(url)
        result = response.read().decode('utf-8')
        result_in_float = float(result)
        self.ans = result_in_float

def load_computations_list_from_file(filename):
    with open(filename, 'r') as f:
        contents = json.load(f)
        return contents['computations']


def get_mathjs_api_url(expression):
    # Expression is a string such as '1 + 1'.
    # Some characters need to be transformed when they are sent to the api.
    # urllib.parse.quote does this.
    # For example, it turns '+' into the code '%2B' so that the api can receieve it.
    expression = urllib.parse.quote(expression)
    url = 'http://api.mathjs.org/v4/?expr=' + expression
    return url

class OperationCounterNumericProcessor(NumericProcessor):
    def __init__(self, computations_list):
        super().__init__(computations_list)
        self.count_operations = {
            "add": 0,
            "subtract": 0,
            "multiply": 0,
            "divide": 0, 
            "api-compute": 0, 
            "display": 0
        }
    def run_one_computation(self, computation):
        operation = computation["operation"]
        self.count_operations[operation] += 1
        super().run_one_computation(computation)
    def show_statistics(self):
        for key, value in self.count_operations.items():
            print(f"operation: {key}, count: {value}")

if __name__ == '__main__':
    computations = load_computations_list_from_file('example_api.json')
    processor = NumericProcessor(computations)
    processor.run_computations()
    NumericProcessor= OperationCounterNumericProcessor(computations)
    NumericProcessor.show_statistics()
