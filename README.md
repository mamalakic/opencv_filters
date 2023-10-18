# Filters using computer vision
This is a project for ACM's workshop

### Notes 
- Dark png's tend to mess up the masking so they are avoided.
- Code is based off of tutorials found. e.g. https://medium.com/@mohd-uzair/making-face-filters-with-opencv-e3c928865239


## Current features
- Cycle filters using 0-9 keys
- Debug prints


## TODO
- EMA smoothing for less twitchy filter application
- More scalable code (have to add case for each new png)
- ~~Fix hat filters. They are generally out of the detected face coords.~~


## Bugs
- Program is very prone to curvature. A camera tilt can make the filter look bad. I'm not aware how I can fix lens distortion.
- Fix out of bound errors
- If the user is too far away, scaling factor will be too much and mess up filter positioning