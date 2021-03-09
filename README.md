# DateTime adapter

DateTime adapter for WebThingsIO Gateway.

Purpose: Create rules where date and time is needed as input

## Upgrade ##
After upgrade the addon the pages must be reloaded before the new attributes are visible.  
After upgrade to version 1.0.2 check existing rules because some properties are changed.

## Release notes ##
1.0.2
 * Fixed bug in Sunrise offset minuts and Sunset offset minutes where it would name the events after the sunset offset only
 * Fixed bug in offsets where they would not fire after the original Event
 * Added readonly Azimuth property which represents the azimuth angle of the sun at sunrise on the current day. This can help determine certain events like blinding light or solar panel position
 * Added readonly Elevation property which represents the elevation angle of the sun at sunrise on the current day. This can help determine certain events like blinding light or solar panel position
 * Added Next time and Last time properties which represent the next/last sunset/sunrise
 
1.0.1
 * Add Sunrise Offset Minutes and Sunset Offset Minutes config which if set, generates a Sunrise/Sunset event offset from the actual Sunrise/Sunset event.
 * When creating rules simply Select your offset event i.e. Event "Sunset -n mins"

1.0.0
 * Added event 'Sunset'/'Sunrise'
 * Added property enum 'Weekday'
 * Removed property 'Sunrise'/'Sunset'
 * Removed 'Hour_n' and 'Minute n'. Not needed whe gateway 0.7 support Integer
 * Use Enum instead of Strings (require gateway version >= 0.7)
 * Use Integer instead of Strings (require gateway version >= 0.7)
 * Property 'Hour', 'Minute' is now integers
 * Property '5 minutes' is an enum

0.9.5
 * Added property `Hour_N`. Used in rules to create interval. See below for example.
 * Added property `Minute_N`

## DateTime have the following properties and events
 * Sunrise (an event)
 * Sunset (an event)
 * Sunset offset n mins (an event)
 * Sunrise offset n mins (an event)
 * Weekend. Boolean on for Saturday and Sunday
 * Weekday. Enum. Monday...Sunday
 * Dark. Boolean on when it is dark outside
 * Hour. Integer, values 0-23
 * Minute. Integer, values 0-59. Support < and > in rule-engine
 * Even Hour. Boolean on for even hours
 * Even minute. Boolean on for even minute
 * 5 minutes. Enum. Values 0,5,10,15,20,...,55. (Note it is called minute5 in rule engine)
 * Azimuth. Integer, values -180 to 180. Degrees of the sun position from North
 * Elevation. Integer, values -90 to 90. Degrees of the sun elevation from horizon
 * Next event. Integer, values 0 to 1400. Minutes until next sunrise or sunset.
 * Last event. Integer, values 0 to 1400. Minutes since last sunrise or sunset.

## Configuration
Configure the position latitude and longitude where you live and horizon. Normally the sunset/sunrise
is set to some value when the sun is below horizon.

## Example
Turn the lamp in bedroom only on weekdays
`if the time of day is 06:13 and DateTime is not weekend, turn BedroomLamp on

To start the fan evey hour and switch it of after 5 minutes  
`if DateTime minute is 20, turn Fan on`  
`if DateTime minute is 25, turn Fan off`

To start the fan evey second hour when it is dark and switch it of after 5 minutes  
`if DateTime is dark and DateTime minute is 20 and DateTime is even_hour, turn Fan on`  
`if DateTime minute is 25, turn Fan off`

If it only for 5 minutes
`while DateTime minutes5 is 5, turn Fan on`

A motion sensor is onlyactive between 10:00--10:59 
`if DateTime Hour is greater than 9 and DateTime Hour is less than 11 and Motion sensor is motion, turn Light on`

Open blinds 15 minutes before sunrise (configure -15 for offset mins)
`if DateTime event "Sunrise offset -15 mins" occurs, do Scene Controller action "AllOpen"`

Close blinds because the sun hits your eye like a big pizza pie (look at controller for az/el parameters when blinded)
`if DateTime Azimuth is greater than -112, DateTime Azimuth is less than -95, DateTime Elevation is less than 7, DateTime Elevation is greater than 2, set Blind-1 Level to 50`

## Bugs
### Bug 1.
Because of a bug in gateways rule enginge it will not handle rules with more than one properties correctly.
If a rule is `if DateTime minute is 5 and DateTime is dark, turn Fan on` it will not work directly if the
rule is created when it is dark. To work it must first be not dark.  
To solve this after the rule is created go to the things page and click on the dark property in DateTime device.
The same is valie for e.g. 'weekend'.  
See bug https://github.com/WebThingsIO/gateway/issues/1452


```
sudo apt install python3-dev libnanomsg-dev
pip install pyephem # 3.7.6.0 sunset/sunrise
sudo pip3 install nnpy pytz
sudo pip3 install git+https://github.com/WebThingsIO/gateway-addon-python.git
```
