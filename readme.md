[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

## Name
Stock intrinsic value calculator
## Description
Uses free discounted cash flow (10/ 20 years) to estimate intrinsic value of a stock

## Visuals

## Prerequisites

| Python  | > 3.96             |
| :------ | :----------------- |
| Support | :white_check_mark: |

| Database | PostgreSQL               |
| :------- | :----------------------- |
| Support  | :white_check_mark: 12,13 |

Software: 
google chrome
register and get API keys from alpha vantage and rapid-api. put your keys in .env file

On mac, using postgres.app, make sure terminal can locate pg_config (by running "which pg_config" to find out). if not, 
run this on terminal:
sudo mkdir -p /etc/paths.d &&
echo /Applications/Postgres.app/Contents/Versions/latest/bin | sudo tee /etc/paths.d/postgresapp
## Installation
python -m venv .venv
pip install -r requirements.txt
set up .env based on .env.example. make sure to change the dbusername and password

## Usage
python run.py

## Support

## Roadmap

## Authors and acknowledgement

Yangxuan Cho - yangxuan.1996@gmail.com  
Sylvia Goh - sgxh98@gmail.com  

## License

## Resources
- https://finance.yahoo.com/
- https://www.investing.com/
- https://finviz.com/
- <a href="https://www.exchangerate-api.com">Rates By Exchange Rate API</a>
- http://www.market-risk-premia.com/us.html
- http://pages.stern.nyu.edu/~adamodar/New_Home_Page/datafile/ctryprem.html
## Project status

<!-- MARKDOWN LINKS & IMAGES -->

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/yangxuancho
