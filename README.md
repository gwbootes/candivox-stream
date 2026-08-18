# Candivox Model Stage

This is one web page. It shows a 3D model with a see-through background.

You put it in OBS as a Browser source. The model is really 3D. It turns. Light hits it.
It is not a flat picture with a fake 3D filter on top.

Built by Pixel and Rattles for the Candivox stream.

---

## Why we did it this way

We looked for an OBS plugin first. There isn't a good one.

- **StreamFX** is what most guides tell you to get. It stopped working right after OBS 30. Skip it.
- **3D Effect** (by exeldro) still works. But it only tilts flat images. It cannot open a model file.
- There is one script that opens `.obj` files in OBS. It is half finished. The filename is locked in the code.

A Browser source can do real 3D, and it can be see-through. So we used that.

---

## Step 1. Get the model out of MagicaVoxel

Click **File**, then **Export**, then pick **obj**.

MagicaVoxel saves **three files**. Put all three in the `models` folder. The page needs all three.

| File | What it holds |
|---|---|
| `thing.obj` | the shape |
| `thing.mtl` | which colors to use |
| `thing.png` | the colors |

If the Export menu also has **gltf**, pick that one instead. It puts everything in one
file, so nothing can go missing. The page opens `.obj`, `.glb`, and `.gltf`.

---

## Step 2. Pick where you load it from

This page is live on the web already:

```
https://gwbootes.github.io/candivox-stream/
```

Use that and there is nothing to start up. It just works.

**The local way, if you want it.** Double-click **`stage.bat`**. It starts
minimised to your taskbar. Then use `http://localhost:8777/index.html` instead.

Use the local way when you are testing new models and have not pushed them yet,
when your internet is down, or when you want mouse tracking in OBS. Mouse
tracking only works this way. Step 6 covers it.

`serve.bat` is the older, simpler version. `stage.bat` does everything it did.

Do not open `index.html` by double-clicking it. A page opened straight off your
hard drive is not allowed to load the model files next to it. The page comes up
fine and the model never arrives.

## Step 3. Put it in OBS

1. Click **Sources**, then **+**, then **Browser**.
2. Untick **Local file**.
3. In the **URL** box, paste the line below. Change the file name to your model.
4. Set the width and height you want it to fill.
5. Leave **Shutdown source when not visible** unticked. Otherwise it reloads every time you switch scenes.

```
https://gwbootes.github.io/candivox-stream/?model=models/television.obj&spin=8
```

Try it right now with the test cube. This should show a spinning teal box on a grid:

```
https://gwbootes.github.io/candivox-stream/?model=models/test-cube.obj&debug=1&spin=20
```

If the cube spins, everything works and your own models will too.

## Step 4. Show the whole set at once

This puts every model in a row, side by side, each one turning on its own spot:

```
https://gwbootes.github.io/candivox-stream/?gallery=1&spin=15
```

Add `&debug=1` while you set it up so you can see the floor. Take it off before you stream.

**After you export new models, do two things.**

1. Double-click **`make-manifest.bat`**.
2. Push the new files to GitHub.

Here is why step 1 matters. A web page is not allowed to look inside a folder
and see what's there. So the list of models is written down in
`models/manifest.json`, and that batch file writes it. New models will not show
up until you run it.

Step 2 matters because the live page reads from GitHub. A model sitting only on
your hard drive is invisible to it.

Want only a few of them? List them yourself and skip the manifest:

```
https://gwbootes.github.io/candivox-stream/?models=models/tv.obj,models/gacha.obj
```

Two extra settings for rows:

| Setting | Normal | What it does |
|---|---|---|
| `gap` | `0.25` | Space between models. Bigger number, more room |
| `even` | `0` | Set to `1` to make every model the same height |

Leave `even` off and the models keep their real sizes next to each other. Turn it
on and they all match, which is easier to look at when one is huge and one is tiny.

---

## Step 5. Make it lean toward your mouse

