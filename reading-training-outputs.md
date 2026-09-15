# Reading `model.train()` Output — Ultralytics YOLO

Notes for interpreting what a training run prints and saves.

## 1. Live console output (during training)

Each epoch prints one line that looks roughly like:

```
Epoch  GPU_mem  box_loss  cls_loss  dfl_loss  Instances  Size
5/100    3.1G     1.42      0.98      1.15        12       640
```

Then periodically (every epoch by default) a validation line:

```
Class  Images  Instances  Box(P    R      mAP50  mAP50-95)
all    45      52         0.78     0.71   0.80    0.55
```

**The three losses (lower is better, should trend down over epochs):**
- `box_loss` — how far off the predicted bounding box location/size is from
  the true box.
- `cls_loss` — how confident/correct the predicted class label is 
- `dfl_loss` — distribution focal loss, a secondary box-precision term. Just watch that it isn't climbing.

**What to actually watch while it's running:** box_loss and cls_loss should
both fall over the first ~20-30 epochs, then flatten out. If they're still
falling fast at epoch 100, more epochs would probably help. If they
flatten by epoch 30 and stay flat, later epochs aren't doing much.

## 2. The metrics: P, R, mAP50, mAP50-95

- **P (Precision)** — of everything the model *said* was a "phone," what
  fraction actually was a phone? Low precision = lots of false alarms
  (detecting things that aren't there, or mislabeling).
- **R (Recall)** — of every actual phone in the validation images, what
  fraction did the model *find*? Low recall = it's missing real objects.
- **mAP50** — mean Average Precision at IoU threshold 0.5 (i.e., "counts as
  a correct detection if the predicted box overlaps the true box by at
  least 50%"). The most commonly quoted single number for "how good is
  this detector." 0.5+ is a reasonable first result on a small custom
  dataset; 0.8+ is quite good.
- **mAP50-95** — the same idea averaged over stricter overlap thresholds
  (0.5 through 0.95). A tougher, more honest number — expect it noticeably
  lower than mAP50 (a 0.80/0.55 split like the example above is normal,
  not a bug).

## 3. Files saved to disk (`runs/detect/train/`)

Ultralytics writes these automatically, whether or not you capture the
return value:

- **`weights/best.pt`** — the checkpoint from whichever epoch had the best
  validation performance.
- **`weights/last.pt`** — the checkpoint from the final epoch. Useful
  mainly if you want to resume training later.
- **`.csv`** — every epoch's numbers in one row each (all the
  losses + P/R/mAP columns from above). Good for pulling into a quick plot
  or table
- **`.png`** — the same data as `.csv`, already plotted as
  loss and metric curves. **This is the one image worth opening every time
  you train.** 
  Read it like this:
  - Loss curves (top rows) trending down and flattening = normal, healthy
    training.
  - Loss curves that bottom out then start *rising* again = overfitting;
    the model is starting to memorize training images instead of
    generalizing. With your dataset size, watch for this.
  - Loss curves still dropping steeply at the last epoch = you probably
    stopped too early; more epochs (or `patience` letting it run longer)
    would likely help.
- **`PR_curve.png` / `P_curve.png` / `R_curve.png`** — precision and
  recall plotted against confidence threshold. Useful if you want to
  tune the confidence cutoff your detection script uses.

## 4. Quick red flags

- **mAP staying near 0 the whole run** — usually a `data.yaml` problem
  (paths wrong, or labels not normalized), not a "needs more epochs"
  problem. 
- **Precision high, recall low** — model is cautious/confident but missing
  a lot of real objects. Often means too few training images of that
  class, or too little variation in angle/lighting.
- **Recall high, precision low** — model is trigger-happy, flagging things
  that aren't there. Often means background clutter wasn't sufficiently
  represented as "no object" in training.
- **Both good on validation but bad in your own live webcam test later** —
  classic sign your training photos don't match real deployment
  conditions (lighting, distance, background) closely enough.

