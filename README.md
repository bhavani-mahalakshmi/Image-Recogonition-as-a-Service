<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Elastic Web Application - Image Recognition</h3>
  <p align="center">
    A web application that uses AWS EC2, SQS and S3 to provide image recognition as a service to users.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Frameworks/Tools Used</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">References</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

**Group Members:**


Panemangalore Srikanth Kini


Arindam Jain


Bhavani Mahalakshmi Gowri Sankar



**Web Tier URL:**
http://52.91.101.27:8080/

**SQS Queue Names:**


Input Queue = Request-Queue


Output Queue = Response-Queue

**S3 Bucket Names:**


INPUT_BUCKET = input-image-files


OUTPUT_BUCKET = output-image-files

This is the project for the course CSE 546 - Cloud Computing. It consists of a three-tier architecture (web-tier, 
app-tier and the data-tier) which uses AWS resources to elastically scale in and out proportionally with respect to the load.

High level overview:
* The web-tier consists of a flask server that allows users to upload images. The server pushes the images along with a unique identifier to SQS input queue and reads the output SQS queue to return the classification of the image to the user. 
* The app-tier consists of a back-end service that reads the input queue, puts the image into the input S3 bucket, classifies the image, puts the result into the output S3 bucket as well as the output SQS queue.
* The data-tier consists of the input and output S3 buckets which contain the input images and the classifications.

The web-tier also comprises an auto-scaling controller service that utilizes the length of input SQS queue to scale out automatically whereas the logic to scale in is handled in the app-tier.

<p align="right">(<a href="#top">back to top</a>)</p>

### Frameworks/Tools Used

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for the acknowledgements section. Here are a few examples.

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Boto3](https://aws.amazon.com/sdk-for-python/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This section contains instructions on setting up the project locally.
To get a local copy up and running follow these simple steps.

There are two folders, web-tier and app-tier each containing their separate dependencies and code.
To install the required dependencies, run

```
pip3 install -r requirements.txt
```

For running the main flask server:

```
cd web-tier/
flask run --host <host> --port <port>
```

For running the controller script to perform auto-scaling:

```
cd web-tier/auto-scaler/
python3 controller.py
```

For running the app-tier code, first install the dependancies using pip.
Then run the main.py file using

```
python3 main.py
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.md` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- REFERENCES -->
## References

* [Choose an Open Source License](https://choosealicense.com)
* [AWS SDK for Python (boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* [Web Development with Flask](https://flask.palletsprojects.com/en/2.0.x/)

<p align="right">(<a href="#top">back to top</a>)</p>
