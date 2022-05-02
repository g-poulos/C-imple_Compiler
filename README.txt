# Dimitropoulos Dimitrios, 4352, cse84352
# Poulos Grigorios, 4480, cse84480

* Usage: $python3 met.py <inputfile>
* The programs in the 'test' folder where used to test the compiler.Each sub-folder
  contains:
    - 'lex' and 'syntax': small programs that are expected to fail the compilation.
    - 'complete_programs': Complete programs that can be compiled without errors.
    - 'intermediate': Complete and small programs that where used to test the generated
                      quads after the compilation. This folder also contains a
                      sub-folder with the expected output of each test.
    - 'symbol_table': Programs from the course material to test the symbol table.
    - 'c_convertable': Programs that can be compiled and converted to C. The .c file
                       can then be also compiled and run. All programs expect an input
                       from the user.
* Unit tests where also used to test the 'intermediate' and 'complete_programs' test folders.s
* The implementation of the compiler follows the object-oriented structure which is
  described in the course material.



        ---------------    ---------------      ---------------     ---------------     ---------------
        |     Lex     |----|   Parser    |------|   Token     |     |     Quad    |     |     Scope   |
        ---------------    ---------------      ---------------     ---------------     ---------------


                                    -------------
                                    |   Entity  |
                                    -------------
                                           ^
                                          / \
                                           |
                                           |
               ------------------------------------------------------------
               |                  |                   |                   |
               |                  |                   |                   |
        -------------       -------------       -------------       --------------      ---------------
        |  Function |       |  Variable |       | Parameter |       |TempVariable|      |   Argument  |
        -------------       -------------       -------------       --------------      ---------------