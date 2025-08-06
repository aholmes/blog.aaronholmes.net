.. meta::
    :date: 2014-11-28

JavaScript Vector Animations with Divs or Canvas
================================================

|pagedate|

.. tags:: JavaScript, Canvas, Pixi.js, Animation, Codepen, GitHub, Fiddle

.. raw:: html

    <p class="codepen" data-height="300" data-default-tab="result" data-slug-hash="jOdYeb" data-pen-title="Vector Animations" data-user="aholmes" style="height: 300px; box-sizing: border-box; display: flex; align-items: center; justify-content: center; border: 2px solid; margin: 1em 0; padding: 1em;">
      <span>See the Pen <a href="https://codepen.io/aholmes/pen/jOdYeb">
      Vector Animations</a> by Aaron Holmes (<a href="https://codepen.io/aholmes">@aholmes</a>)
      on <a href="https://codepen.io">CodePen</a>.</span>
    </p>
    <script async src="https://public.codepenassets.com/embed/index.js"></script>
    
What's this all about?
----------------------

A few months ago I found the post `Vector animations with Python <http://zulko.github.io/blog/2014/09/20/vector-animations-with-python/>`_. I thought the presented demos were very cool, and the code interesting, but I was disappointed with the lack of interactivity. You can't very well change a GIF while you're watching it!

Because of that, I was inspired to recreate the `first example <https://imgur.com/inspired-by-dave-whyte-animation-6rx7SUz>`_. I started with rendering the animation with a bunch of ``<div>`` elements, and then I moved onto to rendering the animation with in a ``<canvas>`` element using `Pixi.js <http://www.pixijs.com/>`_. You can play with the codepen above to alter the animation's look and behavior.

The HTML
--------

I wanted to keep the HTML for this demo simple. A single ``<div>`` exists on the page which acts as the container for either the ``<canvas>`` element, or the list of ``<div>`` elements. Some HTML exists to handle the options dialog as well.

.. code-block:: html

    <!-- This block is for the options dialog. -->  
    <div id="options">  
        <a href="" id="hide-options">Hide Options</a>
        <label><input type="checkbox" name="opacity"/> Opacity</label>
        <label><input type="checkbox" name="inverse"/> Inverse</label>
        <label><input type="checkbox" name="reverse"/> Reverse</label>
        <label><input type="checkbox" name="chill"/> Chill</label>
        <label><input type="checkbox" name="running" checked="checked"/> Running</label>
        <label><input type="text" name="colorbg" value="#FFFFFF"> BG color</label>
        <label><input type="text" name="colorborder" value="#000000"> Border color</label>
        <label><input type="range" step="10" min="0" max="800" value="400" name="width"> Width</label>
        <label><input type="range" step="1" min="-60" max="60" value="20" name="fps"> FPS</label>
        <button name="reset">Reset</button>
        <button name="fullscreen">Fullscreen</button>
    </div>  
    <div id="toggle-options"><a href="" id="show-options">Show Options</a></div>

    <!-- This is the container for the animation. It's really all we need. -->  
    <div class="container" id="container"></div>  

Accomplishing this with ``<div>``
---------------------------------

My first approach with this was to render the animations with a bunch of div elements. I used JavaScript to recalculate their positions relative to their container on each "tick" (using ``requestAnimFrame()``).

Application loop
^^^^^^^^^^^^^^^^

The script has a main application loop that is a function called run(). Because this is JavaScript, we can't use a real while loop, or the browser would never repaint anything.

.. code-block:: javascript

    /**
     * Start the application loop.
     * @param {Function} make_frame The method returned from bootstrap().
     */
    function run()  
    {
        run.t = run.t || 0;

        var frame = run.t / runOptions.fps;
        if (run.t === runOptions.frameRate)
        {
            run.t = 0;
        }

        run.make_frame(frame);

        // continue painting new frames when not running, but don't animate the disks
        // this way, chill mode, with, and opacity can be changed when the frames are "still."
        if (diskOptions.running)
        {
            run.t++;
        }

        requestAnimFrame(run);
    }

    run.make_frame = makeFrameMethod;  

The animation is bootstrapped at the very end with ``run()``.

This same method is used by both the ``<div>`` and ``<canvas>`` approach. We run ``run.make_frame = makeFrameMethod;`` to generate the method we need to use based on the "mode" option, which is either "dom" or "canvas".

Bootstrapping the ``<div>`` rendering method
--------------------------------------------

Okay, here's the fun part. ``makeFrameMethod`` does two things when running in "dom" mode.

