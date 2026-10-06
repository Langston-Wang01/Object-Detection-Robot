# Python Threading

Based on: [Python official `threading` docs](https://docs.python.org/3/library/threading.html),
[Real Python's threading intro](https://realpython.com/intro-to-python-threading/),
and [GeeksforGeeks on daemon threads](https://www.geeksforgeeks.org/python/python-daemon-threads/).

## Why threading, specifically here

`input()` blocks — your program stops and does nothing else until someone
types something and hits Enter. A detection loop can't tolerate that; it
needs to keep reading frames and running inference continuously. The fix
isn't to avoid `input()`, it's to run it on a **second thread** that does
nothing but wait for typed input, while the main thread keeps looping
through frames. The two run concurrently — one blocked on `input()`, the
other never stops.

## The honest caveat: the GIL

Python has a Global Interpreter Lock (GIL) — only one thread executes
Python bytecode at a time, even on a multi-core machine. So threading in
Python does **not** give you true CPU parallelism for heavy computation
(that's what `multiprocessing` is for instead).

This doesn't matter for this use case. Threading is still genuinely useful
when a thread spends most of its time *waiting* rather than computing —
waiting on `input()`, waiting on a file read, waiting on a network
response. While one thread is blocked waiting, Python happily lets another
thread run. A thread sitting idle on `input()` is exactly this case: it's
waiting on you to type, not doing CPU work, so it doesn't compete with
your detection loop for the GIL.

## The core API

```python
import threading

def some_function():
    ...

t = threading.Thread(target=some_function, args=(), daemon=True)
t.start()
```

- `target` — the function this thread runs. Pass the function itself
  (`some_function`), not a call to it (`some_function()`).
- `args` — a tuple of arguments to pass to `target`, if it takes any.
  Omit if the function takes none.
- `daemon` — see below. Set at creation time, not changeable after
  `.start()`.
- `.start()` — actually begins running the thread. Nothing happens until
  you call this.
- `.join()` — (not used in this project, but worth knowing) blocks the
  calling thread until the target thread finishes. Not relevant here
  since this background thread runs forever, for the life of the program.

## `daemon=True` — why it matters

A normal (non-daemon) thread keeps the whole program alive until it
finishes on its own — Python won't exit while a non-daemon thread is still
running, even if your main loop has already broken out and finished. The
thread runs an infinite `while True: input()` loop that
never naturally finishes.

`daemon=True` marks the thread as background/expendable: when every
non-daemon thread (your main program) has finished, Python kills any
remaining daemon threads automatically and exits cleanly. This is exactly
what you want for a thread whose only job is "wait for input until the
program ends."

## Sharing a variable between threads

```python
currentTarget = "..."

def listenForTarget():
    global currentTarget
    while True:
        newTarget = input("Enter class to track: ")
        currentTarget = newTarget
```

`global currentTarget` inside the function is required — without it,
`currentTarget = newTarget` would create a new *local* variable inside
`listenForTarget` instead of modifying the outer one, and your main loop
would never see the update.

Is this safe without a `Lock`? For this specific case — one thread
occasionally writing a simple string, the other thread just reading it —
yes. Reassigning a variable to point at a new string object is a single
atomic step in CPython; there's no window where the main loop could read a
half-written value. Locks matter when multiple threads modify *shared,
mutable* data structures together (like both appending to the same list),
which isn't happening here. Worth knowing as a boundary, not something
this project needs to implement.
