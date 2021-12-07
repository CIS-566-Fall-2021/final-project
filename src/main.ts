import {vec3} from 'gl-matrix';
import * as Stats from 'stats-js';
import * as DAT from 'dat-gui';
import Square from './geometry/Square';
import ScreenQuad from './geometry/ScreenQuad';
import OpenGLRenderer from './rendering/gl/OpenGLRenderer';
import Camera from './Camera';
import {setGL} from './globals';
import ShaderProgram, {Shader} from './rendering/gl/ShaderProgram';

// Define an object with application parameters and button callbacks
// This will be referred to by dat.GUI's functions that add GUI elements.
const controls = {
};

let pathSymbol: string = '_';
let wallSymbol: string = 'x';
let obstacleSymbol1 = '1';
let obstacleSymbol2 = '2';
let obstacleSymbol3 = '3';
let startSymbol = '*';
let endsSymbol = '$';
let textFilePath: string = 'dungeon.txt';
let center: number[] = new Array();

let wallTile: Square;
let pathTile: Square;
let obstacleTile: Square;
let startTile: Square;
let endTile: Square;
let screenQuad: ScreenQuad;
let time: number = 0.0;
let usedSquares: Square[];
let numberToCoords: Map<number, [number, number]>;
let coordsToSquare: Map<[number, number], Square>;

function loadTexture(gl: WebGL2RenderingContext, url: string) {
  const texture = gl.createTexture();
  gl.bindTexture(gl.TEXTURE_2D, texture);

  // Because images have to be downloaded over the internet
  // they might take a moment until they are ready.
  // Until then put a single pixel in the texture so we can
  // use it immediately. When the image has finished downloading
  // we'll update the texture with the contents of the image.
  const level = 0;
  const internalFormat = gl.RGBA;
  const width = 1;
  const height = 1;
  const border = 0;
  const srcFormat = gl.RGBA;
  const srcType = gl.UNSIGNED_BYTE;
  const pixel = new Uint8Array([0, 0, 255, 255]);  // opaque blue
  gl.texImage2D(gl.TEXTURE_2D, level, internalFormat,
                width, height, border, srcFormat, srcType,
                pixel);

  const image = new Image();
  image.onload = function() {
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texImage2D(gl.TEXTURE_2D, level, internalFormat,
                  srcFormat, srcType, image);

    // WebGL1 has different requirements for power of 2 images
    // vs non power of 2 images so check if the image is a
    // power of 2 in both dimensions.
    if (isPowerOf2(image.width) && isPowerOf2(image.height)) {
       // Yes, it's a power of 2. Generate mips.
       gl.generateMipmap(gl.TEXTURE_2D);
    } else {
       // No, it's not a power of 2. Turn off mips and set
       // wrapping to clamp to edge
       gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
       gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
       gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    }
  };
  image.src = url;

  return texture;
}

function isPowerOf2(value: number) {
  return (value & (value - 1)) == 0;
}

function readTextFile(file: string): string {
  var text = "";
  var rawFile = new XMLHttpRequest();
  rawFile.open("GET", file, false);
  rawFile.onreadystatechange = function ()
  {
      if(rawFile.readyState === 4)
      {
          if(rawFile.status === 200 || rawFile.status == 0)
          {
              var allText = rawFile.responseText;
              text = allText;
          }
      }
  }
  rawFile.send(null);
  return text;
}

