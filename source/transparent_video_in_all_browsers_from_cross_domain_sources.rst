.. meta::
    :date: 2017-01-06

Transparent Video in all Browsers from Cross-Domain Sources
===============================================================

.. pagedate::

A brief history of :strike:`time` cross-domain transparent video
----------------------------------------------------------------

Transparent video is not a terribly new concept in web development,
however, because browsers do not support transparency in videos,
accomplishing this requires `a unique solution <http://www.sciencelifeny.com/transparency/transparency.html>`_
that involves a canvas element and a video with a separate alpha
channel.

This solution does actually work very well to work around the
limitation. There is a gotcha to be aware of when using video
sources from a different origin, however; drawing to the canvas
with data from a different origin "`taints <https://developer.mozilla.org/en-US/docs/Web/HTML/CORS_enabled_image#What_is_a_tainted_canvas>`_"
the canvas. Once a canvas has been tainted, you are no longer able
to extract data from the canvas. This breaks the workaround for
transparent video, which relies on extracting the values of the
alpha channel stored in a canvas. Thankfully, this can be worked
around **in most** browsers by configuring `CORS <http://enable-cors.org/>`_
correctly and setting the `crossorigin <https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-crossorigin>`_
attribute on the source video element.

----

Where this fails
----------------

Unfortunately, like many things in web development, the latest versions of ``Safari 9.0.2``, ``Internet Explorer 11``, and ``Edge 25`` do not correctly honor the CORS configuration when cross-domain data is drawn to a canvas. This means there was no way to achieve transparent video in these three browsers unless the source video comes from the same origin.

After a lot of research, I stumbled across this `answer <http://stackoverflow.com/a/19734500>`_ regarding drawing cross-domain images to a canvas. The missing piece for me was the existence of the ``URL.createObjectUrl()`` method.

The solution in its entirety
----------------------------

Please reference `How to use transparency info from a video on a website <http://www.sciencelifeny.com/transparency/transparency.html>`_ for a more descriptive writeup on the basics of video transparency in browsers. The primary piece I have left out here is that you will need a video with the alpha channel stored in a separate position.

First, the HTML. The page needs:

* A single video element that does not display (because the video will be drawn to the canvas)
* A canvas whose width and height match the video, which is used to draw the video data to
* A canvas whose width matches the video, and whose height is twice the video height

The main JavaScript file execution is deferred in order to run after the page has finished loading.

.. code-block:: html

    <head>  
        <script src="script/main.js" defer></script>
    </head>  
    <body>  
        <video style="display:none" autoplay>
            <source src="video.mp4" type='video/mp4' />
        </video>
        <canvas width="1920" height="1080" id="output"></canvas>
        <canvas style="display:none;" width="1920" height="2160" id="buffer"></canvas>
    </body>  

The JavaScript will reference all three HTML elements, references to the canvas' 2D contexts and video width and height are saved, and the buffer and output canvas widths and heights are set.

.. code-block:: javascript

    var outputCanvas = document.getElementById('output'),  
        output       = outputCanvas.getContext('2d'),
        bufferCanvas = document.getElementById('buffer'),
        buffer       = bufferCanvas.getContext('2d');

    outputCanvas.width  = Math.floor(outputCanvas.clientWidth );  
    outputCanvas.height = Math.floor(outputCanvas.clientHeight);  
    bufferCanvas.width  = Math.floor(bufferCanvas.clientWidth );  
    bufferCanvas.height = Math.floor(bufferCanvas.clientHeight);

    var video  = document.getElementById('video');  
    var width  = outputCanvas.width;  
    var height = outputCanvas.height;  

In order to avoid excessive CPU usage, and to continually draw video frames to the canvas, a recursive method, ``determineDraw()`` is used in conjunction with ``requestAnimationFrame()``.

.. code-block:: javascript

    var lastDrawTime = -1;  
    function determineDraw() =>  
    {
        // If the video has finished, there is no need to execute again, and this ends the script.
        if (vid.paused || vid.ended)
        {
            URL.revokeObjectURL(url);
            return;
        }

        // If the current playhead of the video has not changed since the last time this method executed,
        // there is no need to draw the same frame again.
        // lastDrawTime's initial value is -1 because video.currentTime will never be -1.
        if (video.currentTime !== lastDrawTime)
        {
            // If the video playhead has changed, the current frame is drawn (explained below).
            draw();
            // Store the current playhead position.
            lastDrawTime = video.currentTime;
        }

        // Recurse.
        requestAnimationFrame(determineDraw);
    };

To kick things off

.. code-block:: javascript

    var xhr = new XMLHttpRequest();  
    xhr.onload = function()  
    {
        var url = URL.createObjectURL(this.response);
        var vid = document.createElement('video');
        (<any>vid).crossorigin = 'anonymous';

        vid.addEventListener('loadeddata', () =>
        {
            // now that our in-memory video element has loaded, we can remove the original video element.
            (video.remove && video.remove()) || ((<any>video).removeNode && (<any>video).removeNode());

            // Once the video starts playing, recursion begins, and we draw to the canvas roughly every 16ms.
            video.addEventListener('play', determineDraw, false);

            // start playback
            vid.play();
        });

        // setting the in-memory video source URL to the in-memory object bypasses the tainted canvas cross-origin check.
        vid.src = url;
    };

    function draw() =>  
    {
        buffer.drawImage(video, 0, 0);

        // this can be done without alphaData, except in Firefox which doesn't like it when image is bigger than the canvas
        var image = buffer.getImageData(0, 0, width, height),
            imageData = image.data,
            alphaData = buffer.getImageData(0, height, width, height).data;

        // Grabs every 4th data point (the alpha value) and overwrites the same data point on the RGB channel.
        for (var i = 3, len = imageData.length; i < len; i = i + 4)
        {
            imageData[i] = alphaData[i - 1];
        }

        output.putImageData(image, 0, 0, 0, 0, width, height);
    }


An admission
------------

I started writing this post almost a year ago now, and I never got back around to breaking the code down into more describable parts.

I also, unfortunately, am unable to include another significant portion of the code that allows these same concepts to work in some older browers, or those with iffy CORS support. I can give a hint, though: it uses XMLHttpRequest to get the video (instead of a video tag) and draws the request result to the canvas.

.. tags:: JavaScript, Canvas, Experimental, AJAX, XMLHttpRequest, Video
