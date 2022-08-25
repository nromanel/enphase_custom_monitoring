# enphase_custom_monitoring
This repo contains some little snippets for the custom monitoring of my Solar instllation which uses an "Enphase IQ Combiner 3"

## 1. Splunk Data Collection

The Enphase combiner has an unauthenticated landing page.
Interrogating it via DevTools, we can see an Ajax call is made to this endpoint: http://enphase_ip/production.json

Praise be to JSON!

I'm simply reading the payload as-is and sending it to a splunk HEC Endpoint.

The HEC Token is configured to drop the data into an index called *solar*.
This is important, as the dashboard code below is based off that index.

## 2. Splunk Dashboard

The attached is good ol-fashioned Splunk Dashboard XML.

## 3. RaspberryPi LCD Desktop Display

The solution would not be complete without having a quick real-time view into my solar generation.
I picked up a 20x4 LCD Module - https://www.amazon.com/gp/product/B01GPUMP9C

Making the same call to the production.json endpoint, and generating a view of the current state of production:
eg:

    08/25/2022  16:00:00   <--- Timestamp
    Now:  4000w    6000w   <--- First Number is your current consumption, second is generation
    kWh:  35.07     49.2   <--- Today's kwH consumed and generated
    Usage Gen:     14.11   <--- A positive number is what you've exported onto the grid.
