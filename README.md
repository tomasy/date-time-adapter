# DateTime adapter

DateTime adapter for Mozilla IoT Gateway.

Purpose: Create rules where date and time is needed as input

## Upgrade ##
After upgrade the addon the pages must be reloaded before the new attributes are visible.  
After upgrade to version 1.0.0 check existing rules because some properties are changed.

## Release notes ##
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
 * Sunrise (na event)
 * Sunset (an event)
 * Weekend. Boolean on for Saturday and Sunday
 * Weekday. Enum. Monday...Sunday
 * Dark. Boolean on when it is dark outside
 * Hour. Integer, values 0-23
 * Minute. Integer, values 0-59. Support < and > in rule-engine
 * Even Hour. Boolean on for even hours
 * Even minute. Bollean on for even minute
 * 5 minutes. Enum. Values 0,5,10,15,20,...,55. (Note it is called minute5 in rule engine)

## Configuration
Configure the position latitude and longitude where you live and horizon. Normally the sunset/sunrise
is set to some values whe the sun is below horizon.

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

A motion sensor is onlyactive between 10:00--10:59 
`if DateTime Hour_N is greater than 9 and DateTime Hour_N is less than 11 and Motion sensor is motion, turn Light on`

## Bugs
### Bug 1.
Because of a bug in gateways rule enginge it will not handle rules with more than one properties correctly.
If a rule is `if DateTime minute is 5 and DateTime is dark, turn Fan on` it will not work directly if the
rule is created when it is dark. To work it must first be not dark.  
To solve this after the rule is created go to the things page and click on the dark property in DateTime device.
The same is valie for e.g. 'weekend'.  
See bug https://github.com/mozilla-iot/gateway/issues/1452


```
sudo apt install python3-dev libnanomsg-dev
pip install pyephem # 3.7.6.0 sunset/sunrise
sudo pip3 install nnpy pytz
sudo pip3 install git+https://github.com/mozilla-iot/gateway-addon-python.git
```
