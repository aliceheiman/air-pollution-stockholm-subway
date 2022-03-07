<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">Air Pollution Stockholm Subway</h3>

  <p align="center">
    Research project mapping the air pollution in the Stockholm subway.
    <br />
    <a href="https://github.com/aliceheiman/air-pollution-stockholm-subway"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/aliceheiman/air-pollution-stockholm-subway/issues">Report Bug</a>
    ·
    <a href="https://github.com/aliceheiman/air-pollution-stockholm-subway/issues">Request Feature</a>
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
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#organization">Organization</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
    </li>
    <li>
      <a href="#license">License</a>
    </li>
    <li>
      <a href="#contact">Contact</a>
    </li>
    <li>
      <a href="#additional-links">Additional Links</a>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

High concentrations of particulate matter have been measured in several subway networks worldwide. The results from these studies raise concerns about the potential adverse health effects for both passengers and Metro workers. In Stockholm, Sweden, commuting by subway is a popular mode of transportation, making it relevant to investigate commuter exposure to particulate matter. This study aims to measure PM2.5 mass and UFP number concentration at 20 stations along the Green Line in the Stockholm subway. Measurements were taken using two different sensor types by repeatedly jumping on and off the platforms. A custom mobile application and an extensive data- and statistical analysis were used to collect and analyze the data. It was found that indoor stations had significantly higher PM2.5 levels and bigger PM2.5 particles than outdoor stations. Indoor stations Hötorget, T-Centralen, and Rådmansgatan had the highest PM2.5 means. The results were compared to the WHO Air Quality Guidelines, and stations in the Stockholm subway probably exceed the annual and 24-hour PM2.5 reference values. The highest $\mathrm{UFP}$ number concentrations were recorded at outdoor stations Kristineberg, Thorildsplan, and Gullmarsplan. These findings highlight the importance of investigating subway air quality and show potential to aid future research into this relevant topic.

## About This Repo

This repository contains all the code used as part of a High School Diploma Project analyzing the particulate matter concentrations in the Stockholm subway. 

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/aliceheiman/air-pollution-stockholm-subway.git
   ```
2. Install environment
   ```sh
   pip install -e .
   ```

### Organization

The project is organized into folders:

- **data**: raw and sorted data from the sensors used in the experiments
- **docs**: "read-the-docs" style generated documentation
- **results**: graphs, tables, and computations
- **scripts**: iPython Jupyter Notebooks containing all analysis code
- **src**: reusable python scripts with modular functions

<!-- USAGE EXAMPLES -->
## Usage

All data is found under the **data** folder. To reproduce the results and graphs, use the iPython notebooks in the **scripts** folder. The scripts are structured into the following files:

- **Calibration A**: Analysis of sensor calibration data in a stable inside environment.
- **Calibration B**: Analysis of sensor calibration data in a park.
- **Calibration C**: Analysis of sensor calibration data while cooking.
- **DownMiddleUp**: Analysis of measurements taken at the commuter and subway stations at Odenplan in Stockholm.
- **Sessions DiSCMini**: Data preprocessing and extraction from the DiSC Mini sensor.
- **Sessions Sensirion**: Data preprocessing and extraction from the Sensirion SPS30 sensors.
- **Stations DiSC**: Analysis of Disc Mini station data.
- **Stations Sensirion**: Analysis of Sensirion SPS30 station data.

Feel free to play around with the data and graphs!

<!-- _For more examples, please refer to the [Documentation](https://example.com)_ -->

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information. If using the data provided in this repo, it would be greatly appreciated to refer to this site.



<!-- CONTACT -->
## Contact

Alice Heiman - kod@heiman.se

Project Link: [https://github.com/aliceheiman/air-pollution-stockholm-subway](https://github.com/aliceheiman/air-pollution-stockholm-subway)



<!-- ACKNOWLEDGEMENTS -->
## Additional Links

* [#](Full Paper: Exposure to Particulate Matter and Ultrafine Particles in the Stockholm Subway)
