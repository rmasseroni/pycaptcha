Your company is behind an online forum about cooking, but the registration procedure is too easy for a bot to complete. You’re therefore asked to provide a backend service to work with captcha images. The service must be capable of generating captchas and validate them against the solution. You can find a definition of captcha on wikipedia: https://en.wikipedia.org/wiki/CAPTCHA

You’re responsible to design a complete solution and to actually code it in Python or Node.js (just use the language you’re more comfortable with). You must version this project with git and provide a public URL where we can check your solution. Please don’t put any reference to our company inside the repository.

Some constraints:

- provide a README.md file with clear instructions about how we can test your service in a local development environment;

- the communication protocol will be HTTP. We expect one route to provide the CAPTCHA and a second route to validate it. You’re free to design as you like, but you’re asked to provide documentation for both of the endpoints;

- this service will operate inside a micro-services architecture and must be shipped inside a docker image, in order to be deployable in the cloud;

We expect you to write automated tests for your project.

---
# Docs

### Retrieving CAPTCHA
```
GET /
```
Generates the base64 CAPTCHA image and a unique identifier to associate with the form (_UUIDv4_).

In your registration form you will need:
1. Call the service before rendering the form
2. Integrate the _base64_ image with its validation input field
3. Integrate a hidden field by populating it with the generated uuid

Output example:
```
HTTP/1.0 200 OK
Content-Type: application/json

Body:
{
   "image": "iVBORw0KGgoAAAANSUhEUgAAARgAAABaCAIAAADsC94IAA...", //CAPTCHA Image (base64 encoded)
   "uuid": "600f2d2c-fe27-4097-9269-e27b52398aca" //Form ID
}
```
### Validating the CAPTCHA
`POST /`

Validate the form CAPTCHA image.

Before continuing the registration it will be necessary to call this endpoint passing the form id (_UUIDv4_) and the CAPTCHA code resolved by the user.

To check the validity of the code entered, just check that the call will answer with status code `200`.

Input example:
```
POST /
Content-Type: application/json

Body:
{
    "id_form": "06ab8279-ffbd-49ef-96e8-025d593dffe8",
    "captcha": "V6AKX51"
}
```

Output example:
```
HTTP/1.0 200 OK
Content-Type: application/json

Body:
{
    "message": "Valid captcha"
}
```

---
# Local startup

### Steps to build and run the docker image
- Build the image with the following command:
    ```
    $ docker build -t python-captcha .
    ```

- Run the image with the following command:
    ```
    $ docker run --name python-captcha-test -p 8080:8080 python-captcha
    ```

- You should reach the service at `http://localhost:8080` 

### Testing services

You can cURL the following endpoint to retrieve a captcha image:

```
$ curl localhost:8080
{"image":"...", "uuid":"600f2d2c-fe27-4097-9269-e27b52398aca"}
```

Convert the content of `image` using the following tool
https://codebeautify.org/base64-to-image-converter to view the CAPTCHA image.

Once you decoded the CAPTCHA code, execute the following cURL to validate it (you will need to provide the given `uuid` from the previous request):

```
curl -X POST localhost:8080 \
--header 'Content-Type: application/json' \
--data-raw '{
    "id_form": "<UUID>",
    "captcha": "<CAPTCHA_CODE>"
}'
```

In case of valid CAPTCHA you will get `200` as status code with a message (_Valid captcha_), otherwise you will get a `400` status code with a message indicating which kind of error happened.

---
# Notes
For the convenience of the poc it was chosen to use SQLite.

On a cloud infrastructure it will be necessary to integrate server a database.