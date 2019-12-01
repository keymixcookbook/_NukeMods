import nuke, nukescripts

notes = [
	"We want it dark and glowy",
	"Make it invisible, but we want to see it",
	"There is nothing wrong here",
	"Make it look pretty",
	"It feels wrong, fix it",
	"Too Magenta",
	"Approved",
	"let's try something different",
	"Can we have few versions of this",
	"Let's go back to version 1",
	"Final",
	"It should be easy, No?"
	"More Rain",
	"Let's massage it",
	"Just one small note",
	"Can we have it by tomorrow",
	"That grass at the corner, feels too distracting",
	"Add some lensflare, I think it will be nice",
	"Let's make more realistic....but not too much, you know",
	"Can you match this...and that...and that one also",
	"Visor reflection too yellow",
	"Visor reflection not yellow enough",
	"Pick somewhere in between",
	"Too Pink, too Salmon",
	"Something's wrong, I don't know what",
	"What do you think",
	"It looks great, but..................",
	"Could use more glow",
	"Make explosion bigger",
	"ok",
	"next",
	".",
	"Could be better",
	"We’ll check to see whether MPC can supply an updated render for this",
	"Warmer",
	"Cooler",
	"You diserve a kiss",
	"it needs more shape",
	"Fucking love this",
	"Keep going",
	"Make it pop a bit more",
	"omit",
	"Dial up the realism by 50%",
	"Can we add more CGI’s?",
	"Apply the film look",
	"grain's not organic enough",
	"Couple more rain drops",
	"It needs to be a little be more, because its a little bit not enough.",
	"It's too realistic",
	"This shot sucks. Make it not suck. Next.",
	"Can you stablize Tim (actor in the plate)",
	"50% less physics",
	"Tune down the stars a touch",
	"It looks really good, can you make it 10% better?",
	"Split the difference",
	"The Camera should pan up, pan down and pan forward",
	"Bring the sky down a bit",
	"The sequence is during daytime...(3mth later)....let's change it to golden hour...(3mth later)...Let's make it red",
	"we need some rim light on this piece of mirror",
	"Can you make that cloud happier?"
	]
dice = ['9763','9856','9857','9858','9859','9860','9861']
mood = ['9785','9786','9752','9760']
weather = ['9729','9730','9728','9889','9925','9928']

cmd_notes = '''
import random
nuke.message("Client Feedback:\n%s" % notes[random.randint(0,len(note)-1)])

'''


p = nukescripts.PythonPanel('Artist Insainty Check')

k_notes = nuke.PyScript_Knob('bt_notes',"<h1>CLIENT NOTES GENERATOR</h1>", cmd_notes)
k_dice = nuke.PyScript_Knob('bt_dice',"<h1>ROLL A DICE</h1>", cmd_dice)
k_weather = nuke.PyScript_Knob('bt_mood',"<h1>WHAT WEATHER OUTSIDE</h1>", cmd_weather)