First, we set up some run-time parameters. These parameters are used in "canvas" mode as well.

.. code-block:: javascript

    var delay_between_disks = runOptions.duration / 2 / runOptions.ndisks_per_cycle,  
        total_number_of_disks = parseInt(runOptions.ndisks_per_cycle / runOptions.speed, 10),
        start = 1.0 / runOptions.speed;

Then we create a bunch of ``<div>`` elements and store them in an array. This we, we avoid creating a bunch of elements during each animation frame, and we don't have to make calls to the DOM to get properties of the existing elements. This is different from the GIF rendering method, which creates a blank frame and draws new circles for each frame.

We create two circles here to act as the containers for the whole animation. If the site background is not black, you would see a black stroke around the inner circle.

.. code-block:: javascript

    var container = document.getElementById('container');

    var circle1 = new Disk(0.65 * diskOptions.width, [0.65 * diskOptions.width, 0.65 * diskOptions.width]),  
        circle2 = new Disk(0.42 * diskOptions.width, [0.42 * diskOptions.width, 0.42 * diskOptions.width]);

    circle1.disk.id = 'circle1';  
    circle2.disk.id = 'circle2';  
    circle1.disk.className = '';  
    circle2.disk.className = '';

    circle1.disk.appendChild(circle2.disk);  
    container.appendChild(circle1.disk);  

Finally, we can push new ``<div>`` elements into an array and add them to the DOM.

.. code-block:: javascript

    var disks = [];  
    for (var i = 0; i < total_number_of_disks; i++)  
    {
        disks.push(new Disk(0, [0, 0]));
        circle2.disk.appendChild(disks[i].disk);
    }

You may have noticed the code is calling ``new Disk(...)``. Disk is a helper method to create a new DOM element. The ``setParams`` method ensures that the disk will be positioned correctly.

.. code-block:: javascript

    /**
     * The object container for the disks that animate
     * @param {Number} radius Radius of disk
     * @param {[Number, Number]} xy cartesian coords of disk
     * @constructor
     */
    function Disk(radius, xy)  
    {
        this.disk = document.createElement('div');
        this.disk.className = 'disk';

        this.setParams(radius, xy);
    }

    /**
     * Set the radius and cartesian coords of the disk
     * @param {Number} radius
     * @param {Number} xy
     * @returns {Disk}
     */
    Disk.prototype.setParams = function (radius, xy)  
    {
        this.disk.style.width = (radius * 2) + 'px';
        this.disk.style.height = (radius * 2) + 'px';
        this.disk.style.left = (xy[0] === radius ? 0 : (xy[0] - radius)) + 'px';
        this.disk.style.top = (xy[1] === radius ? 0 : (xy[1] - radius)) + 'px';

        return this;
    }

The rendering method itself
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once ``makeFrameMethod`` finishes initializing the ``<div>`` elements that are actually animated, it then creates and returns the method that will handle positioning each ``<div>`` on every frame.

I am not particularly skilled at math, and will do a terrible job explaining how this works. However, you can read up on `calculating polar coordinates <http://www.mathsisfun.com/polar-cartesian-coordinates.html>`_ to better understand the code below.

The ``color`` variable is just for some extra fun to variably change the opacity of a few circles along the horizontal plane of the animation.

.. code-block:: javascript

    function make_frame(t)  
    {
        var angle, radius, cartCoords, color, circle;

        for (var i = 0; i < total_number_of_disks; i++)
        {
            angle = (Math.PI / runOptions.ndisks_per_cycle) * (total_number_of_disks - i - 1);
            radius = Math.max(0, 0.05 * (t + start - delay_between_disks * (total_number_of_disks - i - 1)));

            cartCoords = polar2cart(radius, angle);
            cartCoords[0] = (cartCoords[0] + 0.5) * parseInt(circle2.disk.style.width, 10);
            cartCoords[1] = (cartCoords[1] + 0.5) * parseInt(circle2.disk.style.height, 10);

            color = ((i / runOptions.ndisks_per_cycle) % 1.0);

            circle = disks[i].setParams(0.3 * diskOptions.width, cartCoords, i).disk;

            circle.style.opacity = diskOptions.opacity ? color : 1;
        }
    }

Now whenever ``requestAnimFrame(run)`` succeeds, ``make_frame(t)`` will iterate over every circle and reposition them. The end result is a very cool animation looking like an endless circle of circles flowing out of the center of the container.

Accomplishing this with ``<canvas>``
------------------------------------

