#Import Libraries and dependencies
import numpy as np
import numpy as np
import pandas as pd
import os
import datetime as dt
import pytz



class MCSimulation:
    """
    A Python Class for running Monte Carlo Simulations on player rosters
    
    Attributes
    __________
    roster : pandas.DataFrame
        players to run the simulation on
    nSim: int
        number of samples in simulation
    nGame: int
        number of games
    simulated_weekly_points : pandas.DataFrame
        simulated weekly data from Monte Carlo
    simulated_szn_points : pandas.DataFrame
        simulated season data from Monte Carlo
    szn_end_points : pandas.DataFrame
        simulated points at end of season
    weekly_confidence_interval: pandas.Series
        the95% confidence intervals for weekly points
    szn_confidence_interval: pandas.Series
        the 95% confidence intervals for weekly points
    avg_szn_confidence_interval: pandas.Series
        the 95% confidence intervals for average weekly points across nGame season
    
    """
    def __init__(self, roster, weights="", number_simulation=1000, number_game=13):

        if not isinstance(roster, pd.DataFrame):
            raise TypeError("roster must be a Pandas DataFrame")

        #set weights for roster    
        num_players= len(pd.unique(roster["Player"]))
        weights=[1.0 /num_players for s in range(0,num_players)]

        #Set class attributes

        self.roster=roster
        self.weights=weights
        self.nSim=number_simulation
        self.nGame=number_game
        self.simulated_weekly_points=""
        self.simulated_szn_points=""
        self.szn_end_points=""
        
    def calc_points(self):
        
        #Calculates roster points weekly and season long 
        
        players=pd.unique(self.roster["Player"]).tolist()
        
        
        #Calculate average points and std. deviation for each player
        avg_list=[]
        std_list=[]
        
        for i in players:
            filtered_df=self.roster[self.roster["Player"]==i]
            
            avg_list.append(filtered_df["Points"].mean())
            std_list.append(filtered_df["Points"].std())
         
       
        std_square=0
        
        #Loop through and calculate variance
        for i in std_list:
            std_square+=i**2
       
        # calculate mean and std
        avg=sum(avg_list)
        std=np.sqrt(std_square)
        
        #initialize the dataframes to hold weekly points and total points
        points_weekly=pd.DataFrame()
        points_szn=pd.DataFrame()
        
        #Run the simulation of projecting points scored nSim number of times
        for n in range(self.nSim):
            #uncomment the below if you want to see each time that the simulation runs
            #if n%10 ==0:
             #   print(f"Running Monte Carlo simulation number {n}.")
            sim_vals_week=[]
            sim_vals_szn=[]
        
            #simulate points for each game
            for i in range(self.nGame):
                sim_vals_week.append(np.random.normal(avg,std))
                
                if len(sim_vals_szn)==0:
                    sim_vals_szn.append(np.random.normal(avg,std))
                else:
                    sim_vals_szn.append(sim_vals_szn[-1]+np.random.normal(avg,std))
                
            
            #sim_week_df=pd.DataFrame(sim_vals_week).to_series()
            #sim_szn_df=pd.DataFrame(sim_vals_szn).to_series()
            
            points_weekly[n]=sim_vals_week
            points_szn[n]=sim_vals_szn
            
        
        #set attributes used for weekly and season long plotting
        self.simulated_weekly_points=points_weekly
        self.simulated_szn_points=points_szn
        self.szn_end_points=points_szn.iloc[-1,:]
        
        #Calculate 95% confidence intervals for cumulative and weekly points
        self.weekly_confidence_interval=points_weekly.iloc[-1,:].quantile(q=[0.025,0.975])
        self.szn_confidence_interval=points_szn.iloc[-1,:].quantile(q=[0.025,0.975])
        self.avg_szn_confidence_interval=(points_szn.iloc[-1,:].div(self.nGame)).quantile(q=[0.025,0.975])
        
        
        return points_szn
    
    
    def plot_weekly_simulation(self):
        """
        Visulizes weekly point performance using calc_points method 
        """
        
        
        #check to make sure simulation has run
        if not isinstance(self.simulated_weekly_points,pd.DataFrame):
            self.calc_points()
            
            #use pandas plot function to plot the weekly points data
        plot_title=f"{self.nSim} Simulations of weekly roster points over the next {self.nGame} games"
        return self.simulated_weekly_points.plot(legend=None,title=plot_title)
    
    def plot_szn_simulation(self):
        """
        Visulizes season long (cumulative) point performance using calc_points method 
        
        """    
        
        #check to make sure simulation has run
        if not isinstance(self.simulated_szn_points,pd.DataFrame):
            self.calc_points()
            
            #use pandas plot function to plot the weekly points data
        plot_title=f"{self.nSim} Simulations of cumulative roster points over the next {self.nGame} games"
        return self.simulated_szn_points.plot(legend=None,title=plot_title)
    
    
    def plot_szn_distribution(self):
        """
        Visualizes the distribution of cumulative (season long) points simulated using the calc_points method
        """
        
        #check to make sure the simulation has run
        if not isinstance(self.simulated_szn_points,pd.DataFrame):
            self.calc_points()
            
       # Use the `plot` function to create a probability distribution histogram of simulated season ending scores
        # with markings for a 95% confidence interval
            
        plot_title=f"Distribution of cumulative season long point production of roster across all {self.nSim} Simulations"
        plt = self.simulated_szn_points.iloc[-1,:].plot(kind='hist', bins=10,density=True,title=plot_title)
        plt.axvline(self.szn_confidence_interval.iloc[0], color='r')
        plt.axvline(self.szn_confidence_interval.iloc[1],color='r')
        return plt
    
    def plot_avg_szn_distribution(self):
        """
        Visualizes the distribution of cumulative (season long) points simulated using the calc_points method
        """
        
        #check to make sure the simulation has run
        if not isinstance(self.simulated_szn_points,pd.DataFrame):
            self.calc_points()
            
       # Use the `plot` function to create a probability distribution histogram of simulated season ending scores
        # with markings for a 95% confidence interval
            
        plot_title=f"Distribution of avg. points per game production of roster across {self.nGame} weeks across all {self.nSim} Simulations"
        
        avg_points=self.simulated_szn_points.iloc[-1,:].div(self.nGame)
        plt = avg_points.plot(kind='hist', bins=10,density=True,title=plot_title)
        plt.axvline(self.avg_szn_confidence_interval.iloc[0], color='r')
        plt.axvline(self.avg_szn_confidence_interval.iloc[1],color='r')
        return plt    
    
    
    def summarize_szn_points(self):
        """
        Summarize season long performance distribution
        """
        if not isinstance(self.simulated_szn_points,pd.DataFrame):
            self.calc_points()
            
        
        metrics=self.simulated_szn_points.iloc[-1].describe()
        ci_series=self.szn_confidence_interval
        ci_series.index= ["95% CI Lower", "95% CI Upper"]
        return metrics.append(ci_series)
        
    
    def summarize_avg_szn_points(self):
        """
        Summarize average season long performance distribution
        """        
        if not isinstance(self.simulated_szn_points,pd.DataFrame):
            self.calc_points()
        
        metrics=(self.simulated_szn_points.iloc[-1].div(self.nGame)).describe()
        ci_series=self.avg_szn_confidence_interval
        ci_series.index=['95% CI Lower', '95% CI Upper']
        return metrics.append(ci_series)
        
        
     
        
        
        
        
                
        
        
        
        
    
        
        
        
        


    
    