#version 300 es
precision highp float;

uniform sampler2D u_Sampler;

in vec4 fs_Col;
in vec4 fs_Pos;
in vec2 fs_UV;

out vec4 out_Col;

void main()
{
    out_Col = texture(u_Sampler, fs_UV);
    //out_Col = vec4(1.0, 1.0, 1.0, 1.0);
}