While the ``<div>`` method works, it's unfortunately very inefficient. Even when using GPU rendering with ``.disk { transform : translate3d(0, 0, 0); }``, it's just too expensive and chugs along. Canvas, on the other hand, is perfect for animations. Previously, I worked with the raw DOM API when toying around with an `online Ascension clone <https://github.com/aholmes/Ascension>`_. I didn't want to do that this time, so I used `Pixi.js <http://www.pixijs.com/>`_, which saved me hours of work.

All the methods for the ``<canvas>`` approach to this project have the same name as the ``<div>`` approach. Only the inner-workings have changed.

Bootstrapping the ``<canvas>`` rendering method
-----------------------------------------------

We have to do a little more work to get set up using ``<canvas>``.

Both of these variables are meant to store objects and functions for rendering with Pixi.js. This was, we don't need to constantly recreate things.

.. code-block:: javascript

    var runModeHelpers = {}, getGraphics;  

``getGraphics()`` returns the shape-drawing object in Pixi.js.

.. code-block:: javascript

    getGraphics = function ()  
    {
        return new PIXI.Graphics()
            .beginFill(Hex2Num(diskStyles.backgroundColor), diskStyles.opacity)
            .lineStyle(diskStyles.stroke, Hex2Num(diskStyles.borderColor), diskStyles.opacity);
    };

    runModeHelpers.Graphics = getGraphics();

    runModeHelpers.Reset = function ()  
    {
        runModeHelpers.Stage.removeChild(runModeHelpers.Graphics);
        runModeHelpers.Graphics.clear();
        runModeHelpers.Graphics = getGraphics();
        runModeHelpers.Stage.addChild(runModeHelpers.Graphics);
    };

    runModeHelpers.Stage = new PIXI.Stage(0x000000);  
    runModeHelpers.Stage.addChild(runModeHelpers.Graphics);

    runModeHelpers.Renderer = undefined;  

The ``Disk`` class has changed as well. It now creates a new circle object from the Pixi.js Graphics object. ``Disk.prototype.setParams`` is now a NOOP.

.. code-block:: javascript

    function Disk(radius, xy)  
    {
        this.disk = runModeHelpers.Graphics;

        this.disk.drawCircle(
            xy[0],
            xy[1],
            radius
        );
    }

Finally, we create the ``<canvas>`` element and add it to the DOM.

.. code-block:: javascript

    runModeHelpers.Renderer = new PIXI.autoDetectRenderer(  
        0.42 * diskOptions.width * 2,
        0.42 * diskOptions.width * 2,
        null, // view
        false, // transparent
        true // antialias
    );
    runModeHelpers.Renderer.view.id = 'canvas';  
    container.appendChild(runModeHelpers.Renderer.view);

    runModeHelpers.Renderer.render(runModeHelpers.Stage);  

The rendering method itself (part two)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With the ``<canvas>`` method, the rendering method is very similar to the ``<div>`` methods. New positions are calculated, and circle are drawn. What's different, however, is that each frame is cleared before redrawing, similar to how the GIF method renders each frame.

.. code-block:: javascript

    function make_frame(t)  
    {
        var angle, radius, cartCoords, color;

        runModeHelpers.Reset();

        for (var i = 0; i < total_number_of_disks; i++)
        {
            angle = (Math.PI / runOptions.ndisks_per_cycle) * (total_number_of_disks - i - 1);
            radius = Math.max(0, 0.05 * (t + start - delay_between_disks * (total_number_of_disks - i - 1)));

            cartCoords = polar2cart(radius, angle);
            cartCoords[0] = (cartCoords[0] + 0.5) * runModeHelpers.Renderer.width;
            cartCoords[1] = (cartCoords[1] + 0.5) * runModeHelpers.Renderer.height;

            if (diskOptions.opacity)
            {
                color = ((i / runOptions.ndisks_per_cycle) % 1.0);

                runModeHelpers.Graphics
                    .endFill()
                    .beginFill(Hex2Num(diskStyles.backgroundColor), color)
                    .lineStyle(diskStyles.stroke, Hex2Num(diskStyles.borderColor), color);
            }

            new Disk(0.3 * diskOptions.width, cartCoords);
        }

        runModeHelpers.Renderer.render(runModeHelpers.Stage);
    }

Wrap up
-------

That's just about the end of the interesting bits of this demo. It all boils down to drawing circle in the correct place, and porting the concept to JavaScript. The dialog on the page allows the user to change colors, the size of the circles, the rate at which frames are renered, and so on. The code is available on `GitHub <https://github.com/aholmes/vectoranimations>`_ if you'd like to see how the rest works.

Thanks for reading!

-*Aaron Holmes*


|cta|
|disqus|