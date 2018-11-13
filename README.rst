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
- To verify the signature of a license, use the method
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


Usage
-----

This section describes how to configure a system to use *truepy*.

Configuration includes installing *truepy*, generating an issuer certificate,
generating licenses and validating licenses.


Installation
~~~~~~~~~~~~

To install *truepy*, run the following command::

    pip install truepy


Generating an issuer certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This functionality in not included in *truepy*. The recommended tool to use is
`OpenSSL <https://www.openssl.org/>`_. To issue a certificate and generate a
private key, run the following command::

    openssl req -x509 \
        -newkey rsa:4096 \
        -keyout key.pem \
        -out certificate.pem \
        -days $VALIDITY

This will prompt you for a password to protect the private key, and some other
information to be included in the certificate.

The most important pieces of information are the password, which you will need
later, and the ``$VALIDITY``. The command line argument ``-days`` passed to
*OpenSSL* determines how many days the certificate will be valid. Be sure not to
set a too low value, as you will ne be able to use the certificate after this
number of days have passed.


Issuing licenses
~~~~~~~~~~~~~~~~

Once you have a certificate and a private key, you can start issuing licenses.
The code below shows the minimum steps required::

    from cryptography.hazmat import backends
    from cryptography.hazmat.primitives import serialization

    from truepy import LicenseData, License


    # Load the certificate
    with open('certificate.pem', 'rb') as f:
        certificate = f.read()

    # Load the private key
    with open('key.pem', 'rb') as f:
        key = serialization.load_pem_private_key(
            f.read(),
            password=b'MySecretPassword',
            backend=backends.default_backend())

    # Issue the license
    license = License.issue(
        certificate,
        key,
        license_data=LicenseData(
            '2016-10-01T00:00:00',
            '2020-10-01T00:00:00'))

    # Store the license
    with open('license.key', 'wb') as f:
        license.store(f, b'LicensePassword')

Please note the second parameter to ``License.store``. It is a password used to
derive an encryption key to encrypt the final license data. It is not secret, as
it will need to be available to the application verifying the license.


Validating licenses
~~~~~~~~~~~~~~~~~~~

To validate a license, you will need the certificate used in the step above, as
well as the password used to encrypt the final license data. The code below
shows the minimum steps required::

    from truepy import License


    # Load the certificate
    with open('certificate.pem', 'rb') as f:
        certificate = f.read()

    # Load the license
    with open('license.key', 'rb') as f:
        license = License.load(f, b'LicensePassword')

    # Verify the license; this will raise License.InvalidSignatureException if
    # the signature is incorrect
    license.verify(certificate)
