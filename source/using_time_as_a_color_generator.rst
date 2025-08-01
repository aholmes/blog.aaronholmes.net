.. meta::
    :date: 2014-12-20

Using Time as a Color Generator
===============================

.. pagedate::

.. raw:: html

    <script>  
    window.addEventListener('load', function()  
    {
        var rgbs =
        [
            [$('#red'),24,'rgb(#,0,0)'],
            [$('#green'),60,'rgb(0,#,0)'],
            [$('#blue'),60,'rgb(0,0,#)']
        ];

        for(var j=0;j<3;j++)
        {
            var target=rgbs[j % rgbs.length];
            for(var i=0;i<target[1];i++)
            {
                target[0].append($('<div/>').css(
                {
                    display:'inline-block',
                    width:'10px',
                    height:'30px',
                    'margin-left':'-1px',
                    'background-color':target[2].replace('#',i)
                }));
            }
        }
    });
    </script>  

    <script>  
    window.addEventListener('load', function()  
    {
        var rgbs =
        [
            [$('#red2'),24,'rgb(#,0,0)'],
            [$('#green2'),60,'rgb(0,#,0)'],
            [$('#blue2'),60,'rgb(0,0,#)']
        ];

        for(var j=0;j<3;j++)
        {
            var target=rgbs[j % rgbs.length];
            for(var i=0;i<target[1];i++)
            {
                target[0].append($('<div/>').css(
                {
                    display:'inline-block',
                    width:'10px',
                    height:'30px',
                    'margin-left':'-1px',
                    'background-color':target[2].replace('#',i.toString().replace(/^(\d)$/, '0$1').split('').reverse().join(''))
                }));
            }
        }
    });
    </script> 

The idea
--------

I saw the site `What colour is it? <about:blank?site-is-defunct>`_ and thought the concept was really cool. For whatever reason, visualization generators pique my interest. I wanted to alter the original to see a wider range of colors, and to play with the ``attr()`` function in CSS' ``::after`` psuedo-element. I also wanted to add a slider just to allow the user to tweak the generated color.

.. raw:: html

    <p class="codepen" data-height="300" data-default-tab="result" data-slug-hash="zxBJMg" data-pen-title="Time color" data-user="aholmes" style="height: 300px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; border: 2px solid; margin: 1em 0; padding: 1em;">
      <span>See the Pen <a href="https://codepen.io/aholmes/pen/zxBJMg">
      Time color</a> by Aaron Holmes (<a href="https://codepen.io/aholmes">@aholmes</a>)
      on <a href="https://codepen.io">CodePen</a>.</span>
    </p>
    <script async src="https://public.codepenassets.com/embed/index.js"></script>

The HTML and CSS
----------------


First set the attribute on your element. I decided to call it ``data-text``.

.. code-block:: html

   <h1 id="time" data-text="00 : 00 : 00"></h1> 

We only need two lines of CSS to get the attribute function to display.

.. code-block:: css

    h1::after  
    {
      display:block;
      content:attr(data-text);
    }


Normally the ``content`` attribute is set to a static string, but there's also the ``attr()`` function that let's you use an attribute value on your element instead.

You can find more information about ``attr()`` on `MDN <https://developer.mozilla.org/en-US/docs/Web/CSS/attr>`_.

**NOTE**: Browser compatibility is sketchy at best. There are some gotchas to be careful of too.

Updating the content with JavaScript
------------------------------------

There are no DOM API methods that let us access ``::after`` or ``::before`` psuedo-elements with JavaScript. We can at least use the ``attr()`` function in conjunction with the ``setAttribute()`` method or ``dataset`` property to change the content of the psuedo-elements.

With the HTML element above, here's how we can change the value of the ``data-text`` attribute. This change will then be rendered with our CSS rules to display new text in the psuedo-element.

.. code-block:: javascript

    var timeHeader = document.getElementById('time');

    var time = "15:30:25";

    if (timeHeader.dataset !== undefined)  
    {
        timeHeader.dataset.text = time;
    }
    else  
    {
        timeHeader.setAttribute('data-text', time);
    }


Theoretically that should be all we need! With a little more code to set the correct time value on a loop, the site will show a new time every second.

A repaint issue on Chrome version 39.0.2171.95
----------------------------------------------

My experiment didn’t go perfectly. I discovered that changing the attribute value does *not* always trigger a repaint, and thus the new time would not display. I have not figured out exactly what caused this; it was sporadic, and I wonder if it’s partly related to how CodePen works.

Thankfully there’s an easy way to trigger a repaint. It’s not exactly the prettiest solution, but it does ensure the new time is displayed each second.

.. code-block:: javascript

    timeHeader.style.display='none';  
    timeHeader.offsetHeight;  
    timeHeader.style.display='';  


A little extra
--------------

The original code uses the time values as the hexidecimal values for the background color. A time of 9 hours, 23 minutes, and 40 seconds give you the hex color ``#092340``.
Given that this will increment the 0th digit for each red, green, and blue hex value, we end up with a similar color for each second, minute, and hour.

If the time value is 09 23 40, then our RGB values are as follows.

.. list-table::
  :header-rows: 1

  * -
    - Hex
    - Dec
    - Conversion
  * - **Red**
    - 0x09
    - 9
    - (0 × 16¹) + (9 × 16⁰)
  * - **Green**
    - 0x23
    - 35
    - (2 × 16¹) + (3 × 16⁰)
  * - **Blue**
    - 0x40
    - 64
    - (4 × 16¹) + (0 × 16⁰)


After 1 second, blue becomes 65, then 66, 67, 68, and so on. This is a very slow increase!

Additionally, because there are only 24 hours in a day, 60 minutes to an hour, and 60 seconds to a minute, our scale of colors is limited. Red ranges from 0 - 23, green 0 - 59, and blue 0 - 59.

Here's a visualization of all possible red, green, and blue values individually.

.. raw:: html

    <div id="red"></div>  
    <div id="green"></div>  
    <div id="blue"></div>

To get a wider range of colors, each hexidecimal string value can be flipped. For example, 9 is "09" as a string, and "90" flipped. Here's what our example above looks like with the values flipped.

.. list-table::
  :header-rows: 1

  * -
    - Hex
    - Dec
    - Flipped String
  * - **Red**
    - 0x09
    - 9
    - 90
  * - **Green**
    - 0x23
    - 35
    - 53
  * - **Blue**
    - 0x40
    - 64
    - 46

And here's the range of colors and the pattern in which they occur.

.. raw:: html
   
    <div id="red2"></div>  
    <div id="green2"></div>  
    <div id="blue2"></div>

.. tags:: JavaScript, CSS, Codepen, Fiddle, Experimental
