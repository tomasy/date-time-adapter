# DateTime adapter

DateTime adapter for Mozilla IoT Gateway.

Purpose: Create rules where date, time, sunrise and sunset is needed

## Upgrade ##
After an upgrade of the addon the pages must be reloaded before the new attributes are visible.

## Release notes ##
0.9.5  
 * Added property `Hour_N`. Used in rules to create interval. See below for example.
 * Added property `Minute_N`

## DateTime have the following properties
 * Sunrise
 * Sunset
 * Weekend. Boolean on for Saturday and Sunday
 * Dark. boolean on when it is dark outside
 * Hour. String, values 0-23
 * Hour_N. Number, values 0-23. Supports < and > in rule-engine
 * Minute. String, values 0-59. (Note it is called minuteS in rule engine)
 * Minute_N. Number, values 0-59. Support < and > in rule-engine
 * Even Hour. Boolean on for even hours
 * Even minute. Bollena on for even minute
 * 5 minutes. values 0,5,10,15,20,...,55. (Note it is called minute5 in rule engine)
## Setup
1. Add the **DateTime Adapter** from the `Settings` -> `Addons`
    - Go ahead and configure it
    - Valid time zone strings are `TZ` values from https://en.wikipedia.org/wiki/List_of_tz_database_time_zones. Example `Europe/Stockholm`
    - For the value `horizon`. Use https://www.timeanddate.com/sun/ , lookup your place and select "Sunrise & Sunset" to see the difference between `-0:34' or `-6`=civil twilight, `-12`=nautical and `-18`=astronomical
2. Add the **DateTime** Thing from the ``Things`` -> ``+`` menu

Now it will be available for use in the ``Rules`` palette. (Thanks to @hwine and @mrinx)

## Configuration
Configure the position latitude and longitude where you live and horizon. Normally the `horizon`
is set to some values where the sun is below horizon.

## Example
Turn the lamp in bedroom only on weekdays
`if the time of day is 06:13 and DateTime is not weekend, turn BedroomLamp on

To start the fan evey hour and switch it of after 5 minutes  
`if DateTime minutesS is 20, turn Fan on`  
`if DateTime minutesS is 25, turn Fan off`

To start the fan evey second hour when it is dark and switch it of after 5 minutes  
`if DateTime is dark and DateTime minutesS is 20 and DateTime is even_hour, turn Fan on`  
`if DateTime minutesS is 25, turn Fan off`

If it only for 5 minutes
`while DateTime minutes5 is 5, turn Fan on`

A motion sensor is only active between 10:00--10:59
`if DateTime Hour_N is greater than 9 and DateTime Hour_N is less than 11 and Motion sensor is motion, turn Light on`

## Debug
### Find calculated sunset and sunrise time
Go to `Settings` -> `Developer` -> `View Logs` -> `run-app.log`. Search for `sunrise will happen in`. As an example you will get `sunrise will happen in 17:55:20.881772 at 2018-11-12 07:45:23.299329+01:00` so sunrise will be at `07:45`

## Bugs
### Bug 1.
Because of a bug in gateways rule enginge it will not handle rules with more than one properties correctly.
If a rule is `if DateTime minute is 5 and DateTime is dark, turn Fan on` it will not work directly if the
rule is created when it is dark. To work it must first be not dark.  
To solve this after the rule is created go to the things page and click on the dark property in DateTime device.
The same is valie for e.g. 'weekend'.  
See bug https://github.com/mozilla-iot/gateway/issues/1452

### Bug 2.
Properties 'Hour', 'Minute' should be of type integer but rule engine do not support this.  
See bug https://github.com/mozilla-iot/gateway/issues/1456

### Bug 3.
5 minutes should be of type enum but rule engine do notsupport this.  
See bug https://github.com/mozilla-iot/gateway/issues/1457
