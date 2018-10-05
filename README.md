<div align="center">
<h1>StatsF1 explorer + predictor</h1>
<em>Bot that explores db and predicts future races</em></br></br>
</div>

<div align="center">
<a href="https://snyk.io/test/github/sirfoga/statsf1"><img alt="Known Vulnerabilities" src="https://snyk.io/test/github/sirfoga/statsf1/badge.svg"></a><br>
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a> <a href="https://opensource.org/licenses/MIT"><img alt="Open Source Love" src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103"></a> <a href="https://github.com/sirfoga/statsf1/issues"><img alt="Contributions welcome" src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
</div>

## How it's implemented
- `statsf1.tools.explorer.RaceExplorer` uses `MongoDB` to fetch result from local db
- `statsf1.tools.stats.Statistician` uses probability distributions (mainly Gaussians) to get probabilities of the outcomes
- `statsf1.tools.predict.Predictor` uses various machine learning techniques (mainly regressors and
 to classifiers) to predict the outcomes


## Example of usage: `explore` mode
```
todo
Process finished with exit code 0
```

## Example of usage: `stats` mode
```
todo
Process finished with exit code 0
```

## Example of usage: `predict` mode
```
todo
Process finished with exit code 0
```


## Install
Running `pip3 install .` will take care of all dependencies. Moreover you need the `MongoDB` database: you can download it with [this bot](https://github.com/sirfoga/scrapebots/tree/master/bots/statsf1).


## Contributing
[Fork](https://github.com/sirfoga/statsf1/fork) | Patch | Push | [Pull request](https://github.com/sirfoga/statsf1/pulls)


## Feedback
Suggestions and improvements are [welcome](https://github.com/sirfoga/statsf1/issues)!


## License
[MIT License](https://opensource.org/licenses/MIT)


## Authors
| [![sirfoga](https://avatars0.githubusercontent.com/u/14162628?s=128&v=4)](https://github.com/sirfoga "Follow @sirfoga on Github") |
|---|
| [Stefano Fogarollo](https://sirfoga.github.io) |


## Thanks to
The awesome [statsf1](http://www.statsf1.com) database and its authors!

## License
[MIT License](https://opensource.org/licenses/MIT)
