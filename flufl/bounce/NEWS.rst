=====================
NEWS for flufl.bounce
=====================

2.0 (2012-01-04)
================
 * Port to Python 3 is mostly complete, however the test suite current fails
   because of <https://bugs.launchpad.net/zope.interface/+bug/911851>.  Once
   that bug is fixed in `zope.interface`, `flufl.bounce` should be Python 3.2
   compatible without the need for `2to3`.
 * All returned addresses are bytes objects in Python 3 and 8-bit strings in
   Python 2 (no change there).
 * Add an additional in-the-wild example of a qmail bounce.  Given by Mark
   Sapiro.
 * Export `all_failures` in the package's namespace.


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