Add `&parallax=25`. Now the whole row tilts toward wherever your pointer is.
Move left, it leans left. It drifts back to the middle when your mouse leaves.

The mouse pointer is hidden already. You do not have to do anything for that.

```
https://gwbootes.github.io/candivox-stream/?gallery=1&spin=15&parallax=25
```

**This exact setting does nothing in OBS. Read this part.**

An OBS Browser source never gets your mouse. OBS only passes the mouse through
while you right-click the source and pick **Interact**, and that is a popup you
have to be clicking inside of. On stream, `parallax` on its own sits dead still.

This is a limit in OBS. No setting fixes it.

`parallax` on its own is for a browser window on your own screen. **Step 6
gets the mouse working inside OBS**, and Step 7 needs no mouse at all.

Two knobs:

| Setting | Normal | What it does |
|---|---|---|
| `parallax` | `0` | How far it leans, in degrees. Try `15` to `45`. `0` turns it off |
| `ease` | `4` | How fast it catches up. Lower is slower and floatier |

| `follow` | `0` | Set to `1` to take the lean from `stage.bat`. Works in OBS |
| `sway` | `0` | Automatic lean, in degrees. Works in OBS. `0` turns it off |
| `swayspeed` | `0.09` | How fast the automatic lean travels, in laps per second |

There is no upper limit on `parallax` or `sway`. Past about `50` they start
swinging around behind the models, which is a real look if you want it.

`drag=1` turns the lean off and gives you the mouse pointer back. You cannot
have both, since they both want the mouse.

---

## Step 6. Mouse tracking that DOES work in OBS

OBS will not hand the page your mouse. So the page goes and asks for it.

Double-click **`stage.bat`**. It serves the page and answers the question
"where is the mouse right now" on the same port. The page asks thirty times a
second and leans that way.

```
http://localhost:8777/index.html?gallery=1&spin=15&follow=1
```

This has to be the `localhost` address. The GitHub one is a plain file host and
has nothing to answer with.

It follows your mouse anywhere on your desktop, across both monitors. You do
not have to be hovering over anything.

`follow=1` turns the lean on by itself, so you only need `parallax` if you want
to change how strong it is.

### Where Silhouette plugs in

The page does not care that a mouse is on the other end. It asks for a
position, and it leans toward whatever comes back.

So when Silhouette knows where your PNGTuber sits on screen, it sends that
number instead:

```
POST http://localhost:8777/position
{"x": 0.6, "y": 0.0}
```

`x` is left to right, from `-1` to `1`. `0` is the middle. Send it whenever the
avatar moves. The camera then follows him and ignores your mouse entirely.

Stop sending for two seconds and it goes back to following the mouse on its
own. Nothing to switch off, and a crash cannot freeze the camera pointing
sideways.

**This page needs no changes for that.** The work is all on Silhouette's side.

---

## Step 7. The version that needs nothing running

`sway` does the same lean, driven by a clock instead of your mouse. It needs
no input, so OBS cannot get in the way of it.

```
https://gwbootes.github.io/candivox-stream/?gallery=1&spin=15&sway=25
```

The camera traces a slow figure eight. It never repeats a flat back-and-forth,
so it reads as alive rather than as a loop.

| Setting | Normal | What it does |
|---|---|---|
| `sway` | `0` | How far it leans, in degrees. Try `15` to `35`. `0` turns it off |
| `swayspeed` | `0.09` | Laps per second. Higher is faster. `0.05` is very slow |

`parallax` wins if you set both. Sway only runs when nothing else is steering.

**Start slow.** Motion behind you on stream pulls the eye hard. `sway=20` with
the normal speed is about one full drift every eleven seconds, which is enough
to feel three-dimensional without stealing attention from you.

---

## Step 8. The perspective grid that matches the desk plate

Check it against the plate first. This draws the grid on top of the picture:

```
http://localhost:8777/index.html?plate=1&grid=1&bg=1
```

