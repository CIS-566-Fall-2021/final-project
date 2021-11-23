import {vec2, vec3, vec4, mat4} from 'gl-matrix';
import Drawable from './Drawable';
import {gl} from '../../globals';

var activeProgram: WebGLProgram = null;

export class Shader {
  shader: WebGLShader;
  constructor(type: number, source: string) {
    this.shader = gl.createShader(type);
    gl.shaderSource(this.shader, source);
    gl.compileShader(this.shader);

    if (!gl.getShaderParameter(this.shader, gl.COMPILE_STATUS)) {
      throw gl.getShaderInfoLog(this.shader);
    }
  }
};

class ShaderProgram {
  prog: WebGLProgram;

  attrPos: number;
  attrNor: number;
  attrUV: number;

  unifRef: WebGLUniformLocation;
  unifEye: WebGLUniformLocation;
  unifUp: WebGLUniformLocation;
  unifDimensions: WebGLUniformLocation;
  unifTime: WebGLUniformLocation;
  unifTexture: WebGLUniformLocation;
  unifViewProj: WebGLUniformLocation;
  unifBirdParams: WebGLUniformLocation;

  colorTexture : WebGLUniformLocation;
  frameBuffer : WebGLUniformLocation;
  targetTexture : WebGLUniformLocation;
  targetTextureWidth : number;
  targetTextureHeight : number;
  devicePixelRatio : number;

  innerWidth : number;
  innerHeight : number;
  frameBufferBound : boolean = false;

  constructor(shaders: Array<Shader>) {
    this.prog = gl.createProgram();

    for (let shader of shaders) {
      gl.attachShader(this.prog, shader.shader);
    }
    gl.linkProgram(this.prog);
    if (!gl.getProgramParameter(this.prog, gl.LINK_STATUS)) {
      throw gl.getProgramInfoLog(this.prog);
    }

    this.attrPos = gl.getAttribLocation(this.prog, "vs_Pos");
    this.attrUV = gl.getAttribLocation(this.prog, "vs_UV");

    this.unifEye   = gl.getUniformLocation(this.prog, "u_Eye");
    this.unifRef   = gl.getUniformLocation(this.prog, "u_Ref");
    this.unifUp   = gl.getUniformLocation(this.prog, "u_Up");
    this.unifDimensions   = gl.getUniformLocation(this.prog, "u_Dimensions");
    this.unifTime   = gl.getUniformLocation(this.prog, "u_Time");
    this.unifTexture   = gl.getUniformLocation(this.prog, "u_Texture");
    this.unifViewProj   = gl.getUniformLocation(this.prog, "u_ViewProj");
    this.unifBirdParams   = gl.getUniformLocation(this.prog, "u_BirdParameters");

    this.devicePixelRatio = 1.0;

  }

  use() {
    if (activeProgram !== this.prog) {
      gl.useProgram(this.prog);
      activeProgram = this.prog;
    }
  }

  setEyeRefUp(eye: vec3, ref: vec3, up: vec3) {
    this.use();
    if(this.unifEye !== -1) {
      gl.uniform3f(this.unifEye, eye[0], eye[1], eye[2]);
    }
    if(this.unifRef !== -1) {
      gl.uniform3f(this.unifRef, ref[0], ref[1], ref[2]);
    }
    if(this.unifUp !== -1) {
      gl.uniform3f(this.unifUp, up[0], up[1], up[2]);
    }
  }

  setDimensions(width: number, height: number) {
    this.use();
    if(this.unifDimensions !== -1) {
      gl.uniform2f(this.unifDimensions, width, height);
    }
  }

  setTime(t: number) {
    this.use();
    if(this.unifTime !== -1) {
      gl.uniform1f(this.unifTime, t);
    }
  }

  setViewProjMatrix(vp: mat4) {
    this.use();
    if (this.unifViewProj !== -1) {
      //console.log("setting viewproj")
      gl.uniformMatrix4fv(this.unifViewProj, false, vp);
    }
  }


