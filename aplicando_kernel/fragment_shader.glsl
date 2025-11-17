#version 330 core
in vec2 vTex;
out vec4 FragColor;

uniform sampler2D frameTex;
uniform vec2 texelSize;      
uniform float kernel[9];
uniform int kernelIndex;    
uniform int grayMode;

void main() {
    // sample 3x3 around current texcoord
    vec2 offs[9] = vec2[](
        vec2(-texelSize.x, -texelSize.y), vec2(0.0, -texelSize.y), vec2(texelSize.x, -texelSize.y),
        vec2(-texelSize.x,  0.0),          vec2(0.0,  0.0),          vec2(texelSize.x,  0.0),
        vec2(-texelSize.x,  texelSize.y),  vec2(0.0,  texelSize.y),  vec2(texelSize.x,  texelSize.y)
    );

    vec3 result = vec3(0.0);
    for (int i = 0; i < 9; ++i) {
        vec3 c = texture(frameTex, vTex + offs[i]).rgb;
        result += c * kernel[i];
    }

    // clamp result
    result = clamp(result, 0.0, 1.0);

    if (grayMode == 1) {
        float l = dot(result, vec3(0.299, 0.587, 0.114));
        FragColor = vec4(vec3(l), 1.0);
    } else {
        FragColor = vec4(result, 1.0);
    }
}