The pink rectangle is the desk. Its front and back should sit right on the top
and bottom of the brown. The floor runs well past the desk in every direction,
because the question is usually where to stand the camera rather than where the
wood stops. `&floor=40` pulls it in if the wide view is distracting, and `H`
hides the whole thing when you want to look at the models with nothing under
them.

The floor is painted in the desk's own two browns, `#4D3726` for the lines and
`#382713` for the surface. Those came out of `desk-v1`'s MagicaVoxel palette
rather than off a colour picker: 54.5% of the desk's surface is the first one
and 45.5% is the second. It stands in until the real colours are chosen, and it
is deliberately unlit, so a model held against it is being held against a flat
true colour rather than a shaded guess. `&gridcolor=` and `&floorcolor=` take
any hex when those real colours arrive, and `&fill=0` takes the surface away
and leaves the lines.

Once it looks right, drop `&bg=1`. The background goes clear again and you put
the plate behind it in OBS as its own image source.

### Where the numbers came from

Nothing here was eyeballed. Both edges of the brown were measured across 47
columns of the actual file, to less than a tenth of a pixel:

| Edge | Fitted line | Error |
|---|---|---|
| Back of desk | `y = 0.000625x + 822.558` | 0.085 px |
| Front of desk | `y = 0.005344x + 1031.808` | 0.070 px |

Those two lines are straight, and they are **not parallel**. So they cross, far
off the left of the frame, and that crossing point is the vanishing point. It
puts the horizon at `y = 794.84`.

That is **below** the middle of the frame, which means the plate's camera is
tilted slightly **up**, not down. The camera sits almost level with the desk
top and looks across it.

The desk `.obj` is 10.0 units deep, and that fixes the rest. The grid now
projects onto `y = 1032.00` and `y = 823.00`, against measured `1031.81` and
`822.56`.

### If it looks wrong

Everything above rests on one delicate number: the two edges differ in angle by
only 0.27 degrees. The measurement is solid, and it is still a small number.

If the plate was ever resized, or if that brown was drawn by hand instead of
rendered, the answer changes. **Look at it before you trust it.**

Add `&horizon=3` to tilt the grid down, or `&horizon=-3` to tilt it up, until
it sits on the wood. Tell me the number that worked and I will bake it in.

One thing that will look odd and is correct: the squares bunch up badly toward
the back. The camera is nearly level with the desk, so the far half of it is
squeezed into about fifteen pixels. That is what the plate says.

| Setting | Normal | What it does |
|---|---|---|
| `plate` | `0` | `1` puts the camera exactly where the plate's camera was |
| `grid` | `0` | `1` draws the grid on the desk top |
| `bg` | `0` | `1` shows the plate behind it, for checking |
| `cell` | `1` | Size of each square, in desk units |
| `floor` | `120` | How far the ground grid reaches, in desk units |
| `horizon` | `0` | Tilts the camera, in degrees. Positive looks down |
| `flush` | `0` | `1` raises the camera until the desk's front edge is exactly on the bottom of the frame, hiding the lip |
| `camy` | `0.1825` | Camera height above the desk top |
| `camz` | `0` | How far the camera stands back from its calibrated spot |
| `edit` | `0` | `1` opens the placement editor. See Step 9. Turns `plate` and `grid` on by itself |

All three camera numbers are saved in `layout.json` once you have found a shot
you like, so you should rarely need to type them. A number in the URL beats the
saved one, which makes it safe to try something without overwriting what works.

### Hiding the desk lip

```
http://localhost:8777/index.html?plate=1&grid=1&flush=1
```

`flush=1` works out the camera height for you rather than guessing at it, so
it stays exact whatever size the OBS source is.

It raises the camera about 20 percent, from `0.1825` to `0.2186`. The desk top
grows from 209 pixels to 251, and the back edge barely moves, from `823` to
`829`. The dark lip goes off the bottom of the screen entirely.

