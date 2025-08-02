.. meta::
    :date: 2018-07-26

The Behavior of C# Nested Static Classes
========================================

.. pagedate::

While working on a code review, I found a nested static class that I needed to verify the validity of. I had three questions:

* Does the CLR create new instances when the containing class is instantiated?
* Do the static class members retain the same values across all instances of the containing class?
* Is the nested class truly static?

As you'll read below, it turns out the nesting of a static class is a bit of a red herring. If you write C# regularly, you already know how this works.

Check the Documentation
-----------------------
Like any good dev, I checked the documentation first.

The Microsoft C# docs for `Static Classes and Static Class Members <https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/static-classes-and-static-class-members>`_ states the following.

    As is the case with all class types, the type information for
    a static class is loaded by the .NET Framework common language
    runtime (CLR) when the program that references the class is
    loaded. The program cannot specify exactly when the class is
    loaded. **However, it is guaranteed to be loaded and to have its
    fields initialized and its static constructor called before**
    the class is referenced for the first time in your program.
    **A static constructor is only called one time, and a static
    class remains in memory for the lifetime of the application
    domain** in which your program resides.

This is pretty clear on static class behavior, but I still wasn't sure whether there were additional nuances regarding nested static classes. We can find more information in the documentation regarding `Nested Types <https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/nested-types>`_, however, this documentation is missing any information about static classes.

----

Solving the Unknown
-------------------

With my questions unanswered, and a desire to be certain in my code review, it was time to create a test case. Here's the code I wrote.

By the way, I typically use `RoslynPad <https://roslynpad.net/>`_ for one-off tests like this.

.. code-block:: csharp

    // Foo is the containing/outer class that is instantiated
    public class Foo  
    {
        // OuterI is used to retrieve the value of the integer
        // parameter for the constructor
        public static int OuterI;

        public Foo(int i)
        {
            OuterI = i;
        }

        // BarI returns the value of the nested static
        // class's value, which points to the containing
        // class's OuterI property
        public int BarI => Bar.InnerI;

        // This is the nested static class being tested
        private static class Bar
        {
            // This is used to retrieve the containing class's
            // value of the OuterI property, which is set by
            // an instance of Foo. Keep in mind, this is a value type,
            // not a reference type, and this is a field,
            // not a property.
            public static int InnerI = Foo.OuterI;
        }
    }


I then tested two scenarios.

The first scenario observes what happens when 1+n ``Foo`` s are
instantiated, followed by printing the value of each instance's
``BarI`` property.

.. code-block:: csharp

    var f1 = new Foo(1);  
    var f2 = new Foo(2);  
    var f3 = new Foo(3);  
    var f4 = new Foo(4);

    Console.WriteLine(f1.BarI);  
    Console.WriteLine(f2.BarI);  
    Console.WriteLine(f3.BarI);  
    Console.WriteLine(f4.BarI);  


The second scenario observes what happens when n+1 ``Foo`` s are
instantiated, then immediately followed by printing the value of
the instances ``BarI`` property.

.. code-block:: csharp

    Console.WriteLine(new Foo(1).BarI);
    Console.WriteLine(new Foo(2).BarI);
    Console.WriteLine(new Foo(3).BarI);
    Console.WriteLine(new Foo(4).BarI);

----

A Challenger Appears!
---------------------

**Before reading further**, I'd like to offer you a challenge;
predict what happens in both scenario 1 and 2.

----

The Behavior, Discovered
------------------------

Figured it out?

The output of the first scenario is:

.. code-block:: text

    4
    4
    4
    4

The output of the second scenario is:

.. code-block:: text

    1
    1
    1
    1

While this may be surprising (the first scenario caught me off
guard), the behavior is explained in the `Static Classes and Static Class Members <https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/static-classes-and-static-class-members>`_
documentation. Indeed, this line applies to all static classes.

    A static constructor is only called one time, and a static
    class remains in memory for the lifetime of the application
    domain in which your program resides.

Why Does this Occur?
--------------------

So with that in mind, what's actually happening here? Let's make
a couple changes to observe the application execution in both
scenarios.

Add a static constructor to ``Bar``, and insert a new ``Console.WriteLine``
statement.

.. code-block:: csharp

    private static class Bar  
    {
        static Bar()
        {
            Console.WriteLine("initialized");
        }

        public static int InnerI = Foo.OuterI;
    }


Then, for both scenario 1 and 2, insert new ``Console.WriteLine`` statements
between each operation.

Scenario 1

.. code-block:: csharp

    Console.WriteLine("new 1");
    var f1 = new Foo(1);
    Console.WriteLine("new 2");
    var f2 = new Foo(2);
    Console.WriteLine("new 3");
    var f3 = new Foo(3);
    Console.WriteLine("new 4");
    var f4 = new Foo(4);

    Console.WriteLine("bar 1");
    Console.WriteLine(f1.BarI);
    Console.WriteLine("bar 2");
    Console.WriteLine(f2.BarI);
    Console.WriteLine("bar 3");
    Console.WriteLine(f3.BarI);
    Console.WriteLine("bar 4");
    Console.WriteLine(f4.BarI);

Scenario 2

.. code-block:: csharp

    Console.WriteLine("bar 1");
    Console.WriteLine(new Foo(1).BarI);
    Console.WriteLine("bar 2");
    Console.WriteLine(new Foo(2).BarI);
    Console.WriteLine("bar 3");
    Console.WriteLine(new Foo(3).BarI);
    Console.WriteLine("bar 4");
    Console.WriteLine(new Foo(4).BarI);

Now, if we execute these scenarios, the application execution
flow becomes clear. The reason for the observed behavior is as
stated in the documentation. The static class is set up before
it is accessed, and it is initialized only one time.

Scenario 1 outputs the following:

    | new 1
    | new 2
    | new 3
    | new 4
    | bar 1
    | *initialized (BarI is accessed for the first time, and the static class is initialized)*
    | 4
    | bar 2
    | 4
    | bar 3
    | 4
    | bar 4
    | 4

Scenario 2 outputs the following:

    | bar 1
    | *initialized (BarI is called for the first time, and the static class is initialized)*
    | 1
    | bar 2
    | 1
    | bar 3
    | 1
    | bar 4

Now I am curious what the non-gaurantee of *when* the static class
is initialized means in runtimes other than the CLR.

.. tags:: C#, .NET, Experimental, Documentation
