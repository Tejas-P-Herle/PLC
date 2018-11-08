PLC – Python Language Converter

TABLE OF CONTENTS:
  * Aim
  * Usage
  * Working

Aim: Interconversion of source code of a program from a given language A to required language B. 
NOTE: Works for any two languages designed with similar objectives (Python to Java) and NOT for languages designed for distinct purposes (HTML to CSS).
Usage:
  Currently supports only windows platform
  Prerequisites:
    Python interpreter 3.7
  Download the above git project.
  Run PLC.py file to launch language converter program.

Working: CONVERTING SOURCE CODE FROM PREVIOUSLY LEARNT EXAMPLES
For example,
Python – print(“Hello World!”)
Java      – Sytem.out.println(“Hello World!”);
Conversion method: Sort out similarities and dissimilarities
  Similarities – The statement to be printed remains the same = [(“Hello World!”)]
  Dissimilarities – The language specific instruction changes = [print, System.out.println, ;]
Given multiple examples for similar conversions, we can perfectly distinguish between Language Specific Code and Objective Specific Code
Python – 
1.  print(“Hello World!”) 
2.  print(“Second print statement”) 

Java – 
1.  System.out.println(“Hello World!”);
2.  System.out.println(“Second print statement”);
In case of multiple examples of similar conversions, for any 2 examples of conversion from a particular language, similarities between the lines of code will now be the Language Specific Code and dissimilarities will now be the Objective Specific Code.
Hence given sufficient, appropriate examples, we can distinguish between Language Specific Code and Objective Specific Code
  Python – Language Specific Code = [print(“, “)]
       Objective Specific Code = [Hello World!, Second print statement]
  Java     – Language Specific Code = [System.out.println(“, “);]
      Objective Specific Code = [Hello World!, Second print statement]

We can see that the Objective Specific Code remains the same for all languages.
Hence, we can generalize the conversion of the above statement from python to java as:
  print(“X”) -> System.out.println(“X”);
Where, X is the statement we want to print.
Hence, we can write code to use the above given conversion expression to convert any print statement it encounters present in python source code to java source code.
NOTE: The above mentioned mechanism is only the core of the current version of the program, other mechanisms of conversion are also working in parallel.


