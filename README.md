# Final Project!

This is it! The culmination of your procedural graphics experience this semester. For your final project, we'd like to give you the time and space to explore a topic of your choosing. You may choose any topic you please, so long as you vet the topic and scope with an instructor or TA. We've provided some suggestions below. The scope of your project should be roughly 1.5 homework assignments). To help structure your time, we're breaking down the project into 4 milestones:

## Milestone 1: Project planning (due 11/15)
Before submitting your first milestone, _you must get your project idea and scope approved by Rachel, Adam or a TA._

### Design Doc
Start off by forking this repository. In your README, write a design doc to outline your project goals and implementation plan. It must include the following sections:

#### Introduction
- What motivates your project?

We want to create a dungeon crawler rogue-like game. The basic idea is to have a player start in a procedurally generated dungeon and have the player get to the final room and
proceed to the next level. We want there to be some number of "abilities" that the player can unlock, and some obstacles/puzzles that can't be bypassed except by the use
of these abilities. For the generator, we want to be able to take in a set of inputs (placements of points of interests, obstacle/puzzle elements, start and end positions) which would then be used to generate a solvable dungeon. There may or may not be combat elements based on time contraints, but basic combat elements with enemies/boss seem very possible. This game would be played from a top-down view (like 2.5d) on a grid (although this could probably be changed to free-form/hexagonal/etc with enough persuasion).

#### Goal
- What do you intend to achieve with this project?

We want to be able to generate a solvable dungeon with obstacle and unlockable abilty elements. We also want to be able to incorporate a level of "hand-craftedness" by being
able to generate the dungeon when given placements of key elements and perhaps path retrictions (like placed walls). Solvable here means the player is able to get to the final room without encountering a configuration where the player can't get to the end because an ability is locked behind an unbypassable obstacle. It'd be nice to have the game be playable.

#### Inspiration/reference:
- You must have some form of reference material for your final project. Your reference may be a research paper, a blog post, some artwork, a video, another class at Penn, etc.  
- Include in your design doc links to and images of your reference material.

Our inpiration comes from a couple games, Crypt of the Necrodancer and some of the older 2D Legend of Zelda games as well as other dungeon generators online.

Crypt of the Necrodancer gameplay: https://youtu.be/3dQU5QK_Bh8
We like how in this game the dungeon is generated using a start and end goal, and the entire level is filled with enemies to get past in order to descend the staircase.

Legend of Zelda: Link's Awakening: https://youtu.be/UQlP9sHf5Ho?t=3927
In this snippet, we see how Link equips a feather to jump over a pit to kill enemies and get to the next room, a similar idea to what we want to implement with "abilities" solving "obstacles"

Mario Maker: https://youtu.be/w3FJDipEdtA
The idea of placing down elements on a map would be similar to (but less complex than) how objects are placed to handcraft a Mario Maker level. However we want procedural generation to still take the reins and generate content.

Basic dungeon generator: https://donjon.bin.sh/d20/dungeon/
Just a basic dungeon generator but one that would be similar to how we plan to generate a 2D grid dungeon

#### Specification:
- Outline the main features of your project.

Developer mode to enable placing of elements to be used in the generation of a dungeon level. Be able to define other rules such as walls that the generator must obey.

Gameplay mode where the player controls a character and navigates a dungeon to get to the end. Support controls for movement, ability usage, etc.

#### Techniques:
- What are the main technical/algorithmic tools you’ll be using? Give an overview, citing specific papers/articles.

Pathfinding algorithms (DFS,BFS, Uniform Cost Search, etc) https://www.redblobgames.com/pathfinding/a-star/introduction.html

#### Design:
- How will your program fit together? Make a simple free-body diagram illustrating the pieces.

