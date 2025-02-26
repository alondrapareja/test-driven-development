import numpy as np
import matplotlib.pyplot as plt
from SignalDetection import SignalDetection 

class Experiment:
    def __init__(self):
        #Initializes an empty list to store SignalDetection objects and their labels
        self.conditions = []  #Stores tuples of (SignalDetection object, label)

    def add_condition(self, sdt_obj: SignalDetection, label: str = None) -> None:
        #Adds a SignalDetection object with an optional label
        if not isinstance(sdt_obj, SignalDetection):
            raise TypeError("sdt_obj has be an instance of SignalDetection")
        self.conditions.append((sdt_obj, label))

    def sorted_roc_points(self) -> tuple:
        #Returns sorted false alarm rates and hit rates for plotting the ROC curve
        if not self.conditions:
            raise ValueError("No conditions available to generate ROC points.")

        false_alarm_rates = []
        hit_rates = []

        for sdt, _ in self.conditions:
            false_alarm_rates.append(sdt.false_alarm_rate())
            hit_rates.append(sdt.hit_rate())

        #Sorts both lists based on false alarm rates
        sorted_indices = np.argsort(false_alarm_rates)
        false_alarm_rates = [false_alarm_rates[i] for i in sorted_indices]
        hit_rates = [hit_rates[i] for i in sorted_indices]

        print("False alarm rates:", false_alarm_rates)
        print("Hit rates:", hit_rates)
        
        return false_alarm_rates, hit_rates


    def compute_auc(self) -> float:
        #Computes the Area Under the Curve (AUC) using the Trapezoidal Rule
        if not self.conditions:
            raise ValueError("No conditions available to compute AUC.")

        false_alarm_rates, hit_rates = self.sorted_roc_points()
        
        return np.trapezoid(hit_rates, false_alarm_rates) #Found Trapezoid function on ChatGBT while searching for simpler ways to apply the Trapezoidal Rule

    def plot_roc_curve(self, show_plot: bool = True) -> None:
        #Plots the ROC curve using matplotlib
        false_alarm_rates, hit_rates = self.sorted_roc_points()

        plt.figure(figsize=(6, 6))
        plt.plot(false_alarm_rates, hit_rates, marker='o', linestyle='-', label='ROC Curve')
        plt.plot([0, 1], [0, 1], 'k--', label='Random Guess')
        plt.xlabel("False Alarm Rate")
        plt.ylabel("Hit Rate")
        plt.title("ROC Curve")
        plt.legend()
        plt.grid(True)

        if show_plot:
            plt.show()