#version 300 es
precision highp float;

// The vertex shader used to render the background of the scene
uniform mat4 u_Model;   
uniform mat4 u_ViewProj; 

in vec4 vs_Pos;
out vec4 fs_Pos;

void main() {
  // fs_Pos = vs_Pos;
  // gl_Position = vs_Pos;
  vec4 modelposition = u_Model * vs_Pos;   // Temporarily store the transformed vertex positions for use below
  gl_Position = u_ViewProj * modelposition;
}
