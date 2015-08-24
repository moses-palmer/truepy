Release Notes
=============

2.0.1 - Corrected documentation
-------------------------------
*  Changed declared type of parameter to ``License.issue``.

2.0 - No dependency on *OpenSSL*
--------------------------------
*  Changed certificate and signature verification routines to use
   ``cryptography`` instead of ``pyOpenSSL``.

   This changes all methods that take a certificate or a key as parameter.


1.0.1 - License Data Bugfix
---------------------------
*  Changed ``truepy.LicenseData.information`` to ``info`` to be compatible with
   *TrueLicense*.


1.0 - Initial Release
---------------------
*  Support for basic license operations for TrueLicense version 1 licenses
