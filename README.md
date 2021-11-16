# Final Project!

This is it! The culmination of your procedural graphics experience this semester. For your final project, we'd like to give you the time and space to explore a topic of your choosing. You may choose any topic you please, so long as you vet the topic and scope with an instructor or TA. We've provided some suggestions below. The scope of your project should be roughly 1.5 homework assignments). To help structure your time, we're breaking down the project into 4 milestones:

## Milestone 1: Project planning (due 11/15)
Before submitting your first milestone, _you must get your project idea and scope approved by Rachel, Adam or a TA._

### Design Doc
Start off by forking this repository. In your README, write a design doc to outline your project goals and implementation plan. It must include the following sections:

#### Introduction
Ashley and I plan to build a procedural dragonfly generator in Houdini, in the hopes that we will gain Houdini expertise and have an exportable dragonfly asset at the end. We were inspired by the terrain generation Houdini project to seek further familiarity with Houdini, given that it is an industry standard and a great procedural tool. We noticed that dragonflies’ core features stay consistent, but there are minute differences in the color of the bodies and the branching veins of the wings. We therefore thought that the dragonfly would be a good subject for a procedural asset generator in Houdini.
#### Goal
Our goal is to create a dragonfly generator in Houdini. We want to allow artists to be able to create various different dragonflies by tweaking hda parameters. We want the shape of the body, the wings' shape size and features, as well as the colors of the dragonfly to be editable. 
At the end, we want to have some nice rendered images of various generated dragonflies, as well as an exportable asset that you could theoretically render with a different engine, if desired. We also want to ensure that we have an hda that could be used in any Houdini project.


#### Inspiration/reference:
Our inspiration is images of both real life dragonflies as well as drawings or pictures of the creatures that better showcase some of their details. We were also inspired by the game Spore. 

![](images/wings.jpg)

![](images/dragonfly1.jpg)

![](images/dragonfly2.jpg)

![](images/dragonfly3.jpg)


https://www.youtube.com/watch?v=9U_9SErk9xU This is a Houdini walkthrough of a butterfly that we referenced

#### Specification:
Main features include the body shape (main body, eyes, legs, and head), the wing shape, the wing pattern, and the shader. 
Emma will focus on creating the body and wing shape. Ashley will create the wing pattern and we will both work together to create the dragonfly shader. 


#### Techniques:
For the body and wing shapes the techniques used will mostly be related to solving problems in Houdini. Vex will be used to make the model more procedural but it will mostly consist of editing various houdini primitives and using nodes such as transforms, for loops, and curves. There will not be any imported models in this project instead all aspects of the dragonfly will be modeled procedurally with houdini in order to add maximum customization for the user. 
The shader for the dragon will require the use of iridescence on the body and the wings as well as potentially some form of glass for the see through elements on the wings. 
The initial wing veins will be some sort of LSystem structure projected onto the wing shape (following the wing shape, if possible). The LSystem will split the wing into different primitives, and we will use a foreach loop to create a voronoi pattern on each primitive, either with the built-in voronoi node or with vex. 


#### Design:

![](images/graph.jpg)

#### Timeline:

#### PreWeek One:

Ashley and Emma
- Research Houdini techniques for the shape and pattern generation in order to see if it would be possible to create in houdini or if we should use WebGL
- Find Houdini tutorial videos that relate to different aspects of our dragonfly generator
- Test wing branching method with voronoi and lsystem nodes
#### Week One:

- Emma:
  - Create single version of body including head, eyes, legs, abdomen, keeping in mind which values will be parameterized upon the creation of the hda
  - Create two different wings (one top wing and one bottom wing) using simple primitives combined together.
- Emma + Ashley:
  - test render with basic shader in order to make sure rendering HDA with a material works
  - Research iridescence for the wing shader
- Ashley:
  - Create lsystem that will partly follow the edge of whatever 2D mesh it’s bound to. The branches of this lsystem should extend to the edges of the bound mesh, but go no further.
  - Project the lsystem down onto the wing shape mesh (just a basic circle or oval for now)
  - Split the wing shape mesh by the lsystem
  - For each created mesh, scatter points and create voronoi system. Then, get the outline of the voronoi system and create small tubes.
#### Week Two:
- Emma:
  - Bug fixes from Week 1
  - Refine wing shape and add more detail to the overall shape
  - Add parameters to wing shape so that multiple variations can be created
- Ashley:
  - Bug fixes from Week 1
  - If the lsystem doesn’t follow the shape of the wing, work on that
  - Add iridescent shader to wings
  - Add wing branching parameters
- Ashley and Emma:
   - Procedural pattern generation for the body (and potentially wings as well)
   - Place wing pattern generation on actual wings. 
   - Create first draft of shader for dragonfly
   - Test renders
#### Week Three
- Ashley and Emma
  - Create hda with parameters for the rest of the body
  - Refine generator based on feedback
  - Refine shader - add parameters to shader
  - Final Renders


Submit your Design doc as usual via pull request against this repository.
## Milestone 2: Implementation part 1 (due 11/22)
Begin implementing your engine! Don't worry too much about polish or parameter tuning -- this week is about getting together the bulk of your generator implemented. By the end of the week, even if your visuals are crude, the majority of your generator's functionality should be done.

Put all your code in your forked repository.

Submission: Add a new section to your README titled: Milestone #1, which should include
- written description of progress on your project goals. If you haven't hit all your goals, what's giving you trouble?
- Examples of your generators output so far
We'll check your repository for updates. No need to create a new pull request.
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
