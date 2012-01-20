=====================
NEWS for flufl.bounce
=====================

2.1 (2012-01-19)
================
 * Fix TypeError thrown when None is returned by Caiwireless.  Given by Paul
   Egan. (LP: #917720)


2.0 (2012-01-04)
================
 * Port to Python 3 without the use of `2to3`.  Switch to class decorator
   syntax for declaring that a class implements an interface.  The functional
   form doesn't work for Python 3.
 * All returned addresses are bytes objects in Python 3 and 8-bit strings in
   Python 2 (no change there).
 * Add an additional in-the-wild example of a qmail bounce.  Given by Mark
   Sapiro.
 * Export `all_failures` in the package's namespace.
 * Fix `python setup.py test` so that it runs all the tests exactly once.
   There seems to be no portable way to support that and unittest discovery
   (i.e. `python -m unittest discover`) and since the latter requires
   virtualenv, just disable it for now.  (LP: #911399)
 * Add full copy of LGPLv3 to source tarball. (LP: #871961)


1.0.2 (2011-10-10)
==================
 * Fixed MANIFEST.in to exclude the .egg.


1.0.1 (2011-10-07)
==================
 * Fixed licenses.  All code is LGPLv3.


1.0 (2011-08-22)
================
 * Initial release.


0.91 (2011-07-15)
=================
 * Provide a nicer interface for detector modules.  Instead of using the magic
   empty tuple returns, provide three convenience constants in the interfaces
   module: NoFailures, NoTemporaryFailures, and NoPermanentFailures.
 * Add logging support.  Applications can initialize the `flufl.bounce`
   logger.  The test suite does its own logging.basicConfig(), which can be
   influenced by the environment variable $FLUFL_LOGGING.  See
   flufl/bounce/tests/helpers.py for details.


0.90 (2011-07-02)
=================
 * Initial refactoring from Mailman 3.
