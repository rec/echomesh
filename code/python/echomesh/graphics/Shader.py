from __future__ import absolute_import, division, print_function, unicode_literals

import pi3d

_VERTEX_SHADER = """
precision highp float;

attribute vec3 vertex;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix[2]; // 0 model movement in real coords, 1 in camera coords
uniform vec3 unib[3];
//uniform vec2 umult, vmult => unib[2]

varying vec2 texcoordout;
varying float dist;

void main(void) {
  texcoordout = texcoord * vec2(unib[2][0], unib[2][1]);
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
  dist = gl_Position.z;
}
"""

_FRAGMENT_SHADER = """

precision mediump float;

varying vec2 texcoordout;
varying float dist;

uniform sampler2D tex0;
uniform vec3 unib[3];
//uniform float blend ====> unib[0][2]
uniform vec3 unif[16];
//uniform vec3 fogshade ==> unif[4]
//uniform float fogdist ==> unif[5][0]
//uniform float fogalpha => unif[5][1]

void main(void) {
  float ffact = smoothstep(unif[5][0]/3.0, unif[5][0], dist); // ------ smoothly increase fog between 1/3 and full fogdist
  vec4 texc = texture2D(tex0, texcoordout); // ------ material or basic colour from texture
  if (texc.a < unib[0][2]) discard; // ------ to allow rendering behind the transparent parts of this object
  gl_FragColor = (1.0 - ffact) * texc + ffact * vec4(unif[4], unif[5][1]); // ------ combine using factors
}
"""

SHADER = pi3d.Shader(vshader_source=_VERTEX_SHADER,
                     fshader_source=_FRAGMENT_SHADER)

def shader(shader_file=None):
  return pi3d.Shader(shfile=shader_file) if shader_file else SHADER
