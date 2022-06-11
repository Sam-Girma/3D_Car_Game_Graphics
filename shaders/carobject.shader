#version 330 core

layout (location = 0) in vec3 position;
layout (location =1) in vec3 colors;
layout (location =2) in vec2 texCoord;

out vec3 newColor;
out vec2 outTexCoord;
in vec4 colors;
uniform mat4 transform;
void main()
{
    gl_Position = vec4(position.x, position.y, position.z, 1.0);
	newColor = colors;
	outTexCoord = vec2(texCoord.x, 1.0 - texCoord.y);

}
