vl
==

.. image:: https://travis-ci.org/verifid/vl.svg?branch=master
    :target: https://travis-ci.org/verifid/vl

.. image:: https://codecov.io/gh/verifid/vl/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/verifid/vl

**vl** is the ``verification layer`` of **verifid**, actually the core project that is responsible from verifying identity cards
or passports. Basically it's a self deployed API which has 4 main endpoints. It runs on either ``Docker`` or ``Kubernetes`` as a
container. All endpoints fit in just two controllers and all endpoints have detailly documented. **vl** relies on some other **verifid**
and as well as other Open Source Python modules. **vl** uses **Nginx** as a load balancer and it's already configured in setup files.

Controllers & Endpoints
-----------------------

|image_controllers|

.. |image_controllers| image:: https://raw.githubusercontent.com/verifid/vl/master/resources/controllers.png
