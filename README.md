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

## Step 2. Start the little server

Double-click **`serve.bat`**. A black window opens. Leave it open.

You need this. Here is why. When a web page is opened straight off your hard drive,
the browser will not let it load other files next to it. The page shows up fine and the
model never arrives. Serving the folder over `localhost` gets rid of that rule.

To stop it, close the black window.

## Step 3. Put it in OBS

1. Click **Sources**, then **+**, then **Browser**.
2. Untick **Local file**.
3. In the **URL** box, paste the line below. Change the file name to your model.
4. Set the width and height you want it to fill.
5. Leave **Shutdown source when not visible** unticked. Otherwise it reloads every time you switch scenes.

```
http://localhost:8777/index.html?model=models/television.obj&spin=8
```

Try it right now with the test cube. This should show a spinning teal box on a grid:

```
http://localhost:8777/index.html?model=models/test-cube.obj&debug=1&spin=20
```

If the cube spins, everything works and your own models will too.

## Step 4. Show the whole set at once

This puts every model in a row, side by side, each one turning on its own spot:

```
http://localhost:8777/index.html?gallery=1&spin=15
```

Add `&debug=1` while you set it up so you can see the floor. Take it off before you stream.

**After you export new models, double-click `make-manifest.bat`.**

Here is why. A web page is not allowed to look inside a folder and see what's
there. So the list of models is written down in `models/manifest.json`, and that
batch file writes it. New models will not show up until you run it.

Want only a few of them? List them yourself and skip the manifest:

```
http://localhost:8777/index.html?models=models/tv.obj,models/gacha.obj
```

Two extra settings for rows:

| Setting | Normal | What it does |
|---|---|---|
| `gap` | `0.25` | Space between models. Bigger number, more room |
| `even` | `0` | Set to `1` to make every model the same height |

Leave `even` off and the models keep their real sizes next to each other. Turn it
on and they all match, which is easier to look at when one is huge and one is tiny.

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
| `drag` | `0` | Set to `1` to turn it with your mouse |
| `debug` | `0` | Set to `1` to see the floor and a dark backdrop |

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
