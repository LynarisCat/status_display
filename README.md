# status_display

## The Idea
This is just a fun side project where i try to make a small E-Ink display that shows some data about the wheather but also to show my digital tasktracking on my whiteboard.
It's my first time messing aroung with an esp, so let's see where this goes.

---
The basic flow is this:
```
The Esp wakes up every hour -> requests a new view via http -> the server collects the data and renders the view -> the view is sent back to the esp -> the esp shows it on the E-Ink Display
```
---

## Project structure

`/esp32`: files to build the esp data
`/server`: all of the backend stuff where the veiws get requested and rendered
`/server/assets`: some assets for building the views
