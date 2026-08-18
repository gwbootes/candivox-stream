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

The pink lines are the front and back edges of the desk. They should sit right
on the top and bottom of the brown. The teal lines are the squares.

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
| `horizon` | `0` | Tilts the grid, in degrees. Use it to correct the match |
| `flush` | `0` | `1` raises the camera until the desk's front edge is exactly on the bottom of the frame, hiding the lip |
| `camy` | `0.1825` | Camera height above the desk top, by hand. `flush` overrides it |

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
