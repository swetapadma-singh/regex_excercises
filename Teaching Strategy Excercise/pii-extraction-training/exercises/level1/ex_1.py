# Read Text from File
file_name = "data/raw/medical_report.txt"
try: 
    if not file_name.endswith(".txt"):
        print("Only text files are supported")
    else:
        with open(file_name, 'r') as file:
            content = file.readlines() 
        total_lines = len(content)
        total_words = 0
        for lines in content:
            words = len(lines.split())
            total_words += words
        print("Total lines in the file are: ",total_lines) 
        print("Total words in the file are: ",total_words)       
except FileNotFoundError:
    print("Kindly check. File not exists.")               
