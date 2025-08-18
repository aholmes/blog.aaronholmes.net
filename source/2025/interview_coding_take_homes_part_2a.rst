.. meta::
    :date: 2025-08-03

Interview Coding Take-Homes: Part 2.a
=====================================

|pagedate|

.. tags:: Programming, Software, Interviewing

UCLA Health - Maze Bug
-----------------------------

This take-home was for a Senior Cloud DevOps Engineer position in a key IT organization at UCLA Health.

This is part 1 of a two-part take-home.

Prompt
------

.. pull-quote::

    This is an intentionally incorrect python script to play through a maze. Can you spot the error and get it working?

.. scrollable::

    .. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-broken.py
       :language: python
       :linenos:
       :caption: :download:`pymaze-broken.py <../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-broken.py>`

My Approach
-----------

Testing the Application
^^^^^^^^^^^^^^^^^^^^^^^

First, I executed the code to see what it does and how it behaves.

.. code-block:: text

    $ python pymaze-broken.py
    Welcome to the maze game!
    Use WASD to move. Try to find the exit (E) while collecting items (*)!
    ##########
    #P       #
    #        #
    #        #
    #  *     #
    #*       #
    # *      #
    #        #
    #       E#
    ##########
    Enter your move (WASD):

So far, so good.

The code states to gather items and find the exit, so let's do that.

.. code-block:: text

    ##########
    #        #
    #        #
    #        #
    #        #
    #        #
    #        #
    #       P#
    #       E#
    ##########
    Enter your move (WASD):

The ``P`` moves around, so that's us, the player.

Gathering items worked without issue, so let's try to "find the exit."

.. code-block:: text

    Enter your move (WASD): s
    ##########
    #        #
    #        #
    #        #
    #        #
    #        #
    #        #
    #        #
    #       P#
    ##########
    Enter your move (WASD):

Uh oh ... looks like the game doesn't finish when the user finds the exit.

In fact, we can keep moving around, but now the exit is gone.

.. code-block:: text

    Enter your move (WASD): w
    ##########
    #        #
    #        #
    #        #
    #        #
    #        #
    #        #
    #       P#
    #        #
    ##########
    Enter your move (WASD):

Examining the Code
^^^^^^^^^^^^^^^^^^

Next, I looked at parts of the code, starting from the application entrypoint.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-broken.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 61 - 85

We can see several calls to ``move_player`` in response to the WASD inputs,
and then a check for whether the player has moved onto the exit position.

This last check seems to be what stops the main ``while`` loop on line 65,
so we need to figure out what prevented that condition from triggering.
My intuition says we need to understand what ``maze`` contains in order to
check whether this condition is correct.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-broken.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 83 - 85
   :dedent:

Debugging
^^^^^^^^^
   
Because this is new code I haven't seen before, the most expedient next step is to run
the application in a `debugger <https://en.wikipedia.org/wiki/Debugger>`__. This way
I can see what ``maze`` contains without needing to manually walk through the code.
This quickly gives me a mental map of what's happening in the application.

Python includes a debugger called `pdb <https://docs.python.org/3/library/pdb.html>`__
that I will use for this. There are other tools, such as VSCode, but this application
is simple enough that we should be able to figure this out on the command line.

We start ``pdb`` with ``python -m pdb <script>``.

.. code-block:: text

    $ python -m pdb pymaze-broken.py
    > pymaze-broken.py(1)<module>()
    -> import random

It helps to get a quick reference of the commands available to us.

.. code-block:: text

    (Pdb) ?

    Documented commands (type help <topic>):
    ========================================
    EOF    cl         disable     ignore    n        return  u          where
    a      clear      display     interact  next     retval  unalias
    alias  commands   down        j         p        run     undisplay
    args   condition  enable      jump      pp       rv      unt
    b      cont       exceptions  l         q        s       until
    break  continue   exit        list      quit     source  up
    bt     d          h           ll        r        step    w
    c      debug      help        longlist  restart  tbreak  whatis

    Miscellaneous help topics:
    ==========================
    exec  pdb

I know I want to see what ``maze`` looks like,
so I will put a breakpoint right after that,
on line 63. Then, I will let the application
continue running.

.. code-block:: text

    (Pdb) b 63
    Breakpoint 1 at pymaze-broken.py:63
    (Pdb) c
    > pymaze-broken.py(63)main()
    -> print("Welcome to the maze game!")
    (Pdb) l
     58                     return (i, j)
     59
     60     # Main function to run the game
     61     def main():
     62         maze = initialize_maze()
     63 B->     print("Welcome to the maze game!")
     64         print("Use WASD to move. Try to find the exit (E) while collecting items (*)!")
     65         while True:
     66             print_maze(maze)
     67             direction = input("Enter your move (WASD): ").upper()
     68             if direction == 'W':
    (Pdb)

