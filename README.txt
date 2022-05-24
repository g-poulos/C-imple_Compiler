# Dimitropoulos Dimitrios, 4352, cse84352
# Poulos Grigorios, 4480, cse84480

* Usage: $python3 met.py <inputfile>
* The programs in the 'test' folder where used to test the compiler. The sub-folders
  contain:
    - 'lex' and 'syntax': Small sized programs that are expected to fail the compilation.
    - 'complete_programs': Complete programs that can be compiled without errors.
    - 'intermediate': Complete and small sized programs that where used to test the
                      generated quads after the compilation. This folder also contains
                      a sub-folder with the expected output of each test.
    - 'symbol_table': Programs from the course material to test the symbol table. Its
                      expected output was also tested with programs from the other test
                      directories.
    - 'c_convertable': Programs that can be compiled and converted to C. The .c file
                       can then be also compiled and run. All programs expect an input
                       from the user.
    - 'final_code': Programs from the class material that can be compiled and converted
                    to risc-v assembly code.
                    The programs in the 'c_convertable' directory can also be compiled
                    and converted to assembly code.
* The 'complete_programs' and 'intermediate' tests were automatically being run in every
  code addition to ensure the correct functionality of the compiler.
* The implementation of the compiler follows the object-oriented structure which is
  described in the course material.
* To implement the functions of the final code, as mentioned, the class material examples
  were used to create a Junit-styled test with expected outcome. The outcome of the class
  material assembly code was altered to correct potential typos. In order to test the final
  assembly code several risk-v compilers were used but the pseudo instructions that our
  compiler is generating were not included.


  A simple class diagram is shown below:

        ---------------    ---------------      ---------------     ---------------
        |     Lex     |----|   Parser    |      |     Quad    |     |     Scope   |
        ---------------    ---------------      ---------------     ---------------
               |
        ---------------
        |    Token    |             -------------
        ---------------             |   Entity  |
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
