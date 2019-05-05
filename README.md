# Examinus Calculatus

**Version 0.4.0**

A simple online CAS system. The project was written as an exam project.

---

## How to run the webserver
To run the web server, the python file named *app.py* in the *src* folder must be run.

### Required programs and packages
Examinus Calculatus calls into two programs and uses different python packages to be fully functional. What's needed is listed down below.

**Required programs:**
* [Gnuplot](https://sourceforge.net/projects/gnuplot/files/gnuplot/)
* [Graphviz](https://www.graphviz.org/download/)

**Required python packages:**
* graphviz
* functools
* math
* subprocess
* threading
* queue
* sys
* flask
* base64

To make it easy, there is an setup.py file in the root folder, which installs all the python packages needed automatically, whereas the programs are not included, but there is a link in the list to the download sites of the programs instead, so you can choose a version that is combatible with your specific operating system yourself.

---

## Current features
* Parser and interpreter that supports basic arithmetic, including nested expressions and the binary operators '+', '-', '*', '/', the unary operators '+', '-' and '!', and functions calls.
* A web-application that lets you interactively evaluate expressions.
    * Syntax highlighting
    * Built-in functions list.
    
## Planned features
* Support for simple algebra.
* Support for number theory.
* Support for calculations with units, and conversions between units.
* Menu to settings.
* The user must be able to change the editor theme.
* The user must be able to comtumize and style the plots.
* Live syntax hightlighting in the inputfield.
* Use of Cython to optimize the speed of calculations.
* Complete the ExCalc's ready and undo function.
* ExCalc must be able to solve computer algebra.

---

## Contributors
- Kian Banke Larsen.
- Markus Solecki Ellyton.


## License and copyright
* © Kian Banke Larsen, Odense Tekniske Gymnasium, Denmark.
* © Markus Solecki Ellyton, Odense Tekniske Gymnasium, Denmark.

Licensed under the [MIT License](LICENSE).