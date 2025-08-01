.. meta::
    :date: 2015-01-25

Circuit Scribe art project step #3
==================================

.. pagedate::

I finally took the time to start maping out where I'll need to draw my Circuit Scribe ink lines. I also drew where I want to place LEDs and calculated resistor values. I may need to revisit some of this to use less resistors to lower the load on the circuit, but I'm not sure. I'll have to draw out a couple circuits and test.

The LEDs I have need a forward voltage of 3.2 and a max forward current of 20 mA. With one LED, I've found that three 80.6 Ω resistors in series gives an appropriate brightness without hitting the max current rating. I'm hoping that the ~130 Ω resistance I've placed in a few places will allow a similar brightness for two LEDs in series.

Some individual LEDs are placed on the ~130 Ω resistance rail as well, and for those I added two additional 80.6 Ω resistors in series bringing the total resistance up to ~290 Ω. I may have to drop my source voltage to 5 V to avoid burning out some LEDs, or add more resistors.

Some calculations follow.

.. code-block:: text

    Measurement              Value
    Source voltage           9
    LED forward voltage      3.2
    LED max forward current  20 mA
    Single resistor          80.6 Ω

For single LEDs I calculated ``R = ((9 - 3.2) / 0.02) = 290``.

I need ``R / 80.6 = 3.6`` resistors. I rounded down to three. I didn't experience any excessive heat with this configuration.

For two LEDs in series I used four 80.6 Ω resistors; two in series, and those two in parallel with two more 80.6 Ω resistors also in parallel.

The total resistance is ``R = 1 / (1/80 + 1/80 + 1/(80 + 80)) = 32``.

The power, then, is calculated as ``I = (9 - 3.2 - 3.2) / 32 = 8.1 mA``.

For driving a single LED off the 32 Ω rail, we need to add additional resistors in series to limit the maximum forward current into the LED.

We already know that the resistance required for a single LED is 290 Ω. From here, we can subtract 32 Ω to determine how many more ohms of resistance we need to add. ``290 - 32 = 258``. We can then figure out how many 80.6 Ω resistors are needed just with division. ``258 / 80.6 = 3.2``. That's three resistors.

Oops! I only drew two additional resistors, which gives us a forward current of about 30 mA – about 10 mA too many. I'll have to revisit that circuit, or simply use a third resistor. That would give this rail about 274 Ω of resistance.

Next up, I should have the corrected circuits drawn out and I'll actually be able to draw them on my canvas!

.. tags:: circuit-scribe, circuit-scribe-seattle