function loadScene(gl: WebGL2RenderingContext) {

  const texture = loadTexture(gl, 'src/assets/basictex.png');

  // Tell WebGL we want to affect texture unit 0
  gl.activeTexture(gl.TEXTURE0);

  // Bind the texture to texture unit 0
  gl.bindTexture(gl.TEXTURE_2D, texture);

  screenQuad = new ScreenQuad();
  screenQuad.create();
  startTile = new Square();
  startTile.create();
  endTile = new Square();
  endTile.create();
  wallTile = new Square();
  wallTile.create();
  pathTile = new Square();
  pathTile.create();
  obstacleTile = new Square();
  obstacleTile.create();


  let dungeonString = readTextFile(textFilePath);

  let dungeonArray = new Array();
  let row = new Array();

  for (let i = 0; i < dungeonString.length; i++) {
    if (dungeonString[i] === '\n') {
      row.pop();
      row.pop();
      dungeonArray.push(row);
      row = [];
    }
    else {
      row.push(dungeonString[i]);
    }
  }
  dungeonArray.pop();

  let mapWidth = dungeonArray.length;
  let mapHeight = dungeonArray[0].length;

  center.push(mapWidth);
  center.push(mapHeight);

  let pathCount = 0;
  let wallCount = 0;
  let obstacleCount = 0;

  let startOffsetArray = [];
  let endOffsetArray = [];
  let pathOffsetsArray = [];
  let wallOffsetsArray = [];
  let obstacleOffsetsArray = [];

  let startUVArray = [];
  let endUVArray = [];
  let pathUVArray = [];
  let wallUVArray = [];
  let obstacleUVArray = [];

  for (let i = 0; i < mapWidth; i++) {
    for(let j = 0; j < mapHeight; j++) {
      let symbol = dungeonArray[i][j];
      if (symbol === startSymbol) {
        startOffsetArray.push(i)
        startOffsetArray.push(j);
        startOffsetArray.push(0);
        startUVArray.push(0.0, 0.25, 0.25, 0.25, 0.25, 0.5, 0.0, 0.5);
      }
      if (symbol === endsSymbol) {
        endOffsetArray.push(i, j, 0);
        endUVArray.push(0.25, 0.25, 0.5, 0.25, 0.5, 0.5, 0.25, 0.5);
      }
      if (symbol === pathSymbol) {
        pathCount++;
        pathOffsetsArray.push(i);
        pathOffsetsArray.push(j);
        pathOffsetsArray.push(0);
        pathUVArray.push(0.25, 0.0, 0.5, 0.0, 0.5, 0.25, 0.25, 0.25);
      }
      if (symbol === wallSymbol) {
        wallCount++;
        wallOffsetsArray.push(i);
        wallOffsetsArray.push(j);
        wallOffsetsArray.push(0);
        wallUVArray.push(0.0, 0.0, 0.25, 0.0, 0.25, 0.25, 0.0, 0.25);
      }
        if (obstacleSymbol1 === symbol) {
          obstacleCount++;
          obstacleOffsetsArray.push(i);
          obstacleOffsetsArray.push(j);
          obstacleOffsetsArray.push(0);
          obstacleUVArray.push(0.5, 0.0, 0.75, 0.0, 0.75, 0.25, 0.5, 0.25);
        }
      
        if (obstacleSymbol2 === symbol) {
          obstacleCount++;
          obstacleOffsetsArray.push(i);
          obstacleOffsetsArray.push(j);
          obstacleOffsetsArray.push(0);
          obstacleUVArray.push(0.5, 0.0, 0.75, 0.0, 0.75, 0.25, 0.5, 0.25);
        }
      
        if (obstacleSymbol3 === symbol) {
          obstacleCount++;
          obstacleOffsetsArray.push(i);
          obstacleOffsetsArray.push(j);
          obstacleOffsetsArray.push(0);
          obstacleUVArray.push(0.5, 0.0, 0.75, 0.0, 0.75, 0.25, 0.5, 0.25);
        }
    }
    
  }
  let startOffset: Float32Array = new Float32Array(startOffsetArray);
  let endOffset: Float32Array = new Float32Array(endOffsetArray);
  let pathOffsets: Float32Array = new Float32Array(pathOffsetsArray);
  let wallOffsets: Float32Array = new Float32Array(wallOffsetsArray);
  let obstacleOffsets: Float32Array = new Float32Array(obstacleOffsetsArray);

  let startUV: Float32Array = new Float32Array(startUVArray);
  let endUV: Float32Array = new Float32Array(endUVArray);
  let pathUVs: Float32Array = new Float32Array(pathUVArray);
  let wallUVs: Float32Array = new Float32Array(wallUVArray);
  let obstacleUVs: Float32Array = new Float32Array(obstacleUVArray);

  startTile.setUVs(startUV);
  startTile.setInstanceVBOs(startOffset);
  startTile.setNumInstances(1);

  endTile.setUVs(endUV);
  endTile.setInstanceVBOs(endOffset);
  endTile.setNumInstances(1);

  pathTile.setUVs(pathUVs);
  pathTile.setInstanceVBOs(pathOffsets);
  pathTile.setNumInstances(pathCount);
  
  wallTile.setUVs(wallUVs);
  wallTile.setInstanceVBOs(wallOffsets);
  wallTile.setNumInstances(wallCount);

  obstacleTile.setUVs(obstacleUVs);
  obstacleTile.setInstanceVBOs(obstacleOffsets);
  obstacleTile.setNumInstances(obstacleCount);

}

function main() {
  // Initial display for framerate
  const stats = Stats();
  stats.setMode(0);
  stats.domElement.style.position = 'absolute';
  stats.domElement.style.left = '0px';
  stats.domElement.style.top = '0px';
  document.body.appendChild(stats.domElement);

  // Add controls to the gui
  const gui = new DAT.GUI();

  // get canvas and webgl context
  const canvas = <HTMLCanvasElement> document.getElementById('canvas');
  const gl = <WebGL2RenderingContext> canvas.getContext('webgl2');
  if (!gl) {
    alert('WebGL 2 not supported!');
  }
  // `setGL` is a function imported above which sets the value of `gl` in the `globals.ts` module.
  // Later, we can import `gl` from `globals.ts` to access it
  setGL(gl);

  // Initial call to load scene
  loadScene(gl);

  const camera = new Camera(vec3.fromValues(center[0] / 2, center[1] / 2, 10), vec3.fromValues(center[0] / 2, center[1] / 2, 0));

  const renderer = new OpenGLRenderer(canvas);
  renderer.setClearColor(0.2, 0.2, 0.2, 1);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

  const instancedShader = new ShaderProgram([
    new Shader(gl.VERTEX_SHADER, require('./shaders/instanced-vert.glsl')),
    new Shader(gl.FRAGMENT_SHADER, require('./shaders/instanced-frag.glsl')),
  ]);

  const flat = new ShaderProgram([
    new Shader(gl.VERTEX_SHADER, require('./shaders/flat-vert.glsl')),
    new Shader(gl.FRAGMENT_SHADER, require('./shaders/flat-frag.glsl')),
  ]);

  // This function will be called every frame
  function tick() {
    camera.update();
    stats.begin();
    instancedShader.setTime(time);
    flat.setTime(time++);
    gl.viewport(0, 0, window.innerWidth, window.innerHeight);
    renderer.clear();
    renderer.render(camera, flat, [screenQuad]);
    renderer.render(camera, instancedShader, [
      pathTile, wallTile, obstacleTile,
    ]);
    stats.end();

    // Tell the browser to call `tick` again whenever it renders a new frame
    requestAnimationFrame(tick);
  }

  window.addEventListener('resize', function() {
    renderer.setSize(window.innerWidth, window.innerHeight);
    camera.setAspectRatio(window.innerWidth / window.innerHeight);
    camera.updateProjectionMatrix();
    flat.setDimensions(window.innerWidth, window.innerHeight);
  }, false);

  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.setAspectRatio(window.innerWidth / window.innerHeight);
  camera.updateProjectionMatrix();
  flat.setDimensions(window.innerWidth, window.innerHeight);

  // Start the render loop
  tick();
}

main();
