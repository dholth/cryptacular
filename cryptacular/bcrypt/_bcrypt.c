/* Python extension module for bcrypt2.
 *
 * Daniel Holth <dholth@fastmail.fm>, 2010
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

#include <Python.h>
#include "ow-crypt.h"


struct module_state {
    PyObject *error;
};


#if PY_MAJOR_VERSION >= 3
    #define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
    #define GETSTATE(m) (&_state)
    static struct module_state _state;
#endif


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

    /* prefix, count, input, size, output, output_size */
    rc = crypt_gensalt_rn(prefix, count, salt, salt_len, output, sizeof(output));

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
    static int
    _bcrypt_traverse(PyObject *m, visitproc visit, void *arg)
    {
        Py_VISIT(GETSTATE(m)->error);
        return 0;
    }

    static int
    _bcrypt_clear(PyObject *m)
    {
        Py_CLEAR(GETSTATE(m)->error);
        return 0;
    }

    static struct PyModuleDef moduledef = {
        PyModuleDef_HEAD_INIT,
        "_bcrypt",
        NULL,
        sizeof(struct module_state),
        _bcrypt_methods,
        NULL,
        _bcrypt_traverse,
        _bcrypt_clear,
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

    if (module == NULL) {
        INITERROR;
    }
    struct module_state *st = GETSTATE(module);

    st->error = PyErr_NewException("_bcrypt.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

    #if PY_MAJOR_VERSION >= 3
        return module;
    #endif
}