If we type a variable's name, ``pdb`` prints its
string representation.

.. code-block:: text

    (Pdb) maze
    [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], ['#', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'], ['#', ' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', '#'], ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'], ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'], ['#', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'], ['#', ' ', ' ', ' ', ' ', '*', ' ', ' ', ' ', '#'], ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'], ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'E', '#'], ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

Fortunately for us, ``maze`` is a list and we don't need to do anything fancy to see its contents.

That said, it is nearly unparseable in a single line, so we can tell ``pdb`` to "pretty print" the
objet instead.

.. code-block:: text

    (Pdb) pp maze
    [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
     ['#', 'P', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
     ['#', ' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', '#'],
     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
     ['#', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
     ['#', ' ', ' ', ' ', ' ', '*', ' ', ' ', ' ', '#'],
     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'E', '#'],
     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

So we know we're looking at a matrix whose values represent the different characters seen in the maze.
Given that we're trying to figure out the comparison of the player position within the maze to the ``EXIT``
variable, let's check what some of these values are too.

.. code-block:: text

    (Pdb) player_pos
    *** NameError: name 'player_pos' is not defined

Oops - that didn't work. Let's see where ``player_pos`` gets set. If we look back at the code,
we see that it gets set in both ``move_player`` ...

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-broken.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 44 - 51

and in the main loop ...

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-broken.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 79 - 82
   :dedent:

In Python, block-level assignments in methods are scoped to
those methods, so we know that the ``move_player`` assignment
is irrelevant here, which means we need line 82 to run.

Let's put a breakpoint there and step through the code.

.. code-block:: text

    (Pdb) b 82
    Breakpoint 2 at pymaze-broken.py:82
    (Pdb) c
    Welcome to the maze game!
    Use WASD to move. Try to find the exit (E) while collecting items (*)!
    ##########
    #P       #
    #     *  #
    #        #
    #        #
    #*       #
    #    *   #
    #        #
    #       E#
    ##########
    Enter your move (WASD):

Now it can get a little tricky to manage both the application
flow and the debugger. My command line input will currently be
sent to the application, not the debugger, because the application
is reading from STDIN.

Here's what happens when I enter input into the application.

.. code-block:: text

    Enter your move (WASD): d
    > pymaze-broken.py(82)main()
    -> player_pos = find_player(maze)
    (Pdb)

We hit the breakpoint we set earlier! The application is now
paused again, and we can input into the debugger.

.. code-block:: text

    (Pdb) l
     77                 print("Invalid move! Use WASD.")
     78                 continue
     79             if not moved:
     80                 print("Cannot move there! Try another direction.")
     81             else:
     82 B->             player_pos = find_player(maze)
     83                 if maze[player_pos[0]][player_pos[1]] == EXIT:
     84                     print("Congratulations! You found the exit!")
     85                     break
     86
     87     if __name__ == "__main__":

We want to see what ``find_player`` is doing, so let's "step into" it.

.. code-block:: text

    (Pdb) s
    --Call--
    > pymaze-broken.py(54)find_player()
    -> def find_player(maze):
    (Pdb) n
    > pymaze-broken.py(55)find_player()
    -> for i in range(len(maze)):
    (Pdb) l
     50             return True
     51         return False
     52
     53     # Function to find the player's position
     54     def find_player(maze):
     55  ->     for i in range(len(maze)):
     56             for j in range(len(maze[i])):
     57                 if maze[i][j] == PLAYER:
     58                     return (i, j)
     59
     60     # Main function to run the game

I also stepped to the "next" instruction, so we're now at the
beginning of the outer ``for`` loop. Let's see what some of these
instructions are doing.

Given that ``maze`` is a matrix, it seems like the outer ``for``
loop will iterate over rows. Let's make sure.

.. code-block:: text

    (Pdb) list(range(len(maze)))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

That looks right - there are ten rows in the maze. Let's step
into the first iteration, and double-check whether the inner
``for`` loop iterates over columns.

.. code-block:: text

    (Pdb) s
    > pymaze-broken.py(56)find_player()
    -> for j in range(len(maze[i])):
    (Pdb) list(range(len(maze[i])))
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

That also looks right - there are ten columns for the row ``i``,
which is currently row ``0``:

.. code-block:: text

    (Pdb) i
    0
    (Pdb) maze[i]
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']

Let's step into this and check the next instructions.

.. code-block:: text

    (Pdb) s
    > pymaze-broken.py(57)find_player()
    -> if maze[i][j] == PLAYER:
    (Pdb) i
    0
    (Pdb) !j # we need a preceeding `!` because `j` is the pdb "jump" command
    0
    (Pdb) maze[i][j]
    '#'
    (Pdb) PLAYER
    'P'
    (Pdb) maze[i][j] == PLAYER
    False

So it seems that we're iterating over every character in the maze
to determine whether that character is ``P``. If the character is ``P``
then we know we've found the player, and we return their (i,j) position.

Let's make sure - we'll set a breakpoint at the ``return`` statement.

.. code-block:: text

    (Pdb) b 58
    Breakpoint 3 at pymaze-broken.py:58
    (Pdb) c
    > pymaze-broken.py(58)find_player()
    -> return (i, j)
    (Pdb) (i, j)
    (1, 2)

If we print the maze again, we'll see that (1, 2) is indeed where the
character ``P`` is.

.. code-block:: text

    (Pdb) pp maze
    [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
     ['#', ' ', 'P',
    # truncated

We should also note that the position the player `was` in is now
a space, while the position that the player `now` occupies was a space
and is now a ``P``.

By now we can start to postulate on the behavior and the possible
origin of the error.

We know, in the UI:

* When the player reaches ``E``, the application does not exit
* The player can continue to move around, and the ``E`` disappears

And in the code:

* Previous player positions are replaced with a space
* The current player position is replaced with a ``P``
* Some value is compared with the variable ``EXIT`` (the character ``E``)

Is it possible that we want to compare ``P`` with ``E``, but we can't
because ``E`` is now gone?

Let's continue on to our exit condition.

To save us some sanity, let's clear all the breakpoints.

.. code-block:: text

    (Pdb) b
    Num Type         Disp Enb   Where
    1   breakpoint   keep yes   at pymaze-broken.py:63
            breakpoint already hit 1 time
    2   breakpoint   keep yes   at pymaze-broken.py:82
            breakpoint already hit 7 times
    3   breakpoint   keep yes   at pymaze-broken.py:58
            breakpoint already hit 5 times
    (Pdb) cl 1
    Deleted breakpoint 1 at pymaze-broken.py:63
    (Pdb) cl 2
    Deleted breakpoint 1 at pymaze-broken.py:82
    (Pdb) cl 3
    Deleted breakpoint 3 at pymaze-broken.py:58

We need to get the character to the final position before the exit,
then we add that breakpoint. We know we can do this because the application
pauses for our input anyway.

Once the character is where we need it, press ``^C`` to switch input
from the application back to ``pdb``, then press ``enter`` once. This lets us issue commands to
``pdb`` again.

Add the breakpoint back to line 82, continue execution, and move the player
onto the exit.

.. code-block:: text

    Enter your move (WASD): s
    ##########
    #        #
    #     *  #
    #        #
    #        #
    #*       #
    #    *   #
    #       P#
    #       E#
    ##########
    Enter your move (WASD):
    Program interrupted. (Use 'cont' to resume).

    > pymaze-broken.py(67)main()
    -> direction = input("Enter your move (WASD): ").upper()
    (Pdb) b 82
    Breakpoint 5 at pymaze-broken.py:82
    (Pdb) c
    Invalid move! Use WASD.
    ##########
    #      * #
    #        #
    #        #
    #        #
    #        #
    # *      #
    #       P#
    #       E#
    ##########
    Enter your move (WASD): s
    > pymaze-broken.py(82)main()
    -> player_pos = find_player(maze)

Let's check ``player_pos``.

.. code-block:: text

    (Pdb) n
    > pymaze-broken.py(83)main()
    -> if maze[player_pos[0]][player_pos[1]] == EXIT:
    (Pdb) player_pos
    (8, 8)

Is that right?

.. code-block:: text

    (Pdb) pp maze
    [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
     ['#', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' ', '#'],
     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
     ['#', ' ', '*', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'P', '#'],
     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

It is ... but the ``E`` has been replaced with ``P``! In fact,
where we expected to check whether the player was on the exit,
it turns out we've been checking whether the player position
is ``P`` this whole time, which it always is!

.. code-block:: text

    (Pdb) maze[player_pos[0]][player_pos[1]]
    'P'

So that's our error - we always check the character at the current
player position after the player has moved, which means it is always
``P``, and therefore never ``E``.

My Solution
^^^^^^^^^^^

.. scrollable::

    .. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-working.py
       :language: python
       :linenos:
       :caption: :download:`pymaze-working.py <../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-working.py>`

My solution checks the player's position against the known exit position,
rather than the `characters` at those positions.

This means we set up a variable to hold that position.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-working.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 14

Which we use to replace line 29 in the broken code to set up the maze.
This reduces code duplication and eases future maintenance.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-working.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 29
   :dedent:

Which is then used to make the final exit condition.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-working.py
   :language: python
   :linenos:
   :lineno-match:
   :lines: 85
   :dedent:

Here is a full diff between the two files.

.. literalinclude:: ../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-working.py
   :language: diff
   :diff: ../_static/files/2025/interview_coding_take_homes_part_2a/pymaze-broken.py


|cta|
|disqus|