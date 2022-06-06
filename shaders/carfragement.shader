#version 330 core

in vec3 newColor;
in vec2 outTexCoord;
out vec4 colors;
uniform sampler2D texSampler;

void main()
{
    colors = vec4(newColor, 1.0);
	outColor = texture(texSampler, outTexCoord);
}
