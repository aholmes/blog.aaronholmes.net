.. meta::
    :date: 2019-09-19

Displaying response headers and pretty JSON with cURL
=====================================================

|pagedate|

.. tags:: HTTP, Bash, curl, Utility, Productivity, Shell

The Problem
-----------

I tend toward using cURL when testing HTTP services, but I had a difficult
time parsing the result when these services spit back unformatted JSON
responses. To make my life a little easier, I set out to find a way to bend
cURL to my will.

The Solution
------------

Let's get straight to it. To make cURL display both response headers and
formatted JSON, we need to make cURL send the headers to STDERR, so we can
then send STDOUT to a formatting utility.

We can accomplish this as so.

.. code-block:: bash

    $ curl -s -D "/dev/stderr" -X POST 'http://example.org/some/url' \
           --data-binary @some-file | python -m json.tool  


This will show a nicely formatted response like this.

.. code-block:: shell-session

    HTTP/1.1 500 Internal Server Error  
    Content-Type: application/json; charset=utf-8  
    X-Powered-By: ASP.NET  
    Date: Wed, 18 Sep 2019 22:39:24 GMT  
    Content-Length: 114

    {
        "Status": 3,
        "Timestamp": "2019-09-18T22:39:24.1659165Z",
        "Error": {
            "Code": 1,
            "Message": "An error has occurred."
        }
    }


What's Going On Here?
---------------------

Let's break this down a bit.

After some initial research into how to send the HTTP headers to STDERR,
I found `this article <https://akrabat.com/pretty-print-curl-i/>`_ that demonstrated
the use of ``-D "/dev/stderr"``.

Breaking the command down:

* ``-s`` will silence the statistics output of cURL
* ``-D "/dev/stderr"`` will send the HTTP headers to STDERR
* ``python -m json.tool`` receives STDOUT, which is the JSON response of my service
* The other options are specific to my service request, and are not relevant to the formatting

**Note:** you can also pipe the cURL output to a utility like `jq <https://stedolan.github.io/jq/>`_,
I just happen to use `python -m json.tool <https://docs.python.org/3/library/json.html>`_.


A Step Further
--------------

These commands and then be turned into Bash aliases and functions.

I have this in my ``~/.bashrc``.

.. code-block:: bash

    alias curl-json='curl -s -D "/dev/stderr"'  
    curl-json-format()  
    {
            curl-json "$@" | python -m json.tool
    }


Now I can use this command!

.. code-block:: bash

    $ curl-json-format -X POST 'http://example.org/some/url' \
          --data-binary @some-file | python -m json.tool  

|cta|
|disqus|