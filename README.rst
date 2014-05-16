TrueLicense compatible license manager for Python
=================================================

This package supports managing licenses one the format used by the Java package
`TrueLicense <https://truelicense.java.net/>`_. Only the version 1 format is
supported.

Please see the *TrueLicense* home page for an exhaustive reference of the
license format, or `Quick license format description`_ below.


Quick license format description
--------------------------------

A license has a validity window in time, an issuer, a holder and various meta
data.

It is signed by the holder, and the signature can be verified using the issuer
certificate.

The license file is also encrypted with a key derived from a password.


Quick library reference
-----------------------

The main class exported by *truepy* is ``truepy.License``.

- To generate a new license, use the class method ``truepy.License.issue``.
- To load a license from a file or stream, use the class method
  ``truepy.License.load``.
- To save a license to a file or stream, use the method
  ``truepy.License.store``.
- To verify the siganture of a license, use the method
  ``truepy.License.verify``.
- To read license information, use the ``truepy.License.license_data``
  attribute; this is of the type ``truepy.LicenseData``.

Loading and storing licenses requires only the license password; these
operations do not perform signing and signature verification.

Issuing a new license requires the private key of the issuer certificate.

Verifying a license signature requires the issuer certificate.


Quick application reference
---------------------------

Please run the application with ``python -m truepy -h`` for more information.
