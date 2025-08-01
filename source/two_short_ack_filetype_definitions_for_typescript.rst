.. meta::
    :date: 2016-02-09

Two short ack filetype definitions for TypeScript
=================================================

.. pagedate::

I search my TypeScript code a lot and finally got tired of using awk, grep, and friends to filter out irrelevant files. Here's a definition for ``.ts`` files and ``.d.ts`` files to help you out.

Put this in your ``.ackrc`` file (or use those switches at the command line).

Now you can search just your ``.ts`` files without also searching compiled ``.js`` and ``.d.ts`` files with::

    ack --ts --notsdef mySearch

More information in the ack manpage.

.. code-block::

    --type-set=ts:ext:ts
    --type-set=tsdef:match:/.+\.d\.ts/

.. tags:: ack, typescript