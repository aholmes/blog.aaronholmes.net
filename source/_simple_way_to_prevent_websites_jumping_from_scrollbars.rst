Simple Way to Prevent Websites Jumping from Scrollbars
------------------------------------------------------

01 April 2016


A common occurance I see on websites, and a frequent question I see as well regards websites "jumping" when more content loads onto the page and a scrollbar becomes visible in the browser. The solution to this is remarkably easy, but I don't think I've seen many developers mention it.

The trick is simply to make the scrollbar present at all times.

If your site creates a vertical scrollbar, use this CSS:

.. code-block:: css

    .body {
        overflow-y: scroll;
    }

If horizontal, use this CSS:

.. code-block:: css

    .body {
        overflow-x: scroll;
    }

And lastly, if your site creates scrollbars in both directions, you can just use ``overflow``.

*Just be aware that* ``overflow-x`` *and* ``overflow-y`` *may not be supported in your target browsers!*

Update Jan 10th, 2019
^^^^^^^^^^^^^^^^^^^^^

It turns out Mac OS and iOS may hide scrollbars regardless of the ``overflow: scroll`` rule. Check out this fix to override this behavior.

.. tags:: css