#Import Libraries and dependencies
import numpy as np
import numpy as np
import pandas as pd
import os
import alpaca_trade_api as tradeapi
import datetime as dt
import pytz



class MCSimulation:
    """
    A Python Class for running Monte Carolo Simulations on player rosters
    
    Attributes
    __________
    roster : pandas.DataFrame
        players to run the simulation on
    nSim: int
        number of samples in simulation
    nGame: int
        number of games
    simulated_total_points
        simulated data from Monte Carlo
    Confidence Interval: pandas. Series
        the confidence interval
    
    """
    def _init_(self, roster, number_simulation=1000, number_game=13):

        if not isinstance(roster, pd.DataFrame):
            raise TypeError("roster must be a Pandas DataFrame")

        #set weights for roster    
        num_players= len(pd.unique(roster["Player"]))
        weights=[1.0 /num_players for s in range(0,num_players)]

        #Set class attributes

        self.roster=roster
        self.weights=weights
        self.nSim=number_simulation
        self.nGame=num_game
        self.simulated_return=""
        
    def calc_cumulative_return(self):
        
        #Calculates cumulative points of roster 
        
        players=pd.unique(self.roster["Player"]).values.tolist()
        
        
        Calculate average points and std. deviation for each player
        avg_list=[]
        std_list=[]
        
        for i in players:
            filtered_df=roster[roster["Player"]=players[i]]
            
            avg_list.append(filtered_df["Points"].mean())
            std_list.append(filtered_df["Points"].mean())
         
        avg=sum(avg_list)
        std=sum(std_list)
        
        
    
        
        
        
        


    
    