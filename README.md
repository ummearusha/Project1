# Project1 - Applying FinTech concepts to Fantasy Football 
A number of quantitative concepts used in financial analysis and portfolio management are adaptable for use in fantasy football. In this project, we built tools to identify optimal team/individual players (portfolio) to maximize fantasy points (returns) given constraints around roaster construction, budget and player volatity. We built tools to analyse players' historical performance, project future performance and used this to generate the optimal roaster/team.

## Key Files
1. Final_Project.ipynb : Jupyter Notebook file. Script utilized to run monte carlo simulations on fantasy football rosters and create visualizations of historic performance of players and positions
2. MCForecastFantasy.py : Python file. Creates MCSimulation class which is utilized in the Final_Project file for running monte carlo simulations. 
3. LineupOptimizer.ipynb :  Jupyter Notebook file Script utilized to select an optimal fantasy football roster for Fanduel. 
4. Project 1 - Fantasy Football.pdf : PDF presentation of our project

## Key Findings

1. Football is highly variable sport, when comparing two rosters with monte carlo simulations, the probability of one team winning relative to another changes significantly from 500 simulations to 1000 (typically from ~50% to ~60%)
2. PuLP Optimization package are useful tools for solving constrained optimization problems such as choosing the optimal fantasy football rosters
3. Historically speaking, performance at individual positions generally has a few outliers each year. Fantasy football players should attempt to identify these outliers when selecting fantasy football teams.


