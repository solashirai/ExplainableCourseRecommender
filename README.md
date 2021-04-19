# ESCoRe
**E**xplainable **S**emantic **Co**urse **Re**commender

Course recommender system powered by a university course ontology to provide explainable recommendations, developed to provide an examplary implementation of an application that was developed using [FREx](https://github.com/solashirai/FREx). ESCoRe serves as a prototype that demonstrates how to develop recommender systems using the FREx package, so some of the steps used to choose recommendations are quite simple and not necessarily suitable for a "real" application.  More information about FREx can be found [here](https://tetherless-world.github.io/FREx/).

The core data used in this application comes from the [Course Recommendation Ontology (CRO)](https://rpi-ontology-engineering.netlify.app/oe2020/course-recommender/). Additional documentation about the CRO can be found on its website.

## Quickstart

Download a local copy of this repo

Set up and actiavete a new virtual environment, using a 64-bit installation of Python 3.8+.
Within the directory where you downloaded this repository, use the following commands to set up the virtual env and install requirements.
```
$ python3 -m venv venv/
$ venv\Scripts\activate.bat
(venv) $ pip install -r requirements.txt
```
If you're using linux, replace the second step with `source venv/bin/activate` to activate the virtual environment.

You should now be able to run the tests in this repo, using the command `python -m pytest tests/`
