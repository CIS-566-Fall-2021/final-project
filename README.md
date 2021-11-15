# Final Project!

This is it! The culmination of your procedural graphics experience this semester. For your final project, we'd like to give you the time and space to explore a topic of your choosing. You may choose any topic you please, so long as you vet the topic and scope with an instructor or TA. We've provided some suggestions below. The scope of your project should be roughly 1.5 homework assignments). To help structure your time, we're breaking down the project into 4 milestones:

## Milestone 1: Project planning (due 11/15)
Before submitting your first milestone, _you must get your project idea and scope approved by Rachel, Adam or a TA._

### Design Doc
Start off by forking this repository. In your README, write a design doc to outline your project goals and implementation plan. It must include the following sections:

#### Introduction
I have a lot of experience in interior environment modelling, however, not so much exterior. I have once attempted to model a street-view environment piece, however found it time consuming and difficult to get right. I also do love Japanese architecture and Japan itself. Thus, combining those two interests, and drawing some inspiration from this poster in my bedroom wall, I want to create a tool that can procedurally generate traditional 'minka' to be placed in a courtyard scene. 



#### Goal
As a minimum viable product, I hope to create an art tool that procedurally creates a traditional japanese minka. Users can customise number of stories, width and height, number of sections, roof slant, whether it sits on top of an elevated platform with staris etc. Colours can be customised too. As a stretch goal, I want to put these houses in a courtyard layout. Placement of the minka would be procedural too. 

#### Inspiration/reference:
I was inspired from this poster in my bedroom wall, and this series of youtube videos:
![image](https://user-images.githubusercontent.com/59979404/141842228-30ea29e6-5119-4356-adaa-fb21b245b9fb.png)
https://www.youtube.com/watch?v=TwCthsWsI7Y&ab_channel=RaduCius
https://www.youtube.com/watch?v=dpqsePcSRkk&ab_channel=Houdini

I found this tutorial on how to procedural create a european style house, which I can adapt for my purposes: https://www.youtube.com/watch?v=WuNTFrDLABY&ab_channel=SimonHoudini

There are also a handful tutorials on creating procedural cities. I can reduce the scale of the city to a smaller courtyard. 
https://www.youtube.com/watch?v=n3m9E4-NkqE&t=522s&ab_channel=%D0%94%D0%B5%D0%BD%D0%B8%D1%81VFX

#### Specification:
- Create a HDA in houdini that generates a traditional japanese Minka procedrally
- Add sliders to adjust various parts of the model including colour
- If I don't get to placing the houses in a procedurally generated courtyard map, I will just use my tool to populate a fixed scene. 
- Aim to get a really nice render!

Create a basic tool that generates a single flower procedurally
Import a petal with a texture and rotate around center n number of times
Add blooming animation that follows pattern from visual reference
Fine tune tool to add more variance and input controls
Focus on getting a really nice render of one flower - will have to learn how to light a scene
Use flower tool to fill a bouquet of flowers or populate some organic scene

#### Techniques:
- What are the main technical/algorithmic tools you’ll be using? Give an overview, citing specific papers/articles.
- I came into this class with little to no experience with Houdini, so I look forward to experimenting and learning how to use this piece of software as my technical challenge. I don't want to over complicate this project too much, so just focusing on the basics of understanding how to use the graph editor, and vex expressions to achieve the exterior of the Japanese house.
- https://www.youtube.com/watch?v=Ri9AAF_hB6Q&ab_channel=IlliaStatkevych
- https://www.artstation.com/marketplace/p/y3DV/houdini-tutorial-procedural-japanese-castle-in-unreal-engine-4

#### Design:
- How will your program fit together? Make a simple free-body diagram illustrating the pieces.

#### Timeline:
- WEEK 1: Work through some houdini procedural house examples, and adapt what I have learned to create a basic Japanese house tool. Focus on breaking down a Japanese house into distinct features (roof, floors, windows and doors, shape)
- WEEK 2: Add more polish to the generator tool as well as texture the house. Give users ability to change the colours of the house. Look into courtyard layout and proceduralism if I have time.
- WEEK 3: Use my tool to create a cool scene in a static/generated courtyard. Render multiple scenes. Add a sky, some trees, etc. to mimic reference images.
