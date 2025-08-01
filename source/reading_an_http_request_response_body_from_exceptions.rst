.. meta::
    :date: 2015-04-16

Reading an HTTP Request Response Body from Exceptions
=====================================================

.. pagedate::

Every so often I need to read the response body of a failed HTTP request while debugging a .NET application in Visual Studio. It's not immediately obvious how you can do this, so here's a quick way to do so. You can use these same methods when working directly with an HTTP response object or an HTTP request object as well.

1) Open the Immediate Window under Debug > Windows > Immediate, or by pressing ``CTRL + ALT + I``.

2) You'll need to cast your exception to a ``WebException``. Try either of these, depending on what kind of exception you're working with:

.. code-block:: csharp

    var s=(e.InnerException as System.Net.WebException).Response.GetResponseStream();
    

::

        {System.Net.SyncMemoryStream}
             [System.Net.SyncMemoryStream]: {System.Net.SyncMemoryStream}
            base: {System.Net.SyncMemoryStream}
            CanRead: true
            CanSeek: true
            CanTimeout: true
            CanWrite: true
            Length: 78
            Position: 0
            ReadTimeout: -1
            WriteTimeout: -1

Still no luck? Look in the Locals window and see if you can find the correct exception that has the HTTP response object in it. You'll know you have the right one when the Immediate Window prints something other than ``null``. For example:

3) Now you can get the response stream from the WebException:

.. code-block:: csharp

    var s = (e.InnerException as System.Net.WebException).Response.GetResponseStream();

::

    {System.IO.StreamReader}
        base: {System.IO.StreamReader}
        BaseStream: {System.Net.SyncMemoryStream}
        CurrentEncoding: {System.Text.UTF8Encoding}
        EndOfStream: false


4) Create a new ``StreamReader`` object just for ease of use:

.. code-block:: csharp

    var sr = new System.IO.StreamReader(s);

5) Finally, read the stream contents. This is the HTTP response body:

.. code-block:: csharp

    sr.ReadToEnd();

::

    "{\"Message\":\"The index 'products' for service 'search' was not found.\"}"

.. tags:: c#, .net, http, debugging