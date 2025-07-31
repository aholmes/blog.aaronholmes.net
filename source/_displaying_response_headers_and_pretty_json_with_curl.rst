Displaying response headers and pretty JSON with cURL
-----------------------------------------------------

19 September 2019


The Problem
^^^^^^^^^^^

I tend toward using cURL when testing HTTP services, but I had a difficult
time parsing the result when these services spit back unformatted JSON
responses. To make my life a little easier, I set out to find a way to bend
cURL to my will.

The Solution
^^^^^^^^^^^^

To make cURL display *both* response headers and formatted JSON, we need to
send the headers to **STDERR** and pipe **STDOUT** to a JSON-formatting
utility:

.. code-block:: shell-session

    $ curl -s -D "/dev/stderr" -X POST 'http://example.org/some/url' \
          --data-binary @some-file | python -m json.tool

This prints something like:

.. code-block:: console

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
^^^^^^^^^^^^^^^^^^^^^

After some research I found an article demonstrating the use of
``-D "/dev/stderr"``.

* ``-s`` silences cURL’s transfer statistics.  
* ``-D "/dev/stderr"`` writes the HTTP headers to **STDERR**.  
* ``python -m json.tool`` consumes **STDOUT**, which is the service’s JSON
  response.  
* The remaining flags are specific to your request and irrelevant to the
  formatting.

Note: you can also pipe the output to a tool like `jq
<https://stedolan.github.io/jq/>`_; I simply prefer
`python -m json.tool <https://docs.python.org/3/library/json.html#json.tool>`_.

A Step Further
^^^^^^^^^^^^^^

You can turn these commands into handy Bash aliases and functions.  
Add this to your ``~/.bashrc``:

.. code-block:: shell-session

    $ alias curl-json='curl -s -D "/dev/stderr"'
    $ curl-json-format() {
          curl-json "$@" | python -m json.tool
      }

Now you can simply run:

.. code-block:: shell-session

    $ curl-json-format -X POST 'http://example.org/some/url' \
          --data-binary @some-file | python -m json.tool

.. tags:: http, bash, curl, utility, productivity, shell