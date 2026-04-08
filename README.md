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

`/esp32`: files to build the esp data<br>
`/server`: all of the backend stuff where the veiws get requested and rendered<br>
`/server/assets`: some assets for building the views<br>

## Configuration
`this section is not finished/complete`

For the task tracker to work you need a folder with daily notes and sync them to your server which is serving the backend (I use the Obsidian note taking app and Syncthing for this). They have to be formated like YearMonthDay (e.g. 20261230 or 20260408). This folder is set in the config.ini


1. copy and rename config.ini.example to config.ini
2. configure the server in this file


## Credit
Font used: https://kottke.org/plus/type/silkscreen/
