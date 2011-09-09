/* Python extension module for bcrypt2.
 *
 * Daniel Holth <dholth@fastmail.fm>, 2010
 * Frank Smit <frank@61924.nl>, 2011 (added Python 3 support)
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "ow-crypt.h"


static PyObject *
_py_crypt_rn(PyObject *self, PyObject *args)
{
    char *rc;
    const char *key;
    const char *setting;
    char output[61];

    memset(output, 0, sizeof(output));

    if (!PyArg_ParseTuple(args, "ss", &key, &setting)) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS;

    /* key, setting, output, size */
    rc = crypt_rn(key, setting, output, sizeof(output));

    Py_END_ALLOW_THREADS;

    if (rc == NULL) {
        Py_RETURN_NONE;
    }

    output[sizeof(output) - 1] = '\0';

    return Py_BuildValue("s", output);
}


static PyObject *
_py_crypt_gensalt_rn(PyObject *self, PyObject *args)
{
    char *rc;
    const char *prefix;
    const int count;
    const char *salt;
    const Py_ssize_t salt_len;
    char output[30];

    memset(output, 0, sizeof(output));

    if (!PyArg_ParseTuple(args, "sis#", &prefix, &count, &salt, &salt_len)) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS;

    /* prefix, count, input, size, output, output_size */
    rc = crypt_gensalt_rn(prefix, count, salt, salt_len, output, sizeof(output));

    Py_END_ALLOW_THREADS;

    if (rc == NULL) {
        Py_RETURN_NONE;
    }

    output[sizeof(output) - 1] = '\0';

    return Py_BuildValue("s", output);
}


static PyMethodDef _bcrypt_methods[] = {
    {"crypt_rn", _py_crypt_rn, METH_VARARGS, "Encrypt password"},
    {"crypt_gensalt_rn", _py_crypt_gensalt_rn, METH_VARARGS, "Generate salt"},
    {NULL, NULL, 0, NULL} /* Sentinel */
};



#if PY_MAJOR_VERSION >= 3
    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "_bcrypt",
        NULL,
        -1,
        _bcrypt_methods,
        NULL,
        NULL,
        NULL,
        NULL
    };

    #define INITERROR return NULL

    PyObject *
    PyInit__bcrypt(void)
#else
    #define INITERROR return

    PyMODINIT_FUNC
    init_bcrypt(void)
#endif
{
    #if PY_MAJOR_VERSION >= 3
        PyObject *module = PyModule_Create(&moduledef);
    #else
        PyObject *module = Py_InitModule("_bcrypt", _bcrypt_methods);
    #endif

    #if PY_MAJOR_VERSION >= 3
        return module;
    #endif
}
