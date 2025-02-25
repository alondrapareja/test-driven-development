import unittest
import numpy as np
import matplotlib.pyplot as plt
from SignalDetection import SignalDetection 
from Experiment import Experiment 

class TestExperiment(unittest.TestCase):
    def test_add_condition(self):
        exp = Experiment()
        sdt = SignalDetection(40,10,20,30)
        exp.add_condition(sdt,"Condition A")

        self.assertEqual(len(exp.conditions),1) #Check to see if the condition was added
        self.assertEqual(exp.labels[0],"Condition A")

    def test_sorted_roc_points(self):
        exp = Experiment ()
        sdt1 = SignalDetection(40,10,20,30)
        sdt2 = SignalDetection(50,5,15,45)
        exp.add_condition(sdt1, "Condition A")
        exp.add_condition(sdt2,"Condition B")
        falseAlarm_rates,hitRates = exp.sorted_roc_points()

        expected_falseAlarm_rates = [0.25,0.40] #replace these with expected values
        expected_hitRates = [0.909,0.8] #replace these with expected values

        self.assertAlmostEqual(falseAlarm_rates, expected_falseAlarm_rates) #checking to see if sorted and matching
        self.assertAlmostEqual(hitRates[0], expected_hitRates[0], places = 6) #checking to see if sorted and matching

    #Test case where AUC should be 0.5 if there are 2 experiments that fall at (0,0) and (1,1)
    def test_compute_auc_case_1(self):
        exp = Experiment()
        sdt1 = SignalDetection(0,0,0,0)
        sdt2 = SignalDetection(10,10,10,10)
        exp.add_condition(sdt1, "Condition A")
        exp.add_condition(sdt2, "Condition B")
        
        #Calculate expected AUC
        expected_auc = 0.5 
        auc_score = exp.compute_auc() 

        #Compare calculated and obtained AUC
        self.assertAlmostEqual(auc_score, expected_auc, places = 6)
    
    #Test case where AUC should be 1.0 if there are 3 experiments that fall at (0,0) (0,1) and (1,1)
    def test_compute_auc_case_2(self):
        exp = Experiment()
        sdt1 = SignalDetection(0,0,0,0)
        sdt2 = SignalDetection(5,10,5,0)
        sdt3 = SignalDetection(10,10,10,10)
        exp.add_condition(sdt1, "Condition A")
        exp.add_condition(sdt2, "Condition B")
        exp.add_condition(sdt3, "Condition C")

        #Calculate expected AUC
        expected_auc = 1.0 
        auc_score = exp.compute_auc() 

        #Compare calculated and obtained AUC
        self.assertAlmostEqual(auc_score, expected_auc, places = 6)

    #Test edge case: AUC, no condition
    def test_empty_exp_auc(self):
        exp = Experiment()
        with self.assertRaises(ValueError): #Raises error due to no condition
            exp.compute_auc()

    #Test edge case: sorted_roc_points, no condition
    def test_empty_exp_sorted_roc_points(self):
        exp = Experiment()
        with self.assertRaises(ValueError): #Raises error due to no condition
            exp.sorted_roc_points()

    #Test edge case: AUC, single condition
    def test_single_con_auc(self):
        exp = Experiment()
        sdt1 = SignalDetection (10,5,15,10)
        exp.add_condition(sdt1, "Condition A")
        with self.assertRaises(ValueError): #Raises error due to single condition 
            exp.compute_auc()

    #Test identical conditions for hit rate and false alarms rate
    def test_sorted_roc_points_iden(self):
        exp = Experiment()
        sdt1 = SignalDetection(20,10,20,10)
        sdt2 = SignalDetection(20,10,20,10)
        exp.add_condition(sdt1, "Condition A")
        exp.add_condition(sdt2, "Condition B")

        falseAlarm_rates,hitRates = exp.sorted_roc_points()

        expected_falseAlarm_rates = [0.5,0.5] 
        expected_hitRates = [0.5,0.5] 

        #Check that both conditions result in the same ROC points
        self.assertEqual(falseAlarm_rates, expected_falseAlarm_rates)
        self.assertEqual(hitRates, expected_hitRates) 

    def test_plot_roc_curve(self):
        exp = Experiment()
        sdt1 = SignalDetection(40,10,20,30)
        sdt2 = SignalDetection(50,5,15,45)
        exp.add_condition(sdt1, "Condition A")
        exp.add_condition(sdt2, "Condition B")

        exp.plot_roc_curve

if __name__ == '__main__':
    unittest.main()