![image](https://user-images.githubusercontent.com/49851189/141921568-039dcb2e-6987-420a-a288-4e13c92c30fc.png)

#### Timeline:
- Create a week-by-week set of milestones for each person in your group. Make sure you explicitly outline what each group member's duties will be.

MS2:

Ben: Level Generator. Generate solvable dungeon using input and output text file. Implement only 1 or 2 obstacles/abilities 

Ruth: Parser. Read a dungeon text file and render a dungeon on screen (Look very ugly). Player gameplay

MS3:

Ben: Iron bugs/optimaztions. Add more obstacles/abilities. Implement a start screen to place elements (Hopefully)

Ruth: Add textures (Make look good).

Final:

Both: Polish

Submit your Design doc as usual via pull request against this repository.
## Milestone 2: Implementation part 1 (due 11/22)
Begin implementing your engine! Don't worry too much about polish or parameter tuning -- this week is about getting together the bulk of your generator implemented. By the end of the week, even if your visuals are crude, the majority of your generator's functionality should be done.

Put all your code in your forked repository.

Submission: Add a new section to your README titled: Milestone #1, which should include
- written description of progress on your project goals. If you haven't hit all your goals, what's giving you trouble?
- Examples of your generators output so far
We'll check your repository for updates. No need to create a new pull request.

UPDATE:

The goals for this milestone was to have the generator produce a map that contains different types of "doors" and "keys", and have it be such that the map is solvable. Another goal was to have the map be renderable by webgl, and have a playable game.

What is implemented right now is the core logic component for the map generator. Doors and keys are placed in such a way that the map is guaranteed to be solvable. The current output right now is a crude text file with 3x3 boxes that represent rooms and other symbols representing door and key types. As of now we do not have the game renderable and playable.

## Milestone 3: Implementation part 2 (due 11/29)
We're over halfway there! This week should be about fixing bugs and extending the core of your generator. Make sure by the end of this week _your generator works and is feature complete._ Any core engine features that don't make it in this week should be cut! Don't worry if you haven't managed to exactly hit your goals. We're more interested in seeing proof of your development effort than knowing your planned everything perfectly. 

Put all your code in your forked repository.

Submission: Add a new section to your README titled: Milestone #3, which should include
- written description of progress on your project goals. If you haven't hit all your goals, what did you have to cut and why? 
- Detailed output from your generator, images, video, etc.
We'll check your repository for updates. No need to create a new pull request.

Come to class on the due date with a WORKING COPY of your project. We'll be spending time in class critiquing and reviewing your work so far.

## Final submission (due 12/6)
Time to polish! Spen this last week of your project using your generator to produce beautiful output. Add textures, tune parameters, play with colors, play with camera animation. Take the feedback from class critques and use it to take your project to the next level.

Submission:
- Push all your code / files to your repository
- Come to class ready to present your finished project
- Update your README with two sections 
  - final results with images and a live demo if possible
  - post mortem: how did your project go overall? Did you accomplish your goals? Did you have to pivot?

## Topic Suggestions

### Create a generator in Houdini

### A CLASSIC 4K DEMO
- In the spirit of the demo scene, create an animation that fits into a 4k executable that runs in real-time. Feel free to take inspiration from the many existing demos. Focus on efficiency and elegance in your implementation.
- Example: 
  - [cdak by Quite & orange](https://www.youtube.com/watch?v=RCh3Q08HMfs&list=PLA5E2FF8E143DA58C)

### A RE-IMPLEMENTATION
- Take an academic paper or other pre-existing project and implement it, or a portion of it.
- Examples:
  - [2D Wavefunction Collapse Pokémon Town](https://gurtd.github.io/566-final-project/)
  - [3D Wavefunction Collapse Dungeon Generator](https://github.com/whaoran0718/3dDungeonGeneration)
  - [Reaction Diffusion](https://github.com/charlesliwang/Reaction-Diffusion)
  - [WebGL Erosion](https://github.com/LanLou123/Webgl-Erosion)
  - [Particle Waterfall](https://github.com/chloele33/particle-waterfall)
  - [Voxelized Bread](https://github.com/ChiantiYZY/566-final)

### A FORGERY
Taking inspiration from a particular natural phenomenon or distinctive set of visuals, implement a detailed, procedural recreation of that aesthetic. This includes modeling, texturing and object placement within your scene. Does not need to be real-time. Focus on detail and visual accuracy in your implementation.
- Examples:
  - [The Shrines](https://github.com/byumjin/The-Shrines)
  - [Watercolor Shader](https://github.com/gracelgilbert/watercolor-stylization)
  - [Sunset Beach](https://github.com/HanmingZhang/homework-final)
  - [Sky Whales](https://github.com/WanruZhao/CIS566FinalProject)
  - [Snail](https://www.shadertoy.com/view/ld3Gz2)
  - [Journey](https://www.shadertoy.com/view/ldlcRf)
  - [Big Hero 6 Wormhole](https://2.bp.blogspot.com/-R-6AN2cWjwg/VTyIzIQSQfI/AAAAAAAABLA/GC0yzzz4wHw/s1600/big-hero-6-disneyscreencaps.com-10092.jpg)

### A GAME LEVEL
- Like generations of game makers before us, create a game which generates an navigable environment (eg. a roguelike dungeon, platforms) and some sort of goal or conflict (eg. enemy agents to avoid or items to collect). Aim to create an experience that will challenge players and vary noticeably in different playthroughs, whether that means procedural dungeon generation, careful resource management or an interesting AI model. Focus on designing a system that is capable of generating complex challenges and goals.
- Examples:
  - [Rhythm-based Mario Platformer](https://github.com/sgalban/platformer-gen-2D)
  - [Pokémon Ice Puzzle Generator](https://github.com/jwang5675/Ice-Puzzle-Generator)
  - [Abstract Exploratory Game](https://github.com/MauKMu/procedural-final-project)
  - [Tiny Wings](https://github.com/irovira/TinyWings)
  - Spore
  - Dwarf Fortress
  - Minecraft
  - Rogue

### AN ANIMATED ENVIRONMENT / MUSIC VISUALIZER
- Create an environment full of interactive procedural animation. The goal of this project is to create an environment that feels responsive and alive. Whether or not animations are musically-driven, sound should be an important component. Focus on user interactions, motion design and experimental interfaces.
- Examples:
  - [The Darkside](https://github.com/morganherrmann/thedarkside)
  - [Music Visualizer](https://yuruwang.github.io/MusicVisualizer/)
  - [Abstract Mesh Animation](https://github.com/mgriley/cis566_finalproj)
  - [Panoramical](https://www.youtube.com/watch?v=gBTTMNFXHTk)
  - [Bound](https://www.youtube.com/watch?v=aE37l6RvF-c)

### YOUR OWN PROPOSAL
- You are of course welcome to propose your own topic . Regardless of what you choose, you and your team must research your topic and relevant techniques and come up with a detailed plan of execution. You will meet with some subset of the procedural staff before starting implementation for approval.
