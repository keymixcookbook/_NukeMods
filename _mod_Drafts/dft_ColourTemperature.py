[if {[value Switch1.which]==1} {return "aaa"} {return "bbb"}]


red:
clamp([if {[value kelvin]<=6600} {return 1} {329.7 * (pow([value kelvin]-60,-0.133))}])
green:
clamp([if {[value kelvin]<=6600} {99.47 * log([value kelvin]) - 161.12} {288.12 * (pow(([value kelvin]-60), -0.0755))}])
blue:
clamp([if {[value kelvin]>=6600} {return 1} {138.52 * log([value kelvin] - 10) - 305.045}])

([value kelvin]/100<=66?255:clamp((329.7*pow(([value kelvin]/100-60),-0.133)),0,255))/255
([value kelvin]/100<=66?clamp(99.47*log([value kelvin]/100)-161.12,0,255):clamp(288.12*pow(([value kelvin]-60),-0.0755),0,255))/255
([value kelvin]/100>=66?255:clamp(138.52*log([value kelvin]/100-10)-305.045,0,255))/255


([value kelvin]/100<=66?255:clamp((329.7*pow(([value kelvin]/100-60),-0.133)),0,255))/255
([value kelvin]/100<=66?clamp(99.47*log([value kelvin]/100)-161.12,0,255):clamp(288.12*pow(([value kelvin]-60),-0.0755),0,255))/255
([value kelvin]/100>=66?255:clamp(138.52*log([value kelvin]/100-10)-305.045,0,255))/255


[value kelvin]/100<=66?255:clamp(329.698727446 * pow([value kelvin]/100 - 60, -0.1332047592),0,255)


# red
if kelvin/100 <= 66:
    red = 255
else:
    tmp_red = 329.698727446 * math.pow(kelvin/100 - 60, -0.1332047592)
    if tmp_red < 0:
        red = 0
    elif tmp_red > 255:
        red = 255
    else:
        red = tmp_red

# green
if kelvin/100 <=66:
    tmp_green = 99.4708025861 * math.log(kelvin/100) - 161.1195681661
    if tmp_green < 0:
        green = 0
    elif tmp_green > 255:
        green = 255
    else:
        green = tmp_green
else:
    tmp_green = 288.1221695283 * math.pow(kelvin/100 - 60, -0.0755148492)
    if tmp_green < 0:
        green = 0
    elif tmp_green > 255:
        green = 255
    else:
        green = tmp_green

# blue
if kelvin/100 >=66:
    blue = 255
elif kelvin/100 <= 19:
    blue = 0
else:
    tmp_blue = 138.5177312231 * math.log(kelvin/100 - 10) - 305.0447927307
    if tmp_blue < 0:
        blue = 0
    elif tmp_blue > 255:
        blue = 255
    else:
        blue = tmp_blue
