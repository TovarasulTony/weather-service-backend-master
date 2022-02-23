Weather service
===============

This is the test for backend developers.

Take as long as you need or you think is reasonable. You don't need to
complete all the requirements if you are pushed for time, however your
solution should give us enough code to confirm that you are competent
programmer.

You should use python and whatever framework and/or libraries you feel most
comfortable with.

Please do not make your solution publicly available, just compress this folder
and send it back to us.

Introduction
------------

We want you to write an HTTP service which provides an API to get a weather
forecast for a given city.

You should use the [openweathermap](https://www.openweathermap.org) API as
your data source. The API requires an API key that can be obtained for free
after [signing up](https://home.openweathermap.org/users/sign_up) (if you have
any problems obtaining an API key, contact us and we will provide one)

Getting it running
------------------

**Please fill this section out, imagine we are starting with a brand new
installation of ubuntu 20.04 and we know nothing about your implementation**

python3 -m pip install Flask

The Service
-----------

We would like to make the following calls against this web service using 
[curl](https://curl.haxx.se/)

The submitted result will be put through automated testing to verify the API
is working as expected.

### `/ping`

This is a simple health check that we can use to determine that the service is
running, and provides information about the application. The `"version"`
attribute in the response should match the version number in the `VERSION`
file.

```bash
$ curl -si http://localhost:8080/ping

HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
  "name": "weatherservice",
  "status": "ok",
  "version": "1.0.0"
}
```

### `/forecast/<city>`

This endpoint allows a user to request a breakdown of the current weather for
a specific city. The response should include a description of the cloud cover,
the humidity as a percentage, the pressure in hecto Pascals (hPa), and
temperature in Celsius.

For example fetching the weather data for London should look like this:

```bash
$ curl -si http://localhost:8080/forecast/london/

HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "clouds": "broken clouds",
    "humidity": "66.6%",
    "pressure": "1027.51 hPa",
    "temperature": "14.4C"
}
```

The endpoint should also take an `at` query string parameter that will
return the weather forecast for a specific date or datetime. The `at`
parameter should accept both date and datetime stamps in the [ISO
8601](https://en.wikipedia.org/wiki/ISO_8601) format. Ensure that your service
respects time zone offsets.

```bash
$ curl -si http://localhost:8080/forecast/london/?at=2018-10-14T14:34:40+0100

HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "clouds": "sunny",
    "humidity": "12.34%",
    "pressure": "1000.51 hPa",
    "temperature": "34.4C"
}

$ curl -si http://localhost:8080/forecast/london/?at=2018-10-14

HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "clouds": "overcast",
    "humidity": "20.6%",
    "pressure": "1014.51 hPa",
    "temperature": "28.0C"
}
```

### Errors

When no data is found or the endpoint is invalid the service should respond
with `404` status code and an appropriate message:

```bash
$ curl -si http://localhost:8080/forecast/westeros

HTTP/1.1 404 Not Found
Content-Type: application/json; charset=utf-8
{
    "error": "Cannot find country 'westeros'",
    "error_code": "country_not_found"
}
```

Similarly invalid requests should return a `400` status code:

```bash
$ curl -si http://localhost:8080/forecast/london?at=1938-12-25

HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8
{
    "error": "Date is in the past",
    "error_code": "invalid date"
}
```

If anything else goes wrong the service should response with a `500` status code
and a message that doesn't leak any information about the service internals:

```bash
$ curl -si http://localhost:8080/forecast/london

HTTP/1.1 500 Internal Server Error
Content-Type: application/json; charset=utf-8
{
    "error": "Something went wrong",
    "error_code": "internal_server_error"
}
```

Things that we would like to see
--------------------------------

* Tests! We believe that code without tests is bad code, please include any
  instructions and/or dependencies that we will need in order to run your
  tests.
* No sensitive data (such as your API key) should included in your code, your
  service should read sensitive information from the environment at run time
  (please include this information in your set up documentation).
* We work with [git](https://git-scm.com/) for version control, please include
  your `.git` folder when you compress this folder and send it back to us. You
  should feel free to commit at any point in the process.

Stretch Goals
-------------

If you have time or want to go the extra mile then try implementing the
following features:

* Configurable units for temperature (Fahrenheit, Kelvins, etc) and Pressure
  (bars, atmospheres, tor, etc) via query string parameters.
* Secure your service with [Basic auth](https://en.wikipedia.org/wiki/Basic_access_authentication)
  using the user `admin` and the password `secret`.
* Cache responses for a short period of time in order to avoid making
  unnecessary requests to the 3rd party API.
* Create a working [docker](https://www.docker.com/) container and include the
  `Dockerfile` along with your service.
* Run the service somewhere on the internet and give us a link. Bonus points
  for including your deployment configuration and/or documentation.
