.. meta::
    :date: 2025-08-03

Interview Coding Take-Homes: Part 1
===================================

|pagedate|

.. tags:: Programming, Software, Interviewing

As software engineers, we are frequently asked to demonstrate our ability to
architect and implement software. Sometimes this is done through algorithm and
data structure live-coding interviews, sometimes through take-home assignments,
often both, or through other means.

I have been given a number of take-home assignments, which I usually focus on
polishing and treating like production-grade software (within reason).
The downside of this focus is the energy it can take - which is compounded
when actively looking for new work.

To that end, I would like to showcase my past take-homes, which demonstrate
my ability to architect and write software.

UCLA Health - Data Corruption
-----------------------------

This take-home was for a Senior Software Engineer position in a research lab
at UCLA Health. You can find the full repository `here <https://github.com/aholmes/2020-InterviewRound3>`_.

Prompt
------

This is the prompt provided by UCLA Health.

.. pull-quote::
   
    Your local grocery store, Half Foods, have been encountering issues with
    their system and needs you to help process some of their data. Every time
    a customer makes a purchase, a text file is generated, containing the
    barcodes of each product they bought as well as other information. A
    sample file CustomerG.txt is as follows:

::

    01232020Jamie
    BEVGTTKYGDGJHGTFBNGDVZJGDIPXVS
    CANFDNSKAVOUXSCGSYBHQYHNMDQOBL
    FRZNQQNPSESCHIMIXOUHNAWLXRZEPT
    BEVGZYUFGNIHDCZIPWLZJLPDSGNEAH

.. pull-quote::

    The first line includes the date (MMDDYYYY) as well as the customer
    information. Each line following that is an item barcode, in no particular
    order.

    The barcode can be broken down into these components:

::

    [Product Type][Subtype][Unique ID]	
    [BEVG][TTKYGD][GJHGTFBNGDVZJGDIPXVS]

.. pull-quote::

    The product type is always 4 letters long, the subtype is 6 letters long, and
    the unique id is 20 letters long.

    You are also provided a product type key:
    BEVG - Beverages
    BAKE - Baked Goods
    CANF - Canned Foods
    CNSB - Condiments/Spices/Baking
    SNCN - Snacks/Candy
    DREG - Dairy/Eggs
    FRZN - Frozen Foods
    FRVG - Fruits/Vegetables
    GRPA - Grains/Pastas
    MTSF - Meat/Seafood
    MISC – Misc


My Approach to the Code
-----------------------

This application is a .NET Core Console application written in C#.

Structure
^^^^^^^^^

The domain code is organized per `Domain-Driven Design <https://en.wikipedia.org/wiki/Domain-driven_design>`_
(DDD) principles and guidelines.

Business logic is shared between the DDD classes and a set of classes I've
named ``ConsoleWriter``\ s.

Domain
~~~~~~

The domain of the application is broken down as follows.

Aggregates
~~~~~~~~~~

An Aggregate called ``PurchaseAggregate`` is responsible for processing
questions about a set of Purchases (a ``PurchaseEntity``) in a file.  
For example, this Aggregate can return the most common Product purchases in a
file.

Entities
~~~~~~~~

An Entity called ``PurchaseEntity`` contains information on the Purchase,
representing the entire Purchase file.

* This Entity holds the Purchase date, Customer name, and the three parts of a
  Product entry in a file.
* This Entity is able to construct itself from a file. It parses this file and
  sets the appropriate properties.
* No instance methods exist on this Entity.

A Purchase is considered an Entity because every Purchase is unique regardless
of the data contained within that Purchase. For example—however unlikely it
may be—two Customers with the same name may buy the exact same Products at the
same time as another Customer.

Values
~~~~~~

A Value type exists for each of the following:

* Barcode (``BarcodeValue``)
* Customer (``CustomerValue``)
* Product ID (``ProductIdValue``)
* Product Type (``ProductTypeValue``)
* Product Subtype (``ProductSubtypeValue``)
* Timestamp (``TimestampValue``)

These are considered Value types because, in relation to a Purchase, each Value
is equivalent based on its properties. For example, a Product ID of ``"BEVG"``
represents a Product ID of ``"BEVG"`` regardless of how many ``"BEVG"`` entries
there are for a Purchase.

Review `classStructure.puml </_static/files/2025/interview_coding_take_homes_part_1/classStructure.puml>`__ to understand the relations
between these types.

.. image:: /_static/images/2025/interview_coding_take_homes_part_1/classStructure.svg
   :target: /_static/images/2025/interview_coding_take_homes_part_1/classStructure.svg

