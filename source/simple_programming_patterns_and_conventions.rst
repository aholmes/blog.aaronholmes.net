.. meta::
    :date: 2015-12-24

Simple programming patterns and conventions
===========================================

|pagedate|

.. tags:: Patterns, Conventions, Programming

I thought it might be helpful to some developers to see some simple patterns and conventions in a variety of languages. Many of us know about more complex and abstract patterns, like the `Abstract Factory Pattern <https://en.wikipedia.org/wiki/Abstract_factory_pattern>`_ or the `Flyweight Pattern <https://en.wikipedia.org/wiki/Flyweight_pattern>`_, but smaller patterns are rarely discussed outside of answers to questions.

These are some patterns and conventions that I tend to use in any code I write. They range from one-liners to a couple of methods, and are mostly understandable at first glance. I've avoided going too much into why someone might choose any given pattern, and leave it as an exercise to the reader to determine where these patterns might be useful for them.

As of now, I've only listed a single convention because I use it in a number of the patterns below. I'm sure the convention is controversial, so if you don't agree with it, please keep in mind that the meat of this post is in the patterns.

I will add other conventions and patterns in the future, and may add others from comments here or on reddit.

A final note on the code below. I did not enclose all code in the required class or method blocks in order to keep the focus on the patterns alone. Additionally, I've specified the language that each example is written for; many of them work just fine in other languages. If you have any questions on why a pattern doesn't make sense, or is not executing, don't hesitate to ask.

Enjoy!

Conventions
-----------

Branching flow-control statements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For branching flow-control statements, do not use braces and keep the code on a single line.

Return statements
^^^^^^^^^^^^^^^^^

**Language**: C#, most C-like languages with some contingencies

.. code-block:: csharp

    if (MyBoolean) return null;  

Continuing in a loop
--------------------

**Language**: C#, most C-like languages

Breaking out of a loop
^^^^^^^^^^^^^^^^^^^^^^

**Language**: C#, most C-like languages

----

Patterns
--------


Prevent a method from executing more than once
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is an easy way to prevent a method from executing multiple times. By checking a condition at the beginning, and then ensuring that condition is true immediately after, any subsequent calls will return immediately.

**Language**: C#, Java with some contingencies

.. code-block:: csharp

    static boolean executed;  
    static void MyFoo()  
    {
        if (executed) return null; // simply check the condition before any other code
        executed = true; // then assign your variable
        /* ... */
    }

Using a ``switch`` statement as a compact alternative to if statements
----------------------------------------------------------------------

**Language**: JavaScript

.. code-block:: javascript

    switch(true)  
    {
        case myFoo === myBar: FooBar(); break; // while the next statement is false if this is true, the additional check is avoided with the `break` statement
        case myFoo === myBaz: FooBaz(); break;
        default: DefaultMethod();
    }

Execute multiple ``using`` blocks without braces
------------------------------------------------

Like any other block statement, in C#, ``using`` can be used without braces as well. This is especially useful to avoid excessive visual nesting.

**Language**: C#

.. code-block:: csharp

    using(var myDisposableObject = new Disposable())  
    using(var myFoo = new Foo())  
    using(var myBar = new Bar())  
    {
        // Each of myDisposableObject, myFoo, and mBar are accessible here
        /* ... */
    }

Avoid unnecessary awaits by passing the ``Task`` around
-------------------------------------------------------

At least for me, using ``async`` / ``await`` in C# seemed to require making your methods that called asynchronous methods async themselves, and making those methods await. Instead, if your method does not need to await, you can make it return a ``Task`` and then pass the task returned from an asynchronous method wherever you need it. This is especially helpful if you need to use ``out`` or ``ref`` in a method that calls an asynchronous method.

**Language**: C#

.. code-block:: csharp

    static void Main()  
    {
        MySyncMethod().Wait();
    }

    static async Task MyAsyncMethod()  
    {
        Console.WriteLine("Waiting 1 second @ " + DateTime.UtcNow);
        await Task.Delay(1000); // here we await the result so we can execute code immediately after, usually to operate on the result of the Task
        Console.WriteLine("Finished waiting @ " + DateTime.UtcNow);
    }

    static Task MySyncMethod()  
    {
        Console.WriteLine("Calling asynchronous method");
        return MyAsyncMethod(); // MySyncMethod doesn't need to execute code immediately after, so it is synchronous and only returns the Task
    }

Prevent a method call with a specific type during compile time
--------------------------------------------------------------

I happened across this solution when clicking around Stack Overflow. Apologies for not crediting the solution; I don't recall where I found it.

You may have a method that accepts an abstract class, an interface, or some form of "base" class, but you want to restrict a certain subclass of that type from being used (perhaps the subclass is obsolete). Rather than checking the type during runtime and throwing an exception, you use this pattern to gain a compile time check in addition to a runtime check. This example uses constructors, but it works for methods as well.

By default, the Obsolete annotation will display a warning. You can configure msbuild or Visual Studio to treat warnings as errors, which will prevent the following code from compiling.

**Language**: C#

.. code-block:: csharp

    public interface IBar {}

    public class Bar: IBar {}  
    public class Baz: IBar {}

    public class Foo  
    {
        public Foo(IBar bar)
        {
        }

        [Obsolete("Foo cannot be instantiated with a Baz.")]
        public Foo(Baz baz) // overload the IBar constructor with the type that is disallowed
        {
            throw new NotImplementedException();
        }
    }

    public class Program  
    {
        public static void Main()
        {
            new Foo(new Bar());
            new Foo(new Baz()); // this generates a warning during compile time, and an exception during runtime
        }
    }

Define and declare the type of arrays and objects in TypeScript
---------------------------------------------------------------

I think this is a problem and solution unique to TypeScript. You need to define a variable as an array or an object, but either you've disallowed implicity any, or you need to declare the type of the variable. There are, of course, other ways to accomplish this, but I believe this is the most compact way.

**Language**: TypeScript

.. code-block:: typescript

    var myFoos = <Foo[]>[]; // here we simply cast the array to the specific type needed
    var myFood = <Foo>{}; // the same pattern is used for objects as well  

Execute multiple async tasks in parallel
----------------------------------------

You may need to execute a series of asynchronous tasks in parallel, and then await their result. There are a couple different ways I accomplish this, depending on how the tasks are created. You can use the pattern *Avoid unnecessary awaits by passing the ``Task`` around* here as well.

**Language**: C#

.. code-block:: csharp

    static async Task MyFirstMethod()  
    {
        var tasks = new List<Task>(); // here we use a List<Task> in order to optionally add tasks to await

        tasks.Add(Task.Delay(1000));

        if (aCondition) // if aCondition is true, two tasks are added to the list
        {
            tasks.Add(Task.Delay(1000));
            tasks.Add(Task.Delay(1000));
        }

        Console.WriteLine(DateTime.UtcNow);
        await Task.WhenAll(tasks); // this method will complete after 1 second, when all three tasks are completed
        Console.WriteLine(DateTime.UtcNow);
    }

    static async Task MySecondMethod()  
    {
        var tasks = new[] // here an array is initialized because there is no need to conditionally add more tasks
        {
            Task.Delay(1000),
            Task.Delay(1000),
            Task.Delay(1000)
        };

        Console.WriteLine(DateTime.UtcNow);
        await Task.WhenAll(tasks);
        Console.WriteLine(DateTime.UtcNow);
    }


|cta|
|disqus|