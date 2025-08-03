.. meta::
    :date: 2016-02-09

Two short ack filetype definitions for TypeScript
=================================================

|pagedate|

.. tags:: ack, TypeScript

I search my TypeScript code a lot and finally got tired of using awk, grep, and friends to filter out irrelevant files. Here's a definition for .ts files and .d.ts files to help you out.

::

    --type-set=ts:ext:ts
    --type-set=tsdef:match:/.+\.d\.ts/

Put this in your `.ackrc <https://metacpan.org/pod/ack#Use-the-.ackrc-file>`_ file (or use those switches at the command line).

Now you can search just your .ts files without also searching compiled .js and .d.ts files with ``ack --ts --notsdef mySearch``.

More information `in the ack manpage <http://beyondgrep.com/documentation/ack-2.14-man.html#defining_your_own_types>`_.

|cta|
|disqus|