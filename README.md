<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!--[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]-->
[![MIT License][license-shield]][license-url]
[![Contributors][contributors-shield]][contributors-url]
<!-- [![Forks][forks-shield]][forks-url] -->
[![Stargazers][stars-shield]][stars-url]

<!-- [![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<!-- <br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Best-README-Template</h3>

  <p align="center">
    An awesome README template to jumpstart your projects!
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template">View Demo</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</div> -->



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#branch-info">Information on git branches</a></li>
    <!-- <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li> -->
    <li><a href="#license">License</a></li>
    <li><a href="#developed-by">Developed by</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

A Simulator built from scratch in Python to demonstrate various coexistence scenarios for LTE and WiFi topologies in unlicensed spectrum

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



### Built With

<!-- * [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url] -->




[![Python][python.com]][python-url]
![Shell Script](https://img.shields.io/badge/shell_script-%23121011.svg?style=for-the-badge&logo=gnu-bash&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
Instructions to set up the project locally

### Prerequisites

* Python version 3.9+

### Installation

1. Install Python from [official website](https://www.python.org/)
2. Clone the repo
   ```sh
   git clone https://github.com/chimms1/LTE-WiFi-Simulator.git
   ```
3. Install Python packages (project dependencies)
   ```sh
   pip install numpy pandas matplotlib seaborn tqdm openpyxl
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage


### Classes and Files
All the entities are modeled into various classes

1. Main class `Simulator/main-latest-all.py`: this is the main file that runs the simulation
2. Service class `Simulator/running/ServiceClass.py`: contains all the methods used to perform operations such as creating users, calculating resources, etc.
3. Params class `Simulator/running/ConstantParams.py`: contains the parameters set by the user
4. Verbose class `Simulator/running/Print.py`: contains the flags to print specific information and plot graphs.
5. BaseStation class `Simulator/entities/BaseStation.py`: contains the class definition for LTE BS and Wi-Fi AP.
6. UserEquipment class `Simulator/entities/UserEquipment.py`: contains the class definition for LTE and Wi-Fi User equipment
7. Learning class `Simulator/Qlearning/learning.py`: contains the class definition for Q-learning (reward function, QTable operation, Actions, etc)


### How to execute
1. Set the desired number of users, Number of iterations, Noise, pTx, datarate profile, etc in `ConstantParams.py`
2. Set exploration-exploitation iterations accordingly in `learning.py`
3. Set flags in `Print.py` to print information.
4. Do additional configurations if required.
5. Run `main-latest-all.py`

## NOTE
1. Currently, only a single LTE BS and WiFi AP can be used.
2. As of now load can be varied only once.
3. Increasing users to more than 30 may cause a decrease in SINR.
4. Exceptions are not handled in many cases.
5. Internal code may lack documentation in a few places.
6. Complete research work done in this project is yet to be released
<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Branch Info
1. `main`: has contents of rl-dfs
2. `rl-dfs`: Contains algorithm with 7 states for Dynamic Frame Selection based on Q-Learning
3. `Power-State`: Contains algorithm with 21 states for energy efficient Dynamic Frame Selection based on Q-Learning
4. `dyna-q`: Contains algorithm with 21 states for energy efficient Dynamic Frame Selection based on Dyna-Q+
5. `CSMA/CA`: Development branch used to test implementation of CSMA/CA algorithm present in main file.
6. `dev-y`: Development branch, used for implementation and testing
<!-- ROADMAP -->
<!-- ## Roadmap

- [x] Add Changelog
- [x] Add back to top links
- [ ] Add Additional Templates w/ Examples
- [ ] Add "components" document to easily copy & paste sections of the readme
- [ ] Multi-language Support
    - [ ] Chinese
    - [ ] Spanish

See the [open issues](https://github.com/othneildrew/Best-README-Template/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- CONTRIBUTING -->
<!-- ## Contributing

Contributions are what makes the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- LICENSE -->
## License

Distributed under the LGPL-2.1 License. See `LICENSE.txt` for more information.

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- CONTACT -->
## Developed by

* Yash Deshpande
* Shreyas Joshi
* Ramita Commi
* Gurkirat Singh

<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Resources that we found helpful

* [Computer Networks Theory => Computer Networking: a Top Down Approach by Jim Kurose, Keith Ross](https://gaia.cs.umass.edu/kurose_ross/index.php)
* [Reinforcement Learning/Q Learning](https://www.coursera.org/learn/unsupervised-learning-recommenders-reinforcement-learning)
* [DynaQ+](https://notesonai.com/Dyna-Q+-+Planning+and+Learning)
* [The readme you are currently reading](https://github.com/othneildrew/Best-README-Template)
* [Img Shields](https://shields.io)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Chimms1/LTE-WiFi-Simulator.svg?style=for-the-badge
[contributors-url]: https://github.com/chimms1/LTE-WiFi-Simulator/graphs/contributors
<!-- [forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members -->
[stars-shield]: https://img.shields.io/github/stars/Chimms1/LTE-WiFi-Simulator.svg?style=for-the-badge
[stars-url]: https://github.com/chimms1/LTE-WiFi-Simulator/stargazers

[license-shield]: https://img.shields.io/github/license/Chimms1/LTE-WiFi-Simulator.svg?style=for-the-badge
[license-url]: https://github.com/chimms1/LTE-WiFi-Simulator/blob/main/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://in.linkedin.com/in/yash-deshpande-410567270



[python.com]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/






[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
