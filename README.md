<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** kajuberdut, version_machine, twitter_handle, patrick.shechet@gmail.com, version_machine, String functions in pure Python
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/kajuberdut/version_machine">
    <img src="https://raw.githubusercontent.com/kajuberdut/version_machine/main/images/icon.svg" alt="icon" width="160" height="160">
  </a>

  <h3 align="center">version_machine</h3>

  <p align="center">
    Single file helper for bumping version. 
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#usage">Usage</a>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <!-- <li><a href="#license">License</a></li> -->
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

version_machine bumps version strings in files.


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installing with pip

  ```sh
  pip install version_machine
  ```

  Alternately, you can copy version_machine/core.py from this library into your own project and run the file as a script.

For information about cloning and dev setup see: [Contributing](#Contributing)


<!-- USAGE EXAMPLES -->
## Usage

### CLI
version_machine can be run with defaults from the command line:

```console
foo@bar:~$ version_machine path/to/file.py
```

The best way to configure behavior is to add entries to pyproject.toml:

```toml
[tool.version_machine]
  path = "version_machine/__version__.py"
  increment_type = "patch"
```

### Functional use
Version machine provides "version_travel" which can be called inside your pythone code.


```python
from version_machine import version_travel
from pathlib import Path

THIS_FILE = Path(__file__)
example_path = THIS_FILE.parent / "example_version.py" 

version_travel(path=example_path, increment_type="major")
```

examples/example_version.py is update by the above code from:

```python
__version__ = "0.0.1"
```

to:

```python
__version__ = "1.0.1"
```

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Add tests, we aim for 100% test coverage [Using Coverage](https://coverage.readthedocs.io/en/coverage-5.3.1/#using-coverage-py)
4. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the Branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

### Cloning / Development setup
1. Clone the repo and install
    ```sh
    git clone https://github.com/kajuberdut/version_machine.git
    cd version_machine
    pipenv install --dev
    ```
2. Run tests
    ```sh
    pipenv shell
    ward
    ```
  For more about pipenv see: [Pipenv Github](https://github.com/pypa/pipenv)



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Patrick Shechet - patrick.shechet@gmail.com

Project Link: [https://github.com/kajuberdut/version_machine](https://github.com/kajuberdut/version_machine)




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/kajuberdut/version_machine.svg?style=for-the-badge
[contributors-url]: https://github.com/kajuberdut/version_machine/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/kajuberdut/version_machine.svg?style=for-the-badge
[forks-url]: https://github.com/kajuberdut/version_machine/network/members
[stars-shield]: https://img.shields.io/github/stars/kajuberdut/version_machine.svg?style=for-the-badge
[stars-url]: https://github.com/kajuberdut/version_machine/stargazers
[issues-shield]: https://img.shields.io/github/issues/kajuberdut/version_machine.svg?style=for-the-badge
[issues-url]: https://github.com/kajuberdut/version_machine/issues
[license-shield]: https://img.shields.io/badge/License-MIT-orange.svg?style=for-the-badge
[license-url]: https://github.com/kajuberdut/version_machine/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/patrick-shechet