This no longer matches the plate picture, on purpose. It is a different shot.
When you rebuild the desk in 3D, build it to this camera.

---

## Step 9. Putting things on the desk

This is the part where you actually decorate.

Start **`stage.bat`**, then open this in a normal browser window:

```
http://localhost:8777/index.html?edit=1&flush=1
```

It has to be `localhost`. The GitHub page can show you the editor, but there is
nothing on the other end to save the file.

Use the same camera settings you plan to stream with. Above is `flush=1`, so
drop that if you decide against it. The models end up in the same place either
way. You just want to be looking through the lens you will actually use.

You will see the desk, and behind it a block of models slowly turning. **A turning
model means "not put down yet."** That block is the staging area. Click one and it
stops turning. That is you picking it up.

Drag it forward onto the desk and it stays where you leave it.

### Keeping things out of the lineup

Not everything in the scene should stand on the desk. Sizing blanks and flat
logo plates are part of how the art was built, not props.

Open **`models/exclude.txt`** and put a piece of the filename on its own line.
Anything matching it stays out. Run `make-manifest.bat` and it is gone from the
lineup.

Nothing is deleted. Take the line back out, rebuild, and the model returns.
Right now that file holds `screenface`, `Final-Candivox Logos`, and
`candivox names`, which is 5 files out and 10 models in.

### The controls

There is one rule and it is worth reading before the tables.

**Whatever you are holding is what the keys move.** With a model selected, the
arrows and `Q` `E` and `PgUp` `PgDn` move that model. With nothing selected they
move *you*. `Esc`, or a click on empty floor, puts the model down and gives the
keys back to the camera.

So the loop is: walk to where you want to judge the shot from, click a model,
place it, `Esc`, click the next one. You never leave the view you are working in
and there is no mode to switch.

**Moving yourself, with nothing selected:**

| You do | It does |
|---|---|
| Drag empty space | Grabs the floor and moves you with it |
| Scroll wheel | Walks in and out along the way you are looking |
| Arrow left and right | Sideways |
| Arrow up and down | Toward the desk and back |
| `PgUp` and `PgDn` | Up and down |
| `Q` and `E` | Tilts down and up |
| `F` | Looks dead level |
| `R` | Backs off until everything is on screen again |
| `Z` | Flies to the model you last had selected |
| `C` | Jumps to the real stream shot. Press again to come back |
| `H` | Hides the floor and the grid. Press again to bring them back |
| `P` | Leans the shot with your mouse. Press again to park it |

`R` does the same harmless thing whether or not you are holding a model, because
it sits right next to `C` and `C` is the one you reach for all evening. The key
that throws a placement away is `Shift`+`R`, which no finger arrives at on its
way somewhere else.

The camera stands on the floor and faces front. It will not swing around the
side and it will not roll over, on purpose: the stream camera cannot do those
things either, and a shot judged through a camera that can is a shot you cannot
actually have.

### Seeing the real frame

Press **F11**. The browser gives the page every pixel of the screen, and F11
again brings the menus back.

That matters more than it looks. The editor already crops the canvas to 16:9,
which is the shape OBS renders at, and greys out the rest of the window. Without
that crop a wide browser window shows more to the left and right than the stream
ever will, because the camera's vertical angle is fixed and the extra width comes
free. Anything placed near an edge would then be placed in a frame that does not
exist.

The corner panel reports the frame size as you go, so you can see when you have
the full 1920 across. `&ratio=0` turns the crop off, and `&ratio=1.6` sets a
different shape if the stream is ever not 16:9. Live sources never get cropped:
OBS has already sized them.

**`C` and the stream camera.** `C` puts you exactly where OBS will be. Every
control above still works there, so you can raise it, back it off, and tilt it
until the desk reads the way you want. The corner panel shows the height, the
sideways offset, the distance, and the tilt the whole time, and `S` writes those
four numbers into `layout.json` next to the models. The live page reads them
back, so the shot you find is the shot that goes out.

