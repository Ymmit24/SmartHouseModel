# Piibox python web site

Can be installed with [pip](https://pypi.python.org/pypi/pip):

    pip install -e https://bitbucket.org/chrispbailey/piibox-python#egg=piibox-python

However this project uses [fabric](http://docs.fabfile.org/en/1.6/) for deployment.

    git clone https://bitbucket.org/chrispbailey/piibox-python piibox-python
    cd piibox-python/install
    fab deploy

This will install the software as a [virtualenv](http://www.virtualenv.org/en/latest/) in `/usr/local/projects/piibox-python`.


The web app uses [bottle](http://bottlepy.org/docs/dev/) as the web framework for http request processing and runs behind the [cherrypy](http://www.cherrypy.org/) (WSGI capable) HTTP server. The front end uses [Bootstrap](http://twitter.github.io/bootstrap/) & [jQuery](http://jquery.com/) for the presentation layer.

The [supervisord](http://supervisord.org/) process monitor is used for running the python webapp as a background process/daemon.

