Requires Python 3.6

PyPy (https://www.pypy.org/) is recommended as it results in enormous speedups on longer running BF programs.

`usage: bf.py [-h] [-c [{8,16,32}]] [-d [N]] file [input]`

Input can be read from stdin, a file, or a pipe

**Cell count:**  
30000 cells and expands by 30000 if the data pointer reaches the end  
Program exits if the data pointer goes below zero

**Cell size:**  
Unsigned 8 bit by default with options to use 16 or 32 bit cells  
Cell size can be specified with the -c, --cell-size flag  
Values wrap on overflow/underflow

**EOF:**  
Cell value is not changed on EOF

**Debug:**  
Supports an additional BF command `#` that will print N cells and the current value of the data pointer  
Number of cells to print can be specified with the -d, --debug flag

**Reference:**  
https://esolangs.org/wiki/Brainfuck  
https://en.wikipedia.org/wiki/Brainfuck  
http://www.hevanet.com/cristofd/brainfuck/

Credit to Daniel B Cristofani for the test programs.

