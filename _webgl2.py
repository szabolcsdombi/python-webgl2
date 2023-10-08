setup_script = '''
const setupPythonWebGL2 = (wasm, gl) => {
  const textEncoder = new TextEncoder('utf-8');
  const textDecoder = new TextDecoder('utf-8');

  const getString = (ptr) => {
    const length = wasm.HEAPU8.subarray(ptr).findIndex((c) => c === 0);
    return textDecoder.decode(wasm.HEAPU8.subarray(ptr, ptr + length));
  };

  const setString = (ptr, text) => {
    const raw = textEncoder.encode(text);
    wasm.HEAPU8.set(raw, ptr);
    wasm.HEAPU8[raw.byteLength] = 0;
  };

  const typedArray = (type, ptr, size) => {
    switch (type) {
      case 0x1400: return wasm.HEAP8.subarray(ptr, ptr + size);
      case 0x1401: return wasm.HEAPU8.subarray(ptr, ptr + size);
      case 0x1402: return wasm.HEAP16.subarray(ptr / 2, ptr / 2 + size * 2);
      case 0x1403: return wasm.HEAPU16.subarray(ptr / 2, ptr / 2 + size * 2);
      case 0x1404: return wasm.HEAP32.subarray(ptr / 4, ptr / 4 + size * 4);
      case 0x1405: return wasm.HEAPU32.subarray(ptr / 4, ptr / 4 + size * 4);
      case 0x1406: return wasm.HEAPF32.subarray(ptr / 4, ptr / 4 + size * 4);
      case 0x84FA: return wasm.HEAPU32.subarray(ptr / 4, ptr / 4 + size * 4);
    };
  };

  const componentCount = (format) => {
    switch (format) {
      case 0x1903: return 1;
      case 0x8227: return 2;
      case 0x1908: return 4;
      case 0x8D94: return 1;
      case 0x8228: return 2;
      case 0x1902: return 1;
      case 0x84F9: return 1;
    }
  };

  const glo = new Map();
  let glid = 1;
  glo[0] = null;

  wasm.mergeLibSymbols({
    webgl2_glCullFace(mode) {
      gl.cullFace(mode);
    },
    webgl2_glClear(mask) {
      gl.clear(mask);
    },
    webgl2_glTexParameteri(target, pname, param) {
      gl.texParameteri(target, pname, param);
    },
    webgl2_glTexImage2D(target, level, internalformat, width, height, border, format, type, pixels) {
      gl.texImage2D(target, level, internalformat, width, height, border, format, type, null);
    },
    webgl2_glDepthMask(flag) {
      gl.depthMask(flag);
    },
    webgl2_glDisable(cap) {
      if (cap !== 0x8D69 && cap !== 0x8642 && cap !== 0x884F && cap !== 0x8DB9) {
        gl.disable(cap);
      }
    },
    webgl2_glEnable(cap) {
      if (cap !== 0x8D69 && cap !== 0x8642 && cap !== 0x884F && cap !== 0x8DB9) {
        gl.enable(cap);
      }
    },
    webgl2_glFlush() {
      gl.flush();
    },
    webgl2_glDepthFunc(func) {
      gl.depthFunc(func);
    },
    webgl2_glReadBuffer(src) {
      gl.readBuffer(src);
    },
    webgl2_glReadPixels(x, y, width, height, format, type, pixels) {
      const data = typedArray(type, pixels, width * height * componentCount(format));
      gl.readPixels(x, y, width, height, format, type, data);
    },
    webgl2_glGetError() {
      return gl.getError();
    },
    webgl2_glGetIntegerv(pname, data) {
      wasm.HEAP32[data / 4] = gl.getParameter(pname);
    },
    webgl2_glViewport(x, y, width, height) {
      gl.viewport(x, y, width, height);
    },
    webgl2_glTexSubImage2D(target, level, xoffset, yoffset, width, height, format, type, pixels) {
      const data = typedArray(type, pixels, width * height * componentCount(format));
      gl.texSubImage2D(target, level, xoffset, yoffset, width, height, format, type, data);
    },
    webgl2_glBindTexture(target, texture) {
      gl.bindTexture(target, glo[texture]);
    },
    webgl2_glDeleteTextures(n, textures) {
      const texture = wasm.HEAP32[textures / 4];
      gl.deleteTexture(glo[texture]);
      glo.delete(texture);
    },
    webgl2_glGenTextures(n, textures) {
      const texture = glid++;
      glo[texture] = gl.createTexture();
      wasm.HEAP32[textures / 4] = texture;
    },
    webgl2_glTexImage3D(target, level, internalformat, width, height, depth, border, format, type, pixels) {
      gl.texImage3D(target, level, internalformat, width, height, depth, border, format, type, null);
    },
    webgl2_glTexSubImage3D(target, level, xoffset, yoffset, zoffset, width, height, depth, format, type, pixels) {
      const data = typedArray(type, pixels, width * height * depth * componentCount(format));
      gl.texSubImage3D(target, level, xoffset, yoffset, zoffset, width, height, depth, format, type, data);
    },
    webgl2_glActiveTexture(texture) {
      gl.activeTexture(texture);
    },
    webgl2_glBlendFuncSeparate(sfactorRGB, dfactorRGB, sfactorAlpha, dfactorAlpha) {
      gl.blendFuncSeparate(sfactorRGB, dfactorRGB, sfactorAlpha, dfactorAlpha);
    },
    webgl2_glGenQueries(n, ids) {
      gl.getExtension('EXT_disjoint_timer_query_webgl2');
      const query = glid++;
      glo[query] = gl.createQuery();
      wasm.HEAP32[ids / 4] = query;
    },
    webgl2_glBeginQuery(target, id) {
      gl.beginQuery(target, glo[id]);
    },
    webgl2_glEndQuery(target) {
      gl.endQuery(target);
    },
    webgl2_glGetQueryObjectuiv(id, pname, params) {
      wasm.HEAP32[params / 4] = gl.getQueryParameter(glo[id], pname);
    },
    webgl2_glBindBuffer(target, buffer) {
      gl.bindBuffer(target, glo[buffer]);
    },
    webgl2_glDeleteBuffers(n, buffers) {
      const buffer = wasm.HEAP32[buffers / 4];
      gl.deleteBuffer(glo[buffer]);
      glo.delete(buffer);
    },
    webgl2_glGenBuffers(n, buffers) {
      const buffer = glid++;
      glo[buffer] = gl.createBuffer();
      wasm.HEAP32[buffers / 4] = buffer;
    },
    webgl2_glBufferData(target, size, data, usage) {
      gl.bufferData(target, size, usage);
    },
    webgl2_glBufferSubData(target, offset, size, data) {
      gl.bufferSubData(target, offset, wasm.HEAPU8.subarray(data, data + size));
    },
    webgl2_glUnmapBuffer(target) {
      return 0;
    },
    webgl2_glBlendEquationSeparate(modeRGB, modeAlpha) {
      gl.blendEquationSeparate(modeRGB, modeAlpha);
    },
    webgl2_glDrawBuffers(n, bufs) {
      gl.drawBuffers(wasm.HEAP32.subarray(bufs / 4, bufs / 4 + n));
    },
    webgl2_glStencilOpSeparate(face, sfail, dpfail, dppass) {
      gl.stencilOpSeparate(face, sfail, dpfail, dppass);
    },
    webgl2_glStencilFuncSeparate(face, func, ref, mask) {
      gl.stencilFuncSeparate(face, func, ref, mask);
    },
    webgl2_glStencilMaskSeparate(face, mask) {
      gl.stencilMaskSeparate(face, mask);
    },
    webgl2_glAttachShader(program, shader) {
      gl.attachShader(glo[program], glo[shader]);
    },
    webgl2_glCompileShader(shader) {
      gl.compileShader(glo[shader]);
    },
    webgl2_glCreateProgram() {
      const program = glid++;
      glo[program] = gl.createProgram();
      return program;
    },
    webgl2_glCreateShader(type) {
      const shader = glid++;
      glo[shader] = gl.createShader(type);
      return shader;
    },
    webgl2_glDeleteProgram(program) {
      gl.deleteProgram(glo[program]);
      glo.delete(program);
    },
    webgl2_glDeleteShader(shader) {
      gl.deleteShader(glo[shader]);
      glo.delete(shader);
    },
    webgl2_glEnableVertexAttribArray(index) {
      gl.enableVertexAttribArray(index);
    },
    webgl2_glGetActiveAttrib(program, index, bufSize, length, size, type, name) {
      const info = gl.getActiveAttrib(glo[program], index);
      setString(name, info.name);
      wasm.HEAP32[size / 4] = info.size;
      wasm.HEAP32[type / 4] = info.type;
    },
    webgl2_glGetActiveUniform(program, index, bufSize, length, size, type, name) {
      const info = gl.getActiveUniform(glo[program], index);
      setString(name, info.name);
      wasm.HEAP32[size / 4] = info.size;
      wasm.HEAP32[type / 4] = info.type;
    },
    webgl2_glGetAttribLocation(program, name) {
      return gl.getAttribLocation(glo[program], getString(name));
    },
    webgl2_glGetProgramiv(program, pname, params) {
      if (pname === 0x8B84) {
        wasm.HEAP32[params / 4] = gl.getProgramInfoLog(glo[program]).length + 1;
      } else {
        wasm.HEAP32[params / 4] = gl.getProgramParameter(glo[program], pname);
      }
    },
    webgl2_glGetProgramInfoLog(program, bufSize, length, infoLog) {
      setString(infoLog, gl.getProgramInfoLog(glo[program]));
    },
    webgl2_glGetShaderiv(shader, pname, params) {
      if (pname === 0x8B84) {
        wasm.HEAP32[params / 4] = gl.getShaderInfoLog(glo[shader]).length + 1;
      } else {
        wasm.HEAP32[params / 4] = gl.getShaderParameter(glo[shader], pname);
      }
    },
    webgl2_glGetShaderInfoLog(shader, bufSize, length, infoLog) {
      setString(infoLog, gl.getShaderInfoLog(glo[shader]));
    },
    webgl2_glGetUniformLocation(program, name) {
      const uniform = gl.getUniformLocation(glo[program], getString(name));
      if (uniform !== null) {
        const location = glid++;
        glo[location] = uniform;
        return location;
      }
      return -1;
    },
    webgl2_glLinkProgram(program) {
      gl.linkProgram(glo[program]);
    },
    webgl2_glShaderSource(shader, count, string, length) {
      gl.shaderSource(glo[shader], getString(wasm.HEAP32[string / 4]));
    },
    webgl2_glUseProgram(program) {
      gl.useProgram(glo[program]);
    },
    webgl2_glUniform1i(location, v0) {
      gl.uniform1i(glo[location], v0);
    },
    webgl2_glUniform1fv(location, count, value) {
      gl.uniform1fv(glo[location], wasm.HEAPF32.subarray(value / 4, value / 4 + count));
    },
    webgl2_glUniform2fv(location, count, value) {
      gl.uniform2fv(glo[location], wasm.HEAPF32.subarray(value / 4, value / 4 + count * 2));
    },
    webgl2_glUniform3fv(location, count, value) {
      gl.uniform3fv(glo[location], wasm.HEAPF32.subarray(value / 4, value / 4 + count * 3));
    },
    webgl2_glUniform4fv(location, count, value) {
      gl.uniform4fv(glo[location], wasm.HEAPF32.subarray(value / 4, value / 4 + count * 4));
    },
    webgl2_glUniform1iv(location, count, value) {
      gl.uniform1iv(glo[location], wasm.HEAP32.subarray(value / 4, value / 4 + count));
    },
    webgl2_glUniform2iv(location, count, value) {
      gl.uniform2iv(glo[location], wasm.HEAP32.subarray(value / 4, value / 4 + count * 2));
    },
    webgl2_glUniform3iv(location, count, value) {
      gl.uniform3iv(glo[location], wasm.HEAP32.subarray(value / 4, value / 4 + count * 3));
    },
    webgl2_glUniform4iv(location, count, value) {
      gl.uniform4iv(glo[location], wasm.HEAP32.subarray(value / 4, value / 4 + count * 4));
    },
    webgl2_glUniformMatrix2fv(location, count, transpose, value) {
      gl.uniformMatrix2fv(glo[location], transpose, transpose, wasm.HEAPF32.subarray(value / 4, value / 4 + count * 4));
    },
    webgl2_glUniformMatrix3fv(location, count, transpose, value) {
      gl.uniformMatrix3fv(glo[location], transpose, wasm.HEAPF32.subarray(value / 4, value / 4 + count * 9));
    },
    webgl2_glUniformMatrix4fv(location, count, transpose, value) {
      gl.uniformMatrix4fv(glo[location], transpose, wasm.HEAPF32.subarray(value / 4, value / 4 + count * 16));
    },
    webgl2_glVertexAttribPointer(index, size, type, normalized, stride, pointer) {
      gl.vertexAttribPointer(index, size, type, normalized, stride, pointer);
    },
    webgl2_glUniformMatrix2x3fv(location, count, transpose, value) {
      gl.uniformMatrix2x3fv(glo[location], transpose, wasm.HEAPF32.subarray(value / 4, value / 4 + count * 6));
    },
    webgl2_glUniformMatrix3x2fv(location, count, transpose, value) {
      gl.uniformMatrix3x2fv(glo[location], transpose, wasm.HEAPF32.subarray(value / 4, value / 4 + count * 6));
    },
    webgl2_glUniformMatrix2x4fv(location, count, transpose, value) {
      gl.uniformMatrix2x4fv(glo[location], transpose, wasm.HEAPF32.subarray(value / 4, value / 4 + count * 8));
    },
    webgl2_glUniformMatrix4x2fv(location, count, transpose, value) {
      gl.uniformMatrix4x2fv(glo[location], transpose, wasm.HEAPF32.subarray(value / 4, value / 4 + count * 8));
    },
    webgl2_glUniformMatrix3x4fv(location, count, transpose, value) {
      gl.uniformMatrix3x4fv(glo[location], transpose, wasm.HEAPF32.subarray(value / 4, value / 4 + count * 12));
    },
    webgl2_glUniformMatrix4x3fv(location, count, transpose, value) {
      gl.uniformMatrix4x3fv(glo[location], transpose, wasm.HEAPF32.subarray(value / 4, value / 4 + count * 12));
    },
    webgl2_glBindBufferRange(target, index, buffer, offset, size) {
      gl.bindBufferRange(target, index, glo[buffer], offset, size);
    },
    webgl2_glVertexAttribIPointer(index, size, type, stride, pointer) {
      gl.vertexAttribIPointer(index, size, type, stride, pointer);
    },
    webgl2_glUniform1uiv(location, count, value) {
      gl.uniform1uiv(glo[location], wasm.HEAPU32.subarray(value / 4, value / 4 + count));
    },
    webgl2_glUniform2uiv(location, count, value) {
      gl.uniform2uiv(glo[location], wasm.HEAPU32.subarray(value / 4, value / 4 + count * 2));
    },
    webgl2_glUniform3uiv(location, count, value) {
      gl.uniform3uiv(glo[location], wasm.HEAPU32.subarray(value / 4, value / 4 + count * 3));
    },
    webgl2_glUniform4uiv(location, count, value) {
      gl.uniform4uiv(glo[location], wasm.HEAPU32.subarray(value / 4, value / 4 + count * 4));
    },
    webgl2_glClearBufferiv(buffer, drawbuffer, value) {
      gl.clearBufferiv(buffer, drawbuffer, wasm.HEAP32.subarray(value / 4, value / 4 + 4));
    },
    webgl2_glClearBufferuiv(buffer, drawbuffer, value) {
      gl.clearBufferuiv(buffer, drawbuffer, wasm.HEAPU32.subarray(value / 4, value / 4 + 4));
    },
    webgl2_glClearBufferfv(buffer, drawbuffer, value) {
      gl.clearBufferfv(buffer, drawbuffer, wasm.HEAPF32.subarray(value / 4, value / 4 + 4));
    },
    webgl2_glClearBufferfi(buffer, drawbuffer, depth, stencil) {
      gl.clearBufferfi(buffer, drawbuffer, depth, stencil);
    },
    webgl2_glBindRenderbuffer(target, renderbuffer) {
      gl.bindRenderbuffer(target, glo[renderbuffer]);
    },
    webgl2_glDeleteRenderbuffers(n, renderbuffers) {
      const renderbuffer = wasm.HEAP32[renderbuffers / 4];
      gl.deleteRenderbuffer(glo[renderbuffer]);
      glo.delete(renderbuffer);
    },
    webgl2_glGenRenderbuffers(n, renderbuffers) {
      const renderbuffer = glid++;
      glo[renderbuffer] = gl.createRenderbuffer();
      wasm.HEAP32[renderbuffers / 4] = renderbuffer;
    },
    webgl2_glBindFramebuffer(target, framebuffer) {
      gl.bindFramebuffer(target, glo[framebuffer]);
    },
    webgl2_glDeleteFramebuffers(n, framebuffers) {
      const framebuffer = wasm.HEAP32[framebuffers / 4];
      gl.deleteFramebuffer(glo[framebuffer]);
      glo.delete(framebuffer);
    },
    webgl2_glGenFramebuffers(n, framebuffers) {
      const framebuffer = glid++;
      glo[framebuffer] = gl.createFramebuffer();
      wasm.HEAP32[framebuffers / 4] = framebuffer;
    },
    webgl2_glFramebufferTexture2D(target, attachment, textarget, texture, level) {
      gl.framebufferTexture2D(target, attachment, textarget, glo[texture], level);
    },
    webgl2_glFramebufferRenderbuffer(target, attachment, renderbuffertarget, renderbuffer) {
      gl.framebufferRenderbuffer(target, attachment, renderbuffertarget, glo[renderbuffer]);
    },
    webgl2_glGenerateMipmap(target) {
      gl.generateMipmap(target);
    },
    webgl2_glBlitFramebuffer(srcX0, srcY0, srcX1, srcY1, dstX0, dstY0, dstX1, dstY1, mask, filter) {
      gl.blitFramebuffer(srcX0, srcY0, srcX1, srcY1, dstX0, dstY0, dstX1, dstY1, mask, filter);
    },
    webgl2_glRenderbufferStorageMultisample(target, samples, internalformat, width, height) {
      gl.renderbufferStorageMultisample(target, samples, internalformat, width, height);
    },
    webgl2_glFramebufferTextureLayer(target, attachment, texture, level, layer) {
      gl.framebufferTextureLayer(target, attachment, glo[texture], level, layer);
    },
    webgl2_glMapBufferRange(target, offset, length, access) {
      return 0;
    },
    webgl2_glBindVertexArray(array) {
      gl.bindVertexArray(glo[array]);
    },
    webgl2_glDeleteVertexArrays(n, arrays) {
      const array = wasm.HEAP32[arrays / 4];
      gl.deleteVertexArray(glo[array]);
      glo.delete(array);
    },
    webgl2_glGenVertexArrays(n, arrays) {
      const array = glid++;
      glo[array] = gl.createVertexArray();
      wasm.HEAP32[arrays / 4] = array;
    },
    webgl2_glDrawArraysInstanced(mode, first, count, instancecount) {
      gl.drawArraysInstanced(mode, first, count, instancecount);
    },
    webgl2_glDrawElementsInstanced(mode, count, type, indices, instancecount) {
      gl.drawElementsInstanced(mode, count, type, indices, instancecount);
    },
    webgl2_glGetUniformBlockIndex(program, uniformBlockName) {
      return gl.getUniformBlockIndex(glo[program], getString(uniformBlockName));
    },
    webgl2_glGetActiveUniformBlockiv(program, uniformBlockIndex, pname, params) {
      wasm.HEAP32[params / 4] = gl.getActiveUniformBlockParameter(glo[program], uniformBlockIndex, pname);
    },
    webgl2_glGetActiveUniformBlockName(program, uniformBlockIndex, bufSize, length, uniformBlockName) {
      setString(uniformBlockName, gl.getActiveUniformBlockName(glo[program], uniformBlockIndex));
    },
    webgl2_glUniformBlockBinding(program, uniformBlockIndex, uniformBlockBinding) {
      gl.uniformBlockBinding(glo[program], uniformBlockIndex, uniformBlockBinding);
    },
    webgl2_glFenceSync(condition, flags) {
      const sync = glid++;
      glo[sync] = gl.fenceSync(condition, flags);
      return sync;
    },
    webgl2_glDeleteSync(sync) {
      gl.deleteSync(glo[sync]);
      glo.delete(sync);
    },
    webgl2_glClientWaitSync(sync, flags, timeout) {
      gl.clientWaitSync(glo[sync], flags, gl.MAX_CLIENT_WAIT_TIMEOUT_WEBGL);
    },
    webgl2_glGenSamplers(count, samplers) {
      const sampler = glid++;
      glo[sampler] = gl.createSampler();
      wasm.HEAP32[samplers / 4] = sampler;
    },
    webgl2_glDeleteSamplers(count, samplers) {
      const sampler = wasm.HEAP32[samplers / 4];
      gl.deleteSampler(glo[sampler]);
      glo.delete(sampler);
    },
    webgl2_glBindSampler(unit, sampler) {
      gl.bindSampler(unit, glo[sampler]);
    },
    webgl2_glSamplerParameteri(sampler, pname, param) {
      gl.samplerParameteri(glo[sampler], pname, param);
    },
    webgl2_glSamplerParameterf(sampler, pname, param) {
      gl.samplerParameterf(glo[sampler], pname, param);
    },
    webgl2_glVertexAttribDivisor(index, divisor) {
      gl.vertexAttribDivisor(index, divisor);
    },
  });
};
'''

demo_canvas = '''
const canvas = document.createElement('canvas');
document.body.appendChild(canvas);

canvas.width = 600;
canvas.height = 400;

canvas.style.position = 'fixed';
canvas.style.bottom = '10px';
canvas.style.right = '10px';

const gl = canvas.getContext('webgl2', {
  alpha: false, depth: false, stencil: false, antialias: false,
  premultipliedAlpha: false, preserveDrawingBuffer: false,
  powerPreference: 'high-performance',
});
'''


def init(pyodide=True):
    if pyodide:
        from pyodide.code import run_js
        run_js(demo_canvas + setup_script + ';setupPythonWebGL2(pyodide._module, gl);')