The calibrated position sits almost level with the desk lip, because that is
where the plate's own camera was. Treat it as a starting point.

### Making the shot lean

The stream camera drifts a short way with whatever is steering it, so the set
has depth instead of sitting there like a photograph. Your mouse steers it on
this page. In OBS, `&follow=1` steers it from `stage.py`, which is the same
hook Silhouette will use to steer it from a PNGTuber's position later.

Press `P` in the editor to watch it. It stays parked until you ask, because a
camera that drifts while you are dragging a model is a camera fighting you.

The camera **travels** rather than turning on the spot. A camera that turns
where it stands moves everything in frame by the same amount, which reads dead
flat. Travelling makes the near models slide across the far ones by real
parallax, and that is the whole effect. Measured on this set at full steer, the
gacha at the front of the desk crosses 149 pixels one way while the bowl on the
rack behind it crosses 131 pixels the *other* way.

That crossover is what `leanpivot` sets. Everything nearer than it slides one
way, everything further slides the other, and whatever sits exactly at it stays
put. The default of `6` puts the still point at the PC monitor, so the chat
stays easy to read while the desk moves around it.

`leanlock` decides how much of the framing is held. At `1` the set stays where
you framed it and you get pure parallax. At `0` the whole shot drifts with the
steer. The default `0.85` is most of the way to held, which matters on this set
because the crops at the frame edges are deliberate and a camera that wandered
would undo them. Turn `lean` down to `0.2` for something barely there, or up to
`0.6` if it should be obvious. `lean=0` switches it off.

**Moving a model:**

| You do | It does |
|---|---|
| Click a model | Picks it up |
| Drag it | Slides it around the desk top |
| Hold Shift while dragging | Snaps to the grid squares |
| `[` and `]` | Bigger and smaller |
| `Q` and `E` | Turns it |
| Arrow keys | Nudges it a little |
| `PgUp` and `PgDn` | Floats it above the desk |
| `F` | Drops it back onto the desk |
| `V` | Hides it from the live page |
| `,` and `.` | Leans it toward the camera and away |
| `N` and `M` | Leans it left and right |
| `G` | Stands it back up straight |
| `D` | Stands another one of these on the desk |
| `Del` | Removes a copy |
| `Shift`+`R` | Starts that one over |
| `Tab` | Next model |
| `Esc` | Put it down, and take the camera back |
| `Ctrl`+`Z` | Undo |
| `S` | **Save** |

Hold **Shift** with any key to move ten times as far. Hold **Alt** to move a tenth
as far, for the fiddly last bit. That works on the camera too.

**Two of something.** `D` copies whatever you are holding and sets the copy down
beside it, already at the same size and turn. Three VHS tapes on the shelf is one
model file and three sets of numbers, so nothing has to go back through
MagicaVoxel to get another one. Copies are named `vhs tape.obj#2`, `#3` and so on
in `layout.json`, and the page loads them back from there on its own. `Del`
removes a copy. It will not remove an original, since the manifest would just
load that one back on the next reload, and `V` already takes it off the live page.

`Ctrl`+`Z` takes back the two moves that can cost you work: `Shift`+`R` and `Del`.
Nudging is its own undo, so it stays off the stack and the last thing you actually
wanted to reverse is still the thing waiting there.

The panel in the corner always shows the numbers for whatever you are holding,
so it also tells you at a glance which one the keys are pointed at.

### Left and right are easy. Front and back are not.

Dragging sideways is precise. Dragging deeper is horrible, and it is horrible
for a real reason.

The camera sits almost level with the desk. So the whole back half of a ten-unit
desk lands in about fifteen pixels of screen. One pixel of mouse movement near
the back is a huge jump in depth. There is nothing to fix there. It is what the
perspective does.

So work in two passes. **Drag to get it roughly right, then use the up and down
arrows for depth.** Each press moves it a tenth of a unit, which is fine control
no amount of mouse skill will match.

