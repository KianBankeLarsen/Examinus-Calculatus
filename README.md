# Examinus Calculatus

**Version 0.4.0**

A simple online CAS system. The project was written as an exam project.

---

## How to run the web server
To run the web server, the python file named *app.py* in the *src* folder must be run.

### Required programs and packages
Examinus Calculatus calls into two programs and uses different python packages to be fully functional. What's needed is listed down below. While some of the programs and packages listed are not strictly necessary, it's recommended that you install all of them to ensure that everything functions properly. As a side note: compatability of all the packages can only be guaranteed for Python version 3.6 and 3.7.

**Required programs:**
* [Gnuplot](https://sourceforge.net/projects/gnuplot/files/gnuplot/) -- required to make plots.
* [Graphviz](https://www.graphviz.org/download/) -- required to render Abstract Syntax Trees, mostly for debugging purposes.

**Required python packages:**
* gmpy
* graphviz
* functools
* math
* subprocess
* threading
* queue
* sys
* flask
* base64

If using pip to install, some of the packages above may require a C compiler to build. On Windows you can visit [this great resource](https://www.lfd.uci.edu/~gohlke/pythonlibs/) for pre-compiled binaries.

---

## Current features
* Parser and interpreter that supports basic arithmetic, including nested expressions and the binary operators '+', '-', '*', '/', '^' the unary operators '+', '-' and '!', and function calls.
* A web-application that lets you interactively evaluate expressions.
    * Syntax highlighting
    * A built-in functions list.
    
## Planned features
* Support for simple algebra.
* Support for number theory.
* Support for calculations with units, and conversions between units.
* Menu for settings.
* The user must be able to change the editor theme.
* The user must be able to customize and style the plots.
* Live syntax hightlighting in the input field.
* Use of Cython to optimize the speed of calculations.
* Complete redo and undo function.

---

## Contributors
- Kian Banke Larsen.
- Markus Solecki Ellyton.


## License and copyright
* © Kian Banke Larsen, Odense Tekniske Gymnasium, Denmark.
* © Markus Solecki Ellyton, Odense Tekniske Gymnasium, Denmark.

Licensed under the [MIT License](LICENSE).

