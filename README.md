<div align="center">
<h1>StatsF1 scraper + explorer + predictor</h1>
<em>Bot that download data, explores db and predicts future races</em></br></br>
</div>

<div align="center">
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a> <a href="https://opensource.org/licenses/MIT"><img alt="Open Source Love" src="https://badges.frapsoft.com/os/v1/open-source.svg?v=103"></a> <a href="https://github.com/sirfoga/scrapebots/issues"><img alt="Contributions welcome" src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
</div>


## Example of usage: update
```
/usr/bin/python3.6 scrapebots/bots/statsf1/cli.py -m update
2018-10-02 13:17:02,656 - statsf1 - DEBUG - Got 1950
2018-10-02 13:17:02,656 - statsf1 - DEBUG - Got 1951
2018-10-02 13:17:02,657 - statsf1 - DEBUG - Got 1952
2018-10-02 13:17:02,657 - statsf1 - DEBUG - Got 1953
2018-10-02 13:17:02,657 - statsf1 - DEBUG - Got 1954
2018-10-02 13:17:02,657 - statsf1 - DEBUG - Got 1955
2018-10-02 13:17:02,657 - statsf1 - DEBUG - Got 1956
2018-10-02 13:17:02,658 - statsf1 - DEBUG - Got 1957
2018-10-02 13:17:02,658 - statsf1 - DEBUG - Got 1958
2018-10-02 13:17:02,658 - statsf1 - DEBUG - Got 1959
2018-10-02 13:17:02,658 - statsf1 - DEBUG - Got 1960
2018-10-02 13:17:02,658 - statsf1 - DEBUG - Got 1961
2018-10-02 13:17:02,658 - statsf1 - DEBUG - Got 1962
2018-10-02 13:17:02,658 - statsf1 - DEBUG - Got 1963
2018-10-02 13:17:02,659 - statsf1 - DEBUG - Got 1964
2018-10-02 13:17:02,659 - statsf1 - DEBUG - Got 1965
2018-10-02 13:17:02,659 - statsf1 - DEBUG - Got 1966
2018-10-02 13:17:02,659 - statsf1 - DEBUG - Got 1967
2018-10-02 13:17:02,659 - statsf1 - DEBUG - Got 1968
2018-10-02 13:17:02,659 - statsf1 - DEBUG - Got 1969
2018-10-02 13:17:02,659 - statsf1 - DEBUG - Got 1970
2018-10-02 13:17:02,659 - statsf1 - DEBUG - Got 1971
2018-10-02 13:17:02,659 - statsf1 - DEBUG - Got 1972
2018-10-02 13:17:02,659 - statsf1 - DEBUG - Got 1973
2018-10-02 13:17:02,659 - statsf1 - DEBUG - Got 1974
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1975
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1976
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1977
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1978
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1979
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1980
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1981
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1982
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1983
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1984
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1985
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1986
2018-10-02 13:17:02,660 - statsf1 - DEBUG - Got 1987
2018-10-02 13:17:02,661 - statsf1 - DEBUG - Got 1988
2018-10-02 13:17:02,661 - statsf1 - DEBUG - Got 1989
2018-10-02 13:17:02,661 - statsf1 - DEBUG - Got 1990
2018-10-02 13:17:02,661 - statsf1 - DEBUG - Got 1991
2018-10-02 13:17:02,661 - statsf1 - DEBUG - Got 1992
2018-10-02 13:17:02,661 - statsf1 - DEBUG - Got 1993
2018-10-02 13:17:02,661 - statsf1 - DEBUG - Got 1994
2018-10-02 13:17:02,661 - statsf1 - DEBUG - Got 1995
2018-10-02 13:17:02,661 - statsf1 - DEBUG - Got 1996
2018-10-02 13:17:02,661 - statsf1 - DEBUG - Got 1997
2018-10-02 13:17:02,661 - statsf1 - DEBUG - Got 1998
2018-10-02 13:17:02,661 - statsf1 - DEBUG - Got 1999
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2000
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2001
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2002
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2003
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2004
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2005
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2006
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2007
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2008
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2009
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2010
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2011
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2012
2018-10-02 13:17:02,662 - statsf1 - DEBUG - Got 2013
2018-10-02 13:17:02,663 - statsf1 - DEBUG - Got 2014
2018-10-02 13:17:02,663 - statsf1 - DEBUG - Got 2015
2018-10-02 13:17:02,663 - statsf1 - DEBUG - Got 2016
2018-10-02 13:17:02,663 - statsf1 - DEBUG - Got 2017
2018-10-02 13:17:02,663 - statsf1 - DEBUG - Got 2018
2018-10-02 13:17:03,518 - statsf1 - DEBUG - thread-139801527076672 Australie 2018
2018-10-02 13:17:03,518 - statsf1 - DEBUG - thread-139801527076672 Bahrec3afn 2018
2018-10-02 13:17:03,518 - statsf1 - DEBUG - thread-139801527076672 Chine 2018
2018-10-02 13:17:03,519 - statsf1 - DEBUG - thread-139801527076672 Azerbac3afdjan 2018
2018-10-02 13:17:03,519 - statsf1 - DEBUG - thread-139801527076672 Espagne 2018
2018-10-02 13:17:03,519 - statsf1 - DEBUG - thread-139801527076672 Monaco 2018
2018-10-02 13:17:03,519 - statsf1 - DEBUG - thread-139801527076672 Canada 2018
2018-10-02 13:17:03,519 - statsf1 - DEBUG - thread-139801527076672 France 2018
2018-10-02 13:17:03,519 - statsf1 - DEBUG - thread-139801527076672 Autriche 2018
2018-10-02 13:17:03,519 - statsf1 - DEBUG - thread-139801527076672 Grande-Bretagne 2018
2018-10-02 13:17:03,519 - statsf1 - DEBUG - thread-139801527076672 Allemagne 2018
2018-10-02 13:17:03,520 - statsf1 - DEBUG - thread-139801527076672 Hongrie 2018
2018-10-02 13:17:03,520 - statsf1 - DEBUG - thread-139801527076672 Belgique 2018
2018-10-02 13:17:03,520 - statsf1 - DEBUG - thread-139801527076672 Italie 2018
2018-10-02 13:17:03,520 - statsf1 - DEBUG - thread-139801527076672 Singapour 2018
2018-10-02 13:17:03,520 - statsf1 - DEBUG - thread-139801527076672 Russie 2018
2018-10-02 13:17:03,520 - statsf1 - DEBUG - thread-139801527076672 Japon 2018
2018-10-02 13:17:03,520 - statsf1 - DEBUG - thread-139801527076672 Etats-Unis 2018
2018-10-02 13:17:03,520 - statsf1 - DEBUG - thread-139801527076672 Mexique 2018
2018-10-02 13:17:03,521 - statsf1 - DEBUG - thread-139801527076672 Brc3a9sil 2018
2018-10-02 13:17:03,521 - statsf1 - DEBUG - thread-139801527076672 Abou Dhabi 2018
2018-10-02 13:17:03,521 - statsf1 - DEBUG - Found 21 races
2018-10-02 13:17:11,276 - statsf1 - DEBUG - thread-139800170456832 France 2018
2018-10-02 13:17:11,349 - statsf1 - DEBUG - thread-139800574134016 Bahrec3afn 2018
2018-10-02 13:17:11,371 - statsf1 - DEBUG - thread-139800555292416 Chine 2018
2018-10-02 13:17:11,447 - statsf1 - DEBUG - thread-139800178849536 Canada 2018
2018-10-02 13:17:11,524 - statsf1 - DEBUG - thread-139800582526720 Australie 2018
2018-10-02 13:17:11,826 - statsf1 - DEBUG - thread-139800530114304 Monaco 2018
2018-10-02 13:17:12,655 - statsf1 - DEBUG - thread-139800538507008 Espagne 2018
2018-10-02 13:17:15,480 - statsf1 - DEBUG - thread-139800546899712 Azerbac3afdjan 2018
2018-10-02 13:17:16,219 - statsf1 - DEBUG - thread-139800170456832 Autriche 2018
2018-10-02 13:17:16,375 - statsf1 - DEBUG - thread-139800555292416 Allemagne 2018
2018-10-02 13:17:16,829 - statsf1 - ERROR - thread-139800170456832 Japon 2018 because incorrect parsing http://www.statsf1.com/en/2018/japon.aspx
2018-10-02 13:17:16,829 - statsf1 - ERROR - thread-139800170456832 Japon 2018 because incorrect dict conversion http://www.statsf1.com/en/2018/japon.aspx
2018-10-02 13:17:16,831 - statsf1 - DEBUG - thread-139800170456832 Japon 2018
2018-10-02 13:17:16,848 - statsf1 - ERROR - thread-139800555292416 Etats-Unis 2018 because incorrect parsing http://www.statsf1.com/en/2018/etats-unis.aspx
2018-10-02 13:17:16,849 - statsf1 - ERROR - thread-139800555292416 Etats-Unis 2018 because incorrect dict conversion http://www.statsf1.com/en/2018/etats-unis.aspx
2018-10-02 13:17:16,850 - statsf1 - DEBUG - thread-139800555292416 Etats-Unis 2018
2018-10-02 13:17:17,002 - statsf1 - DEBUG - thread-139800178849536 Hongrie 2018
2018-10-02 13:17:17,244 - statsf1 - ERROR - thread-139800555292416 Brc3a9sil 2018 because incorrect parsing http://www.statsf1.com/en/2018/bresil.aspx
2018-10-02 13:17:17,246 - statsf1 - ERROR - thread-139800555292416 Brc3a9sil 2018 because incorrect dict conversion http://www.statsf1.com/en/2018/bresil.aspx
2018-10-02 13:17:17,249 - statsf1 - DEBUG - thread-139800555292416 Brc3a9sil 2018
2018-10-02 13:17:17,256 - statsf1 - ERROR - thread-139800170456832 Mexique 2018 because incorrect parsing http://www.statsf1.com/en/2018/mexique.aspx
2018-10-02 13:17:17,257 - statsf1 - ERROR - thread-139800170456832 Mexique 2018 because incorrect dict conversion http://www.statsf1.com/en/2018/mexique.aspx
2018-10-02 13:17:17,259 - statsf1 - DEBUG - thread-139800170456832 Mexique 2018
2018-10-02 13:17:17,276 - statsf1 - DEBUG - thread-139800582526720 Belgique 2018
2018-10-02 13:17:17,928 - statsf1 - DEBUG - thread-139800538507008 Singapour 2018
2018-10-02 13:17:18,103 - statsf1 - DEBUG - thread-139800530114304 Italie 2018
2018-10-02 13:17:18,213 - statsf1 - ERROR - thread-139800178849536 Abou Dhabi 2018 because incorrect parsing http://www.statsf1.com/en/2018/abou-dhabi.aspx
2018-10-02 13:17:18,214 - statsf1 - ERROR - thread-139800178849536 Abou Dhabi 2018 because incorrect dict conversion http://www.statsf1.com/en/2018/abou-dhabi.aspx
2018-10-02 13:17:18,217 - statsf1 - DEBUG - thread-139800178849536 Abou Dhabi 2018
2018-10-02 13:17:18,345 - statsf1 - DEBUG - thread-139800574134016 Grande-Bretagne 2018
2018-10-02 13:17:18,534 - statsf1 - DEBUG - thread-139800546899712 Russie 2018

Process finished with exit code 0
```

## Example of usage: predict
```
/usr/bin/python3.6 scrapebots/bots/statsf1/cli.py -m predict

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
