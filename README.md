# PptHandGestureRemote
An app that lets you control Google Slides presentations with just hand gestures

https://github.com/AnonymousAAArdvark/PptHandGestureRemote/assets/42499336/a10e9f64-2c5d-4257-bab8-a4e1b7895861

## How it works


### Computer Vision

Although this project sounds pretty complicated on paper, its actually easier than it seems. The computer vision / hand detection part of the code is mostly already done using Mediapipe, which is a library produced by Google that aids in pose tracking, such as in the face, hands, and body. 

So, all you have to do is tune and modify the exisitng library such that it focuses on your specific use case. After that, the mediapipe library returns all the coordinates of the body parts that you asked it to track.

<img src="https://github.com/AnonymousAAArdvark/PptHandGestureRemote/assets/42499336/ba22ab1f-baf9-457f-a8b3-bafd81647d4d" width="600" />

These are all the possible coordinates returned by Mediapipe for hands

### Gesture Detection

The hand gesture part is a little more involved, but is still simpler than it probably seems. The hand needs to pass four tests in order to be classified as being in the proper gesture:
1. The middle, ring, and pinky fingers need to be closed
2. The thumb and pointer fingers need to be completely extended
3. The thumb and pointer needs to form approximately a right angle
4. The hand needs to be either pointing in the left or right orientation, not up, down, forward, or backwards


https://github.com/AnonymousAAArdvark/PptHandGestureRemote/assets/42499336/31cca244-453b-421d-91a0-94ea0b0f35d7


If you are curious how these tests are implemented in code, they are contained within the "HandGestureDetection.py" file, it is fairly short and readable, and I also added comments explaining most of the functions.


If the hand passes all of these tests, then either the right or left arrow key will be pressed depending on the orientation. If the gesture is held, then there will be a slight delay between each arrow key press. This will move the slides forwards or backwards. If there are conflicting instructions, for example, if the right hand is pointing right, while the left hand is pointing left, then no keys will be pressed.


## Roadmap

- [x] Hand Detection
- [x] Detect hand orientation
- [x] Detect if finger is closed
- [x] Detect if finger is completely extended
- [x] Detect if thumb and index form right angle
- [x] Support left and right kepresses on both Windows and MacOS
- [x] Multi-hand Support
- [x] Build for production on both Windows and MacOS
- [ ] Convert code to Javascript
- [ ] Develop mobile website
- [ ] Create Chrome (?) extension
