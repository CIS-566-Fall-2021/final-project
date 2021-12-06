#version 300 es

// This is a fragment shader. If you've opened this file first, please
// open and read lambert.vert.glsl before reading on.
// Unlike the vertex shader, the fragment shader actually does compute
// the shading of geometry. For every pixel in your program's output
// screen, the fragment shader is run for every bit of geometry that
// particular pixel overlaps. By implicitly interpolating the position
// data passed into the fragment shader by the vertex shader, the fragment shader
// can compute what color to apply to its pixel based on things like vertex
// position, light position, and vertex color.
precision highp float;

uniform mat4 u_Model;
uniform vec4 u_Color; // The color with which to render this instance of geometry.
uniform vec3 u_DistFromStart;
uniform float u_ForestRadius;

// These are the interpolated values out of the rasterizer, so you can't know
// their specific values without knowing the vertices that contributed to them
in vec4 fs_Pos;
in vec4 fs_Nor;
in vec4 fs_LightVec;
in vec4 fs_Col;

out vec4 out_Col; // This is the final output color that you will see on your
                  // screen for the pixel that is currently being processed.
                //  out vec2 fs_UV;

vec3 vertexHeightNoise(vec3 position) {   
    float noise = sin(position.x + position.z);

    // recalculate the y value same as it was perturbed in terrain class
    vec3 noisyModelPosition = vec3(position.x, noise, position.z);

    return noisyModelPosition;
}

vec4 getNewNormal(vec4 norm) {
    float epsilon = 0.08;

    vec3 tangent = normalize(cross(vec3(0.0, 1.0, 0.0), vec3(norm)));
    vec3 bitangent = cross(vec3(norm), tangent);

    vec3 point1 = vertexHeightNoise(fs_Pos.xyz + epsilon * tangent);
    vec3 point2 = vertexHeightNoise(fs_Pos.xyz + epsilon * bitangent);
    vec3 point3 = vertexHeightNoise(fs_Pos.xyz - epsilon * tangent);
    vec3 point4 = vertexHeightNoise(fs_Pos.xyz - epsilon * bitangent);
    
    return vec4(normalize(cross(normalize(point1 - point3), normalize(point2 - point4))), 0.0);
    //return vec4(normalize(cross(normalize(pos))))
} 

float random3D(vec3 p) {
    return sin(length(vec3(fract(dot(p, vec3(16.1, 121.8, 160.2))), 
                            fract(dot(p, vec3(12.5, 161.3, 160.4))),
                            fract(dot(p, vec3(16.4, 161.2, 122.5))))) * 439.90906);
}


float interpolateNoise3D(float x, float y, float z)
{
    int intX = int(floor(x));
    float fractX = fract(x);
    int intY = int(floor(y));
    float fractY = fract(y);
    int intZ = int(floor(z));
    float fractZ = fract(z);

    float v1 = random3D(vec3(intX, intY, intZ));
    float v2 = random3D(vec3(intX + 1, intY, intZ));
    float v3 = random3D(vec3(intX, intY + 1, intZ));
    float v4 = random3D(vec3(intX + 1, intY + 1, intZ));

    float v5 = random3D(vec3(intX, intY, intZ + 1));
    float v6 = random3D(vec3(intX + 1, intY, intZ + 1));
    float v7 = random3D(vec3(intX, intY + 1, intZ + 1));
    float v8 = random3D(vec3(intX + 1, intY + 1, intZ + 1));


    float i1 = mix(v1, v2, fractX);
    float i2 = mix(v3, v4, fractX);

    //mix between i1 and i2
    float i3 = mix(i1, i2, fractY);

    float i4 = mix(v5, v6, fractX);
    float i5 = mix(v7, v8, fractX);

    //mix between i3 and i4
    float i6 = mix(i4, i5, fractY);

    //mix between i3 and i6
    float i7 = mix(i3, i6, fractZ);

    return i7;
}

float fbmNoise(float x, float y, float z)
{
    float total = 0.0;
    float persistence = 0.1;
    float frequency = 0.1;
    float amplitude = 0.5;
    int octaves = 2;

    for (int i = 1; i <= octaves; i++) {
        total += amplitude * interpolateNoise3D(frequency * x, frequency * y, frequency * z);
        frequency *= 1.0;
        amplitude *= persistence;
    }
    return total;
}

float getBias(float time, float bias)
{
  return (time / ((((1.0/bias) - 2.0)*(1.0 - time))+1.0));
}

float getGain(float time, float gain)
{
    if(time < 0.5) {
        return getBias(time * 2.0, gain) / 2.0;
    } else {
        return getBias(time * 2.0 - 1.0,1.0 - gain)/2.0 + 0.5;
    }
}

vec4 generateColor(vec4 col) {
  float noisedValue = fbmNoise(fs_Pos.x, fs_Pos.y, fs_Pos.z);
  float bias = getBias(noisedValue, 0.3);

  vec3 mixColor = vec3(31.0, 181.0, 123.0) / 255.0;
  return mix(col, vec4(mixColor, 1.0), bias);
  // if (noisedValue < 0.5) {
  //   return col;
  // } else {
  //   return mix(vec4(1,1,1,1));
  // }
}

void main()
{
    // Material base color (before shading)
    vec4 newColor = generateColor(fs_Col);

        vec4 inverse  =vec4(1.0) - newColor;
        float ratio = 1.0 - length(u_DistFromStart) / u_ForestRadius; 


        vec4 diffuseColor = vec4(vec3(vec4(1.0) - (inverse * ratio)), 1.0);

      // find new normal

      vec4 newNorm = getNewNormal(fs_Nor);

        // Calculate the diffuse term for Lambert shading
        float diffuseTerm = dot(normalize(newNorm), normalize(fs_LightVec));
        vec4 lightVec2 = vec4(vec3(0.0), 1.0);        

        diffuseTerm = mix(diffuseTerm, dot(normalize(newNorm), normalize(lightVec2)), .5);
        // Avoid negative lighting values
        diffuseTerm = clamp(diffuseTerm, 0.15, 1.0);

        float ambientTerm = 0.2;

        float lightIntensity = diffuseTerm + ambientTerm;   //Add a small float value to the color multiplier
                                                            //to simulate ambient lighting. This ensures that faces that are not
                                                            //lit by our point light are not completely black.

        // adjust light intensity so ground and sky turn white at the same time
        lightIntensity *= 2.75 - (ratio);
        lightIntensity = clamp(lightIntensity, 0.50, 1.2);
        // Compute final shaded color
        out_Col = vec4(diffuseColor.rgb * lightIntensity, diffuseColor.a);
}
