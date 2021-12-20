#version 300 es
precision highp float;

uniform mat4 u_Model;

uniform vec3 u_DistFromStart;
uniform float u_ForestRadius;
in vec4 fs_Col;
in vec4 fs_Pos;
in vec4 fs_Nor;

out vec4 out_Col;

float random3D(vec3 p) {
    return sin(length(vec3(fract(dot(p, vec3(161.1, 121.8, 160.2))), 
                            fract(dot(p, vec3(120.5, 161.3, 160.4))),
                            fract(dot(p, vec3(161.4, 161.2, 122.5))))) * 435.90906);
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

float fbmNoise(vec3 v)
{
    float total = 0.0;
    float persistence = 0.3;
    float frequency = 4.0;
    float amplitude = 3.0;
    int octaves = 4;

    for (int i = 1; i <= octaves; i++) {
        total += amplitude * interpolateNoise3D(frequency * v.x, frequency * v.y, frequency * v.z);
        frequency *= 2.0;
        amplitude *= persistence;
    }
    return total;
}

vec3 vertexHeightNoise(vec3 position) {
    vec4 modelposition = u_Model * vec4(position, 1.0);   // Temporarily store the transformed vertex positions for use below

    vec3 noiseInput = modelposition.xyz;
    //noiseInput += getAnimation();

    vec3 noise = fbmNoise(noiseInput) * noiseInput;
    
    float noiseScale = noise.r;

    vec3 offsetAmount = vec3(fs_Nor) * noiseScale;
    vec3 noisyModelPosition = modelposition.xyz + 0.075 * offsetAmount;
    return noisyModelPosition;
}

vec4 getNewNormal(vec4 norm) {
    float epsilon = 0.008;

    vec3 tangent = normalize(cross(vec3(0.0, 1.0, 0.0), vec3(norm)));
    vec3 bitangent = cross(vec3(norm), tangent);

    vec3 point1 = vertexHeightNoise(fs_Pos.xyz + epsilon * tangent);
    vec3 point2 = vertexHeightNoise(fs_Pos.xyz + epsilon * bitangent);
    vec3 point3 = vertexHeightNoise(fs_Pos.xyz - epsilon * tangent);
    vec3 point4 = vertexHeightNoise(fs_Pos.xyz - epsilon * bitangent);
    
    return vec4(normalize(cross(normalize(point1 - point3), normalize(point2 - point4))), 0.0);
    //return vec4(normalize(cross(normalize(pos))))
} 

void main()
{

    float ratio = 1.0 - (length(u_DistFromStart) / u_ForestRadius);
    vec3 inverse = vec3(1.0) - vec3(fs_Col);
    vec4 diffuseColor = vec4(vec3(1.0) - vec3(inverse * ratio), 1.0);

    // Calculate the diffuse term for Lambert shading

    vec4 fs_LightVec = vec4(2000.0, 1000.0, 2000.0, 1.0);

    vec4 newNorm = getNewNormal(fs_Nor);

    float diffuseTerm = dot(normalize(fs_Nor), normalize(fs_LightVec));
    // Avoid negative lighting values
    diffuseTerm = clamp(diffuseTerm, 0.10, 1.0);

    float ambientTerm = 0.1;

    float lightIntensity = diffuseTerm + ambientTerm;   //Add a small float value to the color multiplier
                                                        //to simulate ambient lighting. This ensures that faces that are not
                                                        //lit by our point light are not completely black.

    // adjust light intensity so ground and sky turn white at the same time
        lightIntensity *= 2.75 - (ratio);
        lightIntensity = clamp(lightIntensity, 0.50, 1.2);
        
    // Compute final shaded color
    out_Col = vec4(diffuseColor.rgb * lightIntensity, diffuseColor.a);

}
