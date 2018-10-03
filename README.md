<div align="center">
<h1>StatsF1 explorer + predictor</h1>
<em>Bot that explores db and predicts future races</em></br></br>
</div>

<div align="center">
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a> <a href="https://opensource.org/licenses/MIT"><img alt="Open Source Love" src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103"></a> <a href="https://github.com/sirfoga/scrapebots/issues"><img alt="Contributions welcome" src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
</div>

## How

### Explore
- `statsf1.tools.explorer.RaceExplorer` uses `MongoDB` to fetch result from local db
- `statsf1.tools.stats.Statistician` uses probability distributions (mainly Gaussians) to get probabilities of the outcomes
- `statsf1.tools.predict.Predictor` uses various machine learning techniques (mainly regressors and
 to classifiers) to predict the outcomes


## Example of usage: stats
```
/usr/bin/python3.6 statsf1/cli.py -m stats

*** # drivers who complete the race
--- normal distribution 18.052 +- 1.881
    P(> 15.5) = 0.862 <-- best
    P(< 15.5) = 0.052
    P(> 16.5) = 0.712
    P(< 16.5) = 0.138
    P(> 17.5) = 0.511
    P(< 17.5) = 0.288
--- probability VS stakes (more is better)
    P(> 15.5) = 1.168 <-- best
    P(< 15.5) = 0.006
    P(> 16.5) = 1.014
    P(< 16.5) = 0.033
    P(> 17.5) = 0.914
    P(< 17.5) = 0.106

*** Drivers who complete the race
--- who complets? Everyone, except the following:
    P(Fernando ALONSO) = 0.714
      P(Jules BIANCHI) = 0.500
    P(Sébastien BUEMI) = 0.000
    P(Marcus ERICSSON) = 0.750
P(Giedo van der GARDE) = 0.000
     P(Lewis HAMILTON) = 0.857
    P(Nico HULKENBERG) = 0.833
 P(Narain KARTHIKEYAN) = 0.000
       P(Sergio PEREZ) = 0.857
        P(Charles PIC) = 0.500
       P(Nico ROSBERG) = 0.833
       P(Carlos SAINZ) = 0.667
       P(Lance STROLL) = 0.000
   P(Sebastian VETTEL) = 0.857

*** Q time win margin
--- normal distribution 0.423 +- 0.587
     P(< 0.1) = 0.291
 P(0.1 < 0.2) = 0.061
     P(> 0.2) = 0.648 <-- best
--- probability VS stakes (more is better)
     P(< 0.1) = 0.222
 P(0.1 < 0.2) = 0.011
     P(> 0.2) = 1.050 <-- best

*** Race time win margin
--- normal distribution 9.037 +- 7.335
     P(< 3.0) = 0.205
 P(3.0 < 6.0) = 0.134
     P(> 6.0) = 0.661 <-- best
--- probability VS stakes (more is better)
     P(< 3.0) = 0.137
 P(3.0 < 6.0) = 0.063
     P(> 6.0) = 0.829 <-- best

*** Q position of winner
--- normal distribution 1.571 +- 0.495
         P(1) = 0.427
         P(2) = 0.527 <-- best
       P(3-4) = 0.030
       P(5-7) = 0.000
      P(8-13) = 0.000
     P(14-20) = 0.000
--- probability VS stakes (more is better)
         P(1) = 0.296
         P(2) = 1.042 <-- best
       P(3-4) = 0.006
       P(5-7) = 0.000
      P(8-13) = 0.000
     P(14-20) = 0.000

*** Race summary
--- summary of Japon in 2017
+----------+------------------+-------------+-----------+-----------------+----------------+-------+----------+-----------+--------------+----------+---------------+
| race pos |           driver |     chassis | race laps | race completed? |      race time | Q pos |   Q time | race VS Q | best lap pos | best lap | best lap VS Q |
+----------+------------------+-------------+-----------+-----------------+----------------+-------+----------+-----------+--------------+----------+---------------+
|        1 |   Lewis HAMILTON |    Mercedes |        53 |             yes | 1h 27m 31.194s |     1 | 1'27"319 |         0 |            6 | 1'33"780 |        7.399% |
|        2 |   Max VERSTAPPEN |    Red Bull |        53 |             yes | 1h 27m 32.405s |     5 | 1'28"332 |        -3 |            5 | 1'33"730 |        6.111% |
|        3 | Daniel RICCIARDO |    Red Bull |        53 |             yes | 1h 27m 40.873s |     4 | 1'28"306 |        -1 |            3 | 1'33"694 |        6.102% |
|        4 |  Valtteri BOTTAS |    Mercedes |        53 |             yes | 1h 27m 41.774s |     2 | 1'27"651 |         2 |            1 | 1'33"144 |        6.267% |
|        5 |   Kimi RAIKKONEN |     Ferrari |        53 |             yes | 1h 28m 03.816s |     6 | 1'28"498 |        -1 |            2 | 1'33"175 |        5.285% |
|        6 |     Esteban OCON | Force India |        53 |             yes | 1h 28m 38.982s |     7 | 1'29"111 |        -1 |           11 | 1'34"843 |        6.432% |
|        7 |     Sergio PEREZ | Force India |        53 |             yes | 1h 28m 42.618s |     8 | 1'29"260 |        -1 |           10 | 1'34"744 |        6.144% |
|        8 |  Kevin MAGNUSSEN |        Haas |        53 |             yes | 1h 29m 00.147s |    13 | 1'29"972 |        -5 |           13 | 1'35"338 |        5.964% |
|        9 |  Romain GROSJEAN |        Haas |        53 |             yes | 1h 29m 01.077s |    16 | 1'30"849 |        -7 |           14 | 1'35"347 |        4.951% |
|       10 |     Felipe MASSA |    Williams |        52 |             yes |                |     9 | 1'29"480 |         1 |           16 | 1'35"943 |        7.223% |
+----------+------------------+-------------+-----------+-----------------+----------------+-------+----------+-----------+--------------+----------+---------------+

*** Driver summary
--- summary of Lewis HAMILTON at Japon from 2011 to 2017
+------+----------+----------+-----------+-----------------+----------------+-------+----------+-----------+--------------+----------+---------------+
| year | race pos |  chassis | race laps | race completed? |      race time | Q pos |   Q time | race VS Q | best lap pos | best lap | best lap VS Q |
+------+----------+----------+-----------+-----------------+----------------+-------+----------+-----------+--------------+----------+---------------+
| 2017 |        1 | Mercedes |        53 |             yes | 1h 27m 31.194s |     1 | 1'27"319 |         0 |            6 | 1'33"780 |        7.399% |
| 2016 |        3 | Mercedes |        53 |             yes | 1h 26m 49.109s |     2 | 1'30"660 |         1 |            2 | 1'35"152 |        4.955% |
| 2015 |        1 | Mercedes |        53 |             yes | 1h 28m 06.508s |     2 | 1'32"660 |        -1 |            1 | 1'36"145 |        3.761% |
| 2014 |        1 | Mercedes |        44 |             yes | 1h 51m 43.021s |     2 | 1'32"703 |        -1 |            1 | 1'51"600 |       20.384% |
| 2013 |        - | Mercedes |         7 |              no |      Fond plat |     3 | 1'31"253 |         - |           20 | 1'41"202 |       10.903% |
| 2012 |        5 |  McLaren |        53 |             yes | 1h 29m 42.732s |     9 | 1'32"327 |        -4 |           11 | 1'37"760 |        5.885% |
| 2011 |        5 |  McLaren |        53 |             yes | 1h 31m 17.695s |     3 | 1'30"617 |         2 |            9 | 1'37"645 |        7.756% |
+------+----------+----------+-----------+-----------------+----------------+-------+----------+-----------+--------------+----------+---------------+

Process finished with exit code 0
```


## Install
See [README](https://github.com/sirfoga/scrapebots)


## Contributing
See [README](https://github.com/sirfoga/scrapebots)


## Feedback
See [README](https://github.com/sirfoga/scrapebots)


## License
[MIT License](https://opensource.org/licenses/MIT)