With the exception of ``BarcodeValue``, these Value types extend
``ValueBase<T>``. This is done to manage the code that determines equality
between instances of Value types.

Each Value type overrides the default ``==`` and ``!=`` operators in order to
equate their values *by value* rather than each instance *by reference*.

Each Value type implements implicit cast methods between ``string``  
(except for ``TimestampValue`` whose ``T`` type is ``DateTime``) simply for
ease of use in treating these value types as strings.

Business logic
^^^^^^^^^^^^^^

The business logic for this application is primarily contained within
``Program.cs`` (``Main``), the ``PurchaseAggregate``, and the ``PurchaseEntity``
classes. The code is documented and should be reviewed for further
clarification.

Some of the business logic is non-Domain and is thus managed outside the DDD
guidelines. In this case, the output of information about purchases is handled
in classes that I've named ``ConsoleWriter``\ s.

These classes work using the `Visitor Pattern <https://en.wikipedia.org/wiki/Visitor_pattern>`_.

In this design, the Visitor visits a writer that handles unique output for each
of the ``PurchaseAggregate`` and ``PurchaseEntity`` types. The output of these
Dispatchers is returned and written to the console by the Visitor.

Searching
^^^^^^^^^

In order to handle corrupted Purchase Type data, a BK Tree is implemented to
discover the closest-matching Product Type when inputting data, or when
outputting Product Subtypes for a Product Type.

References used:

* https://en.wikipedia.org/wiki/Levenshtein_distance
* https://www.csharpstar.com/csharp-string-distance-algorithm
* https://www.geeksforgeeks.org/bk-tree-introduction-implementation/
* http://blog.notdot.net/2007/4/Damn-Cool-Algorithms-Part-1-BK-Trees
* https://nullwords.wordpress.com/2013/03/13/the-bk-tree-a-data-structure-for-spell-checking/

Other Considerations
^^^^^^^^^^^^^^^^^^^^

As much as possible, this code was written to be easily unit-testable.  
Accordingly, the `Wrapper Pattern <https://en.wikipedia.org/wiki/Adapter_pattern>`_
is employed to avoid using the static ``Console`` class directly.

Unit Tests
^^^^^^^^^^

The application is thoroughly unit tested. The tests run on the *xUnit*
testing framework for .NET and C#.


Scenarios
---------

The prompt included several questions I needed to answer.

Question 1
^^^^^^^^^^


.. pull-quote::
    
    Write a program that takes any customer text file, and prints the
    following information to the console:

    a)	Name of the customer
    b)	Formatted date of purchase
    c)	Total number of items they purchased

Here is an example of the expected output, from my application.

::

    Question 1 solution:

    a) Customer: Jamie
    b) Date: 1/23/2020 12:00:00 AM
    c) Total Items Purchased: 4
    
Question 2
^^^^^^^^^^

Part 1
~~~~~~

Extend your program so that a grocery store employee can easily access more
detailed information about a purchase given the same customer text file input. It is up to you how you want organize and display this, but you should be able to print the following information:

    a)	For every existing product type, the number and list of unique IDs of
        items purchased by the customer
    b)	The most common product type

Here is an example of the expected output.

::

    Question 2 part 1 solution:

    a) The number of unique items purchased: 4
        The unique IDs that were purchased:
        GJHGTFBNGDVZJGDIPXVS
        OUXSCGSYBHQYHNMDQOBL
        SCHIMIXOUHNAWLXRZEPT
        IHDCZIPWLZJLPDSGNEAH
    b) The most common product type purchased: BEVG

Part 2
~~~~~~

.. pull-quote::

    The employee should also be able to put in a specific product type input,
    and get the following information:

    a)	Subtypes for that product type

    In addition, make sure your design allows for new product types to be
    added in the future, as the grocery store expands its inventory. Create a
    function that can easily add a new product type with its code to the key,
    without affecting your program's functionality.

The application pauses to accept user input.

The expected input is a 4-character Product Type code, e.g., "BEVG," "MISC," etc.

The application will accept one character at a time, showing suggestions for
possible Product Types as the user types.

When the 4th character is entered, the application will display the following
Product Subtype information for the best match of the user's Product Type
input.

If there are no matches, the application will let the user know.

Here is an example of the expected output when the user types "BEVG"

