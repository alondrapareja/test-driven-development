# Experiment class to manage different conditions, compute the ROC curve, and compute the AUC.

import numpy as np
import matplotlib.pyplot as plt
from SignalDetection import SignalDetection

class Experiment:
    def __init__(self): #Initializes an empty list to store SDT objects and their corresponding condition labels
        self.conditions = []
        self.labels = [] 

    def add_condition (self, sdt_obj: SignalDetection, label: str = None) -> None: #Adds an SignalDetection object and an optional lebel to the experiment 
        if not isinstance(sdt_obj,SignalDetection):
            raise TypeError("Error: sdt_object must be an instance from the SignalDetection class")
        self.conditions.append(sdt_obj)
        self.labels.append(label)

    def sorted_roc_points(self) -> tuple[list[float], list[float]]: #Returns the sorted false alarm rates and hit rates necessary for plotting the ROC curve
        if not self.conditions:
            raise ValueError("Error: No conditoons have been added to the experiment.")
        
        falseAlarm_rates = []
        hitRates = []

        for condition in self.conditions:
            fa_rate = condition.falseAlarms_rate()
            hit_rate = condition.hits_rate()

            #Prevent dividing by 0 errors 
            fa_rate = fa_rate if (condition.falseAlarms + condition.correctRejections) > 0 else 0.0
            hit_rate = hit_rate if (condition.hits + condition.misses) > 0 else 0.0

            falseAlarm_rates.append(fa_rate)
            hitRates.append(hit_rate)
        
        sorted_indices = np.argsort(falseAlarm_rates)
        sorted_falseAlarm_rates = [falseAlarm_rates[i] for i in sorted_indices]
        sorted_hitRates = [hitRates[i] for i in sorted_indices]

        return sorted_falseAlarm_rates,sorted_hitRates
    
    def compute_auc(self) -> float: #Computes the AUC for the stored SDT conditions
        if not self.conditions:
            raise ValueError("Error: No conditions have been added to compute the Area Under the Curve")
        
        if len(self.conditions)<2:
            raise ValueError("Error: Need at least 2 conditions to compute Area Under the Curve")
        
        falseAlarm_rates,hitRates = self.sorted_roc_points()
        auc_score = np.trapezoid(hitRates,falseAlarm_rates)
        return auc_score
    
    def plot_roc_curve(self, show_plot: bool = True): #Plots the ROC Curve
        falseAlarm_rates, hitRates = self.sorted_roc_points()

        plt.figure()
        plt.plot(falseAlarm_rates, hitRates,label = "ROC Curve")
        plt.plot([0,1],[0,1],"k--",label="Random Guess")
        plt.xlabel("False Alarm Rate")
        plt.ylabel("Hit Rate")
        plt.title("ROC Curve")
        plt.legend()

        if show_plot:
            plt.show()

             

        


