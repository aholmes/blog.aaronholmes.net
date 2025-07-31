Speech Synthesis on Windows Phone 8.1
=====================================

07 December 2014

I recently wrote an application to make my phone report current Los Angeles traffic conditions. I used the ``Windows.Media.SpeechSynthesis`` namespace to read in either a plain-text string, or an `SSML <http://www.w3.org/TR/speech-synthesis/>`_-formatted string, and to speak it until the end. It turns out that speech synthesis with .NET libraries is incredibly simple, but some information takes a little effort to find. For me, searching for "text-to-speech windows phone 8.1" shows me a bunch of results for how to accomplish this with Silverlight! Definitely not what I want.

The setup
---------

Because this was for a Windows Phone application, I needed a way to access a ``MediaElement`` object to play, pause, and stop the speaking if I pressed a button to do this. I opted to create a private object on my ``MainPage`` instance.

.. code-block:: csharp

    namespace PhoneTraffic  
    {
        public sealed partial class MainPage : Page
        {
            private MediaElement media;

            public MainPage()
            {
                this.InitializeComponent();
                this.NavigationCacheMode = NavigationCacheMode.Required;
                media = new MediaElement();
            }
        }
    }
    
From here, we instantiate a ``SpeechSynthesizer`` object.

.. code-block:: csharp
   
    using(var synth = new SpeechSynthesizer())  

Then we need to pass a *plain-text* string into the synthesizer, and store the outputted stream so we can set it on the ``media`` object.

.. code-block:: csharp
   
    var stream = await synth.SynthesizeTextToStreamAsync("Hello, World!");  


Then set the stream source on our ``media`` object.

.. code-block:: csharp
   
    media.SetSource(stream, stream.ContentType);  

Now we're ready to tell the phone to play, pause, or stop the speaking of our sentence. Here's how it looks in my application.

Using plain-text
^^^^^^^^^^^^^^^^

.. code-block:: csharp

    private async void GetTrafficButton_Click(object sender, RoutedEventArgs e)  
    {
        var incidents = await Task.Run(() => JsonConvert.DeserializeObject<TrafficIncident[]>(trafficJson));

        if (incidents.Length == 0)
        {
            using(var synth = new SpeechSynthesizer())
            {
                var stream = await synth.SynthesizeTextToStreamAsync("There are no incidents right now.");
                media.SetSource(stream, stream.ContentType);
                media.Play();
            }
        }
        else
        {
            using(var synth = new SpeechSynthesizer())
            {
                var toSay = String.Empty;

                for(var i = 0; i < incidents.Length; i++)
                {
                    var incident = incidents[i];

                    toSay += " At " + incident.Time + " there was a " + incident.Incident + " incident at " + incident.Location;
                    toSay += (i < incidents.Length - 1) ? " and another " : ".";
                }

                var stream = await synth.SynthesizeTextToStreamAsync(toSay);
                media.SetSource(stream, stream.ContentType);
                media.Play();
            }
        }
    }

My pause and stop methods are simpler:

.. code-block:: csharp
   
    private void PausedSpeechButton_Click(object sender, RoutedEventArgs e)  
    {
        media.Pause();
    }

    private void StopSpeechButton_Click(object sender, RoutedEventArgs e)  
    {
        media.Stop();
    }
    
Using SSML
^^^^^^^^^^

If you want to use SSML, use the method ``SynthesizeSsmlToStreamAsync`` instead of ``SynthesizeTextToStreamAsync`` and pass an SSML-formatted string to it.

My application supports both modes. I create the SSML string on my API server, and the phone consumes it. Here's what the code looks like (replaces the "else" block in the plain-text example).

.. code-block:: csharp

    using(var synth = new SpeechSynthesizer())  
    {
        var stream = await synth.SynthesizeSsmlToStreamAsync(ssml);
        media.SetSource(stream, stream.ContentType);
        media.Play();
    }

Here are some resources I used.

* Wikipedia `Speech Synthesis Markup Language <https://en.wikipedia.org/wiki/Speech_Synthesis_Markup_Language>`_

* W3 `Speech Synthesis Markup Language (SSML) Version 1.0 <http://www.w3.org/TR/speech-synthesis/>`_

* Microsoft MSDN `Windows.Media.SpeechSynthesis namespace <http://msdn.microsoft.com/en-us/library/windows.media.speechsynthesis.aspx>`_

* Microsoft MSDN `SSML say-as Examples <http://msdn.microsoft.com/en-us/library/dd450828(v=office.13).aspx>`_

* Jayway `Windows Phone 8.1 for Developers - Text to speech <http://www.jayway.com/2014/04/15/windows-phone-8-1-for-developers-texttospeech/>`_

.. tags:: C#, .NET, windows-phone, speech