Practically, the front two or three units of desk are where things belong. Past
that they are too small to read on stream anyway.

### About hiding

You have fifteen models and the desk is not that big. `V` marks one as hidden.
It still shows in the editor, so you can always click it and bring it back. It
just does not draw on the live page.

### Saving

Press **`S`**. That writes `layout.json` next to the page.

The old one is kept as `layout.json.bak`. If you save a mess, close the page,
rename the `.bak` back over it, and reload.

Every page in plate mode reads that file from then on. So this is the live one,
with everything sitting where you left it:

```
http://localhost:8777/index.html?plate=1&flush=1&gallery=1
```

No `edit=1`, no grid, no panel. Just the things on the desk.

Push `layout.json` to GitHub and the web version has your layout too.

### Two things worth knowing

**A model always stands on the desk.** Make it bigger and it grows upward
instead of sinking through the wood. That is why the height is worked out for
you rather than being something you set. `PgUp` is there for when you want
something floating on purpose.

**Placed things do not spin.** Once you put a model down, the turn you gave it
is the turn it keeps. A television slowly revolving on a desk looks wrong.
Anything you have not touched yet keeps turning, which is how you spot what is
left to do.

---

## Settings you can change

You only need one copy of this page. The settings go in the web address, after the `?`.

Join them with `&`. Like this: `?model=models/tv.obj&spin=8&pitch=20`

| Setting | Normal | What it does |
|---|---|---|
| `model` | you must set this | Where the model file is |
| `spin` | `12` | How fast it turns. Degrees per second. Use `0` to stop it |
| `yaw` | `0` | Which way it faces at the start |
| `pitch` | `14` | How high up you look from |
| `zoom` | `1` | Under 1 moves closer. Over 1 moves back |
| `fov` | `35` | Lens angle. Lower flattens the row out. Higher exaggerates depth |
| `drag` | `0` | Set to `1` to turn it with your mouse. Brings the pointer back |
| `debug` | `0` | Set to `1` to see the floor and a dark backdrop |
| `parallax` | `0` | Degrees it leans toward your mouse. `0` turns it off |
| `ease` | `4` | How fast the lean catches up. Lower is floatier |
| `lean` | `0.35` | How far the stream camera travels at full steer. `0` turns it off |
| `leanlock` | `0.85` | `1` holds the framing still, `0` lets the whole shot drift |
| `leanpivot` | `6` | The depth that stays put while everything else slides |
| `leany` | `0.16` | Vertical travel. Defaults to under half the sideways one |
| `gridcolor` | `4D3726` | The grid lines. The desk's lighter brown |
| `floorcolor` | `382713` | The solid floor. The desk's darker brown |
| `fill` | `1` | `0` leaves the grid lines with nothing behind them |

**To pose one by hand:** add `drag=1&spin=0`. Right-click the source in OBS and pick
**Interact**. Drag it until it looks good. Then write those angles into `yaw` and `pitch`.

---

## If something looks wrong

**The colors look muddy or smeared.**
MagicaVoxel saves its colors as a very small picture. Sometimes it is one row of dots.
If the page blurs that picture, each block picks up its neighbor's color. The page is
already set to keep it sharp. If you edit the code, don't remove that part.

**The model is very dark, or very flat.**
Voxel models need soft, even light. The page uses one wide soft light and two smaller
ones from different sides. That keeps the block edges easy to see. One strong light
makes voxel art look like mush.

**Nothing shows up.**
You need internet. The page loads its 3D engine (three.js) from the web each time.
We locked it to one version, `0.184.0`, so an update can never change how it looks
mid-stream.

Want it to work with no internet? Download three.js and its `examples/jsm` folder into
this repo. Then point the `importmap` block at the local copies instead.

**You see a red error box.**
Good. That's on purpose. A black square in OBS looks the same as a broken source, so
the page tells you what went wrong instead of going quiet.
