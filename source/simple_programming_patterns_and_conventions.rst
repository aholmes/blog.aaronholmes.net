.. meta::
    :date: 2015-12-24

Simple programming patterns and conventions
===========================================

.. pagedate::

I thought it might be helpful to some developers to see some simple patterns and conventions in a variety of languages. Many of us know about more complex and abstract patterns, like the Abstract Factory Pattern or the Flyweight Pattern, but smaller patterns are rarely discussed outside of answers to questions.

These are some patterns and conventions that I tend to use in any code I write. They range from one-liners to a couple of methods, and are mostly understandable at first glance. I've avoided going too much into why someone might choose any given pattern, and leave it as an exercise to the reader to determine where these patterns might be useful for them.

As of now, I've only listed a single convention because I use it in a number of the patterns below.

Conventions
------------

**Branching flow-control statements**

Do not use braces and keep the code on a single line.

**Return statements**

*Language: C#, most C-like languages with some contingencies*

.. code-block:: csharp

    if (MyBoolean) return null;

**Continuing in a loop**

*Language: C#, most C-like languages*

.. code-block:: csharp

    for(var i = 0; i < 5; i++)
        if (i == 4) continue;

**Breaking out of a loop**

*Language: C#, most C-like languages*

.. code-block:: csharp

    var i = 0;
    while(true)
    {
        if (i == 4) break;
        i++;
    }

Patterns
---------

**Prevent a method from executing more than once**

*Language: C#, Java with some contingencies*

.. code-block:: java

    static boolean executed;
    static void MyFoo()
    {
        if (executed) return null;
        executed = true;
        /* ... */
    }

**Using a switch statement as a compact alternative to if statements**

*Language: JavaScript*

.. code-block:: javascript

    switch(true) {
        case myFoo === myBar: FooBar(); break;
        case myFoo === myBaz: FooBaz(); break;
        default: DefaultMethod();
    }

**Execute multiple using blocks without braces**

*Language: C#*

.. code-block:: csharp

    using(var myDisposableObject = new Disposable())
    using(var myFoo = new Foo())
    using(var myBar = new Bar())
    {
        /* ... */
    }

**Avoid unnecessary awaits by passing the Task around**

*Language: C#*

.. code-block:: csharp

    static void Main()
    {
        MySyncMethod().Wait();
    }

    static async Task MyAsyncMethod()
    {
        Console.WriteLine("Waiting 1 second @ " + DateTime.UtcNow);
        await Task.Delay(1000);
        Console.WriteLine("Finished waiting @ " + DateTime.UtcNow);
    }

    static Task MySyncMethod()
    {
        Console.WriteLine("Calling asynchronous method");
        return MyAsyncMethod();
    }

**Prevent a method call with a specific type during compile time**

*Language: C#*

.. code-block:: csharp

    public interface IBar {}
    public class Bar: IBar {}
    public class Baz: IBar {}

    public class Foo
    {
        public Foo(IBar bar) {}

        [Obsolete("Foo cannot be instantiated with a Baz.")]
        public Foo(Baz baz)
        {
            throw new NotImplementedException();
        }
    }

**Define and declare the type of arrays and objects in TypeScript**

*Language: TypeScript*

.. code-block:: typescript

    var myFoos = <Foo[]>[];
    var myFood = <Foo>{};

**Execute multiple async tasks in parallel**

*Language: C#*

.. code-block:: csharp

    static async Task MyFirstMethod()
    {
        var tasks = new List<Task>();
        tasks.Add(Task.Delay(1000));

        if (aCondition)
        {
            tasks.Add(Task.Delay(1000));
            tasks.Add(Task.Delay(1000));
        }

        Console.WriteLine(DateTime.UtcNow);
        await Task.WhenAll(tasks);
        Console.WriteLine(DateTime.UtcNow);
    }

.. tags:: patterns, conventions, programming