::

    Question 2 part 2 solution:

    Input a 4-character Product Type to list Subtypes in this Purchase.
    Press Enter to stop searching.
     - Possible matches: # this outputs when "B" is typed
            BEVG
            BAKE
            DREG
            CANF
            CNSB
            SNCN
            FRZN
            GRPA
            MISC
            MTSF
            FRVG
     - Possible matches: # this outputs when "E" is typed after the previous "B"
            BEVG
            BAKE
     - Possible matches: # this outputs when "V" is typed after the previous "E"
            BEVG
     - Possible matches: # this outputs when "G" is typed after the previous "V"
            BEVG
     > BEVG

    Searching for best match 'BEVG'

    a) Subtypes for product type BEVG:
        TTKYGD
        ZYUFGN

    Input a 4-character Product Type to list Subtypes in this Purchase.
    Press Enter to stop searching.
     >

Either way, `Part 2`_ will repeat forever until the user presses Enter/Return.

Once this occurs, the application prompts the user to press Enter/Return to exit.

The application is finished after this.

Question 3
^^^^^^^^^^

.. pull-quote::

    A problem arises with the Half Foods database, partially corrupting some
    of the customer purchase data. Luckily, you managed to figure out that
    the data only changed in a consistent way, making it possible to fix.

    The first line of each text file remained the same, but for some of the
    barcodes, a random letter was changed somewhere in product type.
    
    For example:

::

    05242020James
    FRZNQQNPSESCHIMIXOUHNAWLXRZEPT
    BENGTTKYGDGJHGTFBNGDVZJGDIPXVS
    CDNFDNSKAVOUXSCGSYBHQYHNMDQOBL

.. pull-quote::

    Extend your program and modify your answer for Question 2 to account for these errors.

When the application first loads file data, it will ensure correct Product
Type keys are parsed. It will attempt to find the intended Product Type key
with the use of a BK Tree.

When a match is found, or if the Product Type key is already correct, this
Product Type key is imported.

This same functionality is used for `Question 2`_ `Part 2`_, when the user types a
Product Key.

Question 4
^^^^^^^^^^

The repository also contains this `question and answer <https://github.com/aholmes/2020-InterviewRound3/blob/main/docs/THEORY.md>`_.
I've repeated it here for posterity.

.. pull-quote::

    If only some of the files in the customer purchase database are corrupt,
    how would you address this problem going forward? What if the database
    was extremely large? How do you prepare for future data corruptions?
    Write a brief summary of your approach.

Fortunately, I read the entire project requirement before starting. As such,
I started with a unit test that tested these problems, and I developed the
application with these questions in mind. These problems are solved, and the
unit tests now pass.

Let me address each question in order.

.. pull-quote::

    If only some of the files in the customer purchase database are corrupt,
    how would you address this problem going forward?

This concern is moot. The application begins with importing purchase data and
validates against the corrupted data scenario (where Product Types can be
wrong by a single character). This validation does require additional cycles
and memory to complete, but in most cases should not be a problem.

My approach: always validate; never assume the data is correct.

One issue that may arrise is with huge data sets, but in reality, how many
customers will purchase the excessive number of products that would be
necessary to significantly slow down a BK Tree? Taking some measurements,
this list of `370k words <https://raw.githubusercontent.com/dwyl/english-words/7cb484d/words_alpha.txt>`_ is indexed in ~20 seconds, and can search a
worst-case scenario, e.g., "zwitterionic" in ~100ms.

This approach is not a concern across multiple purchases either if the system
can be parallelized. More than one purchase can be analyzed at a time,
reducing the total processing time further.

.. pull-quote::

    What if the database was extremely large?

Generally, I would start with considering what is actually possible or
likely. As I started in the previous question, it is unlikely customers will
purchase an unbelievable number of products. This means the use of an
efficient text searching data structure and algorithm, like a BK Tree, should
never become a bottle neck. Hopefully the bottle neck is I/O (network, disk,
etc).

If we are processing purchase data across many sets of purchases, this could
realistically be problematic. If we were, say, analyzing every purchase made at Amazon for its entire existence, that is a lot of data! In this case, I would rely on parallelization first. Multiple cores, multiple machines, or multiple cloud processing instances can give you the raw resources required to churn through so much data. If this is still insufficient, then it's time to start looking at different algorithms, or perhaps using statistics and probabilities, and whether 100% accurate numbers are needed.

.. pull-quote::

    How do you prepare for future data corruptions?

Future data corruptions are handled the same - the application supports this
from the start. Now, if we are processing data that we have already processed
because it is now corrupt, then we need to devise a mechanism to relate the
corrupted data to the corrected data. In some cases, reprocessing like that
may be best to just start anew.

If we can't do that, having implemented some infrastructure that can help us
manage this data would be a good idea. For example, an SNS topic could be
used to respond immediately to a Product ID change in a purchase, which can
then be validated and reinserted, and you could receive notifications that
data is becoming corrupt and stop it before it gets out of hand.

|cta|
|disqus|