  setBirdParams(params:Array<number>) {
    this.use();
    if (this.unifBirdParams !== -1) {
      console.log("setting birdparams")
      gl.uniform1fv(this.unifBirdParams, params, 0, 20)
    }
  }

  setSize(width:number, height:number) {
    this.innerWidth = width;
    this.innerHeight = height;
  }


  draw(d: Drawable) {
    this.use();

    if (this.attrPos != -1 && d.bindPos()) {
      gl.enableVertexAttribArray(this.attrPos);
      gl.vertexAttribPointer(this.attrPos, 4, gl.FLOAT, false, 0, 0);
    }

    if (this.attrUV != -1 && d.bindUV()) {
      gl.enableVertexAttribArray(this.attrUV);
      gl.vertexAttribPointer(this.attrUV, 2, gl.FLOAT, false, 0, 0);
    }

    if (this.unifTexture != -1) {
      gl.activeTexture(gl.TEXTURE0); //GL supports up to 32 different active textures at once(0 - 31)
      gl.bindTexture(gl.TEXTURE_2D, this.colorTexture);
      gl.uniform1i(this.unifTexture, 0);
    }

    d.bindIdx();

    if(this.frameBufferBound) {
      // render to our targetTexture by binding the framebuffer
      gl.bindFramebuffer(gl.FRAMEBUFFER, this.frameBuffer);
      gl.bindTexture(gl.TEXTURE_2D, this.targetTexture);
      let aspect = this.innerWidth / this.innerHeight;
      gl.viewport(0, 0, this.innerWidth, this.innerHeight);

      // Tell WebGL how to convert from clip space to pixels

      // Clear the attachment(s).
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    } else {
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      gl.viewport(0, 0, this.innerWidth, this.innerHeight);

      let aspect = this.innerWidth / this.innerHeight;
     // console.log(aspect)
      let projectionMatrix = mat4.create();
      mat4.perspective(projectionMatrix, 60, aspect, 0.0, 0.3);
      //console.log(projectionMatrix)
      this.setViewProjMatrix(projectionMatrix)
    }

    gl.drawElements(d.drawMode(), d.elemCount(), gl.UNSIGNED_INT, 0);

    if (this.attrPos != -1) gl.disableVertexAttribArray(this.attrPos);
  }

  setBaseColorTexture(texture:WebGLUniformLocation) {
    this.use();
    this.colorTexture = texture;
    gl.uniform1i(this.unifTexture, 0);
  }

 frameBufferResize() {
    gl.viewport(0, 0, this.innerWidth, this.innerHeight);
    gl.bindTexture(gl.TEXTURE_2D, this.targetTexture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, this.innerWidth, 
      this.innerHeight, 0, gl.RGB, gl.UNSIGNED_BYTE, null);

 }
 
  createFrameBuffer() {
        // create to render to
    this.targetTexture = gl.createTexture();
    this.frameBuffer = gl.createFramebuffer();
    gl.bindFramebuffer(gl.FRAMEBUFFER, this.frameBuffer)

    this.targetTextureWidth = this.innerWidth;
    this.targetTextureHeight = this.innerHeight;

    gl.bindTexture(gl.TEXTURE_2D, this.targetTexture);
    // define size and format of level 0
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, this.innerWidth, 
      this.innerHeight, 0, gl.RGB, gl.UNSIGNED_BYTE, null);


    // gl.texImage2D(gl.TEXTURE_2D, level, internalFormat,
    //               this.innerWidth * devicePixelRatio, this.innerHeight * devicePixelRatio, border,
    //               format, type, texData);
  
    // set the filtering so we don't need mips
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);

    // Create and bind the framebuffer
    gl.bindFramebuffer(gl.FRAMEBUFFER, this.frameBuffer);
    gl.viewport(0, 0, this.targetTextureWidth, this.targetTextureHeight);
    this.frameBufferBound = true;

    // attach the texture as the first color attachment
    gl.framebufferTexture2D(
    gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, this.targetTexture, 0);
  
  }
};



export default ShaderProgram;
