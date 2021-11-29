# Topdown Dungeon Generator

## Milestone 1 - Proposal
#### Introduction
In this project I will be implementing a topdown dungeon generator in Unity using Wave Function Collapse. I am interested in video game development and was curious about how dungeons were being generated in Roguelikes / Roguelites. Through this project I hope to gain exposure in procedural generation techniques for maps and dungeons.

#### Goal
The main goal is to create a topdown dungeon generator that generates at runtime, using tiles. A secondary goal is to create collisions for the walls and make a simple game using the generated dungeons.

#### Inspiration/reference:
[Martin Donald's Superpositions, Sudoku, the Wave Function Collapse algorithm](https://www.youtube.com/watch?v=2SuvO4Gi7uY)

[Robert Heaton's Wave Function Collapse Explained](https://robertheaton.com/2018/12/17/wavefunction-collapse-algorithm/)

##### Overworld generation in Caves of Qud
![](/img/cavesOfQudImage.png)

##### Dungeon generation in Moonlighter (not necessarily from WFC)
![](/img/moonlighterImage.jpg)

#### Specification and Features:
* Runtime generation of a tile based, topdown dungeon using WFC trained on a tileset.
* If time allows, the player will be able to move a character around the dungeon, which will have collisions for bounds.
* If time allows, player will be able to fight enemies in the dungeon.

#### Techniques:
The core of this project will be an implementation of Wave Function Collapse, an algorithm for procedurally generating textures or tilemaps using a small input texture or tileset ([WFC overview](https://github.com/mxgmn/WaveFunctionCollapse)). The algorithm will be given a tileset where each tile has a constraint on the types of tiles that could be adjacent to it. The dungeon will consist of a large tilemap, where each tile in the tilemap will begin as a superposition (all tiles could possibly be in this spot), and WFC will begin choosing specific tiles for these spots and propagating adjacency constraints until each superposition has collapsed into a single, specific tile.

#### Design:
A tileset along with tile constraints will be fed into the WFC algorithm / tilemap generator. The generator will then modify a Unity tilemap at runtime, editing specific tiles of the tilemap as the possibilities of tiles collapse. This Unity tilemap will then be used in the game. If time allows, tilemap colliders will be created using Unity's builtin Tilemap Collider 2D component. A player character and enemies may also be added into the game.

![](/img/CIS566FinalProjectDiagram.png)

* Diagram of core components

#### Timeline:
* 11/15 - 11/22: Implement core functionality of WFC. Should be able to generate dungeons.
* 11/22 - 11/29: Fix bugs and if possible add player character and enemies.
* 11/29 - 12/6: Add particle effects and GUI.

## Milestone 2 - Implementation
#### Progress:
I was able to implement most of the core functionality of my map (instead of dungeon as it has become more general) generator. I decided to design the generator to accept any input tilemap consisting of any tileset instead of designing the generator around a specific tileset. This was a good decision since it increases the versatility of the generator, making it reusable across projects.

#### Setbacks:
There is a bug where sometimes WFC will converge instantly. Not sure how to reproduce it, but I'm confident I can fix it. I am also considering to implement backtracking or not. Right now I am solving neighbor conflicts by setting conflicting tiles to a user defined fallback tile, but this will lead to inconsistent generated maps depending on the input tilemap.

#### Results:
##### Grasslands Input
![](/img/GrasslandsInput.png)

##### Grasslands Output
![](/img/GeneratorGrasslands.png)

##### Dungeon Input
![](/img/dungeonInput.png)

##### Dungeon Output
![](/img/GeneratorDungeon.png)

[Tileset from jamiebrownhill](https://jamiebrownhill.itch.io/solaria-demo)

## Milestone 3 - Bugfixes and Features
#### Progress:
I was able to fix the bug in milestone 2 and also added in a form of backtracking. I originally wanted the generator to backtrack to the immediate, previous board whenever a conflict was made, and track "bad boards" by storing them into a hashset, but realized that this was very inefficient for large outputs and would take a very large amount of iterations to converge (>3000 iterations). Instead whenever there is a conflict the board will backtrack half the amount of steps it took from the beginning to the conflict. From very limited testing on an input tilemap that was prone to conflicts without backtracking, the board was able to converge every time with this backtracking implementation. In the event that the board cannot converge the program will report failure by showing the incomplete output (it will not crash).

I refined the map generation by choosing blank tiles with the least entropy (least number of remaining tiles in superposition) to randomly assign a tile to. I also added a weighted option to the generation. By weighting how WFC randomly assigns tiles to based on the frequency they show up in the input tilemap, the output will more closely match the input.

##### Town Input
![](/img/townInput.png)

##### Weighted (left) vs. Unweighted (right) Output
<img src="/img/townOutputWeighted.png" width="40%"/> <img src="/img/townOutputUnweighted.png" width="40%"/>

##### Dungeon Input
![](/img/dungeonInput.png)

##### Dungeon Output (weighted)
![](/img/dungeonOutputWeighted.png)

##### Islands Input
![](/img/islandsInput.png)

##### Islands Output (weighted)
![](/img/islandsOutputWeighted.png)

I also added a UI for the program. Right now the user can see the input and output tilemaps, change the input tilemap to one of three options using a dropdown menu, change whether to use weighted generation or not, and recalculate the board.

##### Program in Action
![](/img/generatorInAction.gif)

Instead of creating a game using my WFC implementation I decided to create a program that allows the user to generate tilemaps. I was more interested in the interactavity of tilemap generation. I plan to allow the user to paint input tilemaps using the three existing tilesets, and if time permits, allow them to constrain the output by painting tiles in the output before generation. Apart from these extra features, I've accomplished what I sought to do.

## Credits
[Dungeon and Islands tilemaps made with tileset from jamiebrownhill](https://jamiebrownhill.itch.io/solaria-demo)
[UI and Town tilemap made with tilesets from KenneyNL](https://kenney.nl/)

#### Helpful References
[Martin Donald's Superpositions, Sudoku, the Wave Function Collapse algorithm](https://www.youtube.com/watch?v=2SuvO4Gi7uY)
[Robert Heaton's Wave Function Collapse Explained](https://robertheaton.com/2018/12/17/wavefunction-collapse-algorithm/)
[WFC Tilemap Implementation Steps from Rémy Devaux](https://trasevol.dog/2017/09/01/di19/)
[WFC Tips and Tricks from BorisTheBrave](https://www.boristhebrave.com/2020/02/08/wave-function-collapse-tips-and-tricks/)
