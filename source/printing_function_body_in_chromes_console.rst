.. meta::
    :date: 2015-07-01

Printing function body in Chrome's console
==========================================

.. pagedate::

Chrome used to, by default, print a function body in the console if you entered a function name into it, or if you called ``console.log()`` with a function name.

What happens now is that Chrome will print a link to the function which, when clicked, will navigate your source viewer to that function.

For example, executing (or logging) ``BLT.TypeScript.Text.truncate`` will print ``function truncate(input, length, ellipsize)``.

For me, navigating away from my source viewer when I want a reference to a function is distracting. I am not aware of a way to re-enable the old behavior, but an alternative is to now call ``toString()`` on the function. Unfortunately, it does not appear that whitespace is preserved.

``BLT.TypeScript.Text.truncate.toString()``

Here is the actual function body:

.. code-block:: javascript

    function truncate(input, length, ellipsize) {
        if (ellipsize === void 0) { ellipsize = true; }
        if (input.length <= length) return input;
        var whitespace = new RegExp('\\s');
        var truncatedStr = input.substr(0, length);
        if (!whitespace.test(truncatedStr)) return truncatedStr + (ellipsize ? ' ...'
        while (length > 0 && !whitespace.test(input.substr(--length, 1))) { }
        return input.substr(0, length) + (ellipsize ? ' ...' : '');
    }

.. tags:: chrome