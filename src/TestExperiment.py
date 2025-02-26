import unittest
from Experiment import Experiment
from SignalDetection import SignalDetection

class TestExperiment(unittest.TestCase):

    def test_add_condition(self):
        #Tests that add_condition correctly stores SignalDetection objects and labels
        exp = Experiment()
        sdt = SignalDetection(40, 10, 20, 30)
        exp.add_condition(sdt, label="Condition A")
        
        self.assertEqual(len(exp.conditions), 1, "Condition was not added correctly")
        self.assertEqual(exp.conditions[0][1], "Condition A", "Condition label was not stored correctly")
        self.assertIs(exp.conditions[0][0], sdt, "SignalDetection object was not stored correctly")

    def test_add_multiple_conditions(self):
        #Tests adding multiple conditions
        exp = Experiment()
        sdt_1 = SignalDetection(40, 10, 20, 30)
        sdt_2 = SignalDetection(30, 20, 10, 40)
        exp.add_condition(sdt_1, label="Condition A")
        exp.add_condition(sdt_2, label="Condition B")

        self.assertEqual(len(exp.conditions), 2, "Multiple conditions were not added correctly")
        self.assertEqual(exp.conditions[1][1], "Condition B", "Second condition label is incorrect")

    def test_sorted_roc_points(self):
        #Tests that sorted_roc_points correctly sorts by false alarm rates
        exp = Experiment()
        exp.add_condition(SignalDetection(40, 10, 20, 30), "A")  
        exp.add_condition(SignalDetection(30, 20, 10, 40), "B") 

        false_alarm_rates, hit_rates = exp.sorted_roc_points()

        #Ensures false alarm rates are sorted in an increasing order
        self.assertTrue(all(false_alarm_rates[i] <= false_alarm_rates[i + 1] for i in range(len(false_alarm_rates) - 1)),
                        "False alarm rates are not sorted correctly")

    def test_compute_auc_half(self):
        #Tests that compute_auc produces AUC = 0.5 for known test case (0,0) and (1,1)
        exp = Experiment()
        exp.add_condition(SignalDetection(1, 0, 0, 1), "A")  #0,0)
        exp.add_condition(SignalDetection(1, 1, 0, 0), "B")  #(1,1)

        auc = exp.compute_auc()
        self.assertAlmostEqual(auc, 0.5, places=2, msg="AUC value is incorrect for (0,0) and (1,1) case")

    def test_compute_auc_perfect(self):
        #Tests that compute_auc produces AUC = 1 for a perfect ROC curve
        exp = Experiment()
        exp.add_condition(SignalDetection(1, 0, 1, 0), "A")  #(0,0)
        exp.add_condition(SignalDetection(0, 1, 1, 0), "B")  #(0,1)
        exp.add_condition(SignalDetection(1, 0, 0, 1), "C")  #(1,1)

        auc = exp.compute_auc()
        self.assertAlmostEqual(auc, 1.0, places=2, msg="AUC value is incorrect for a perfect ROC case")

    def test_compute_auc_increasing(self):
        #Tests that compute_auc produces correct AUC for an increasing ROC curve
        exp = Experiment()
        exp.add_condition(SignalDetection(1, 0, 0, 1), "A")  #(0,0)
        exp.add_condition(SignalDetection(1, 1, 1, 0), "B")  #0.5, 0.5)
        exp.add_condition(SignalDetection(1, 1, 0, 0), "C")  #(1,1)

        auc = exp.compute_auc()
        self.assertGreater(auc, 0.5, "AUC value should be greater than 0.5 for an increasing ROC case")

    def test_empty_experiment_raises_error(self):
        #Tests that calling sorted_roc_points or compute_auc on an empty experiment raises ValueError
        exp = Experiment()
        with self.assertRaises(ValueError, msg="Empty experiment did not raise ValueError for sorted_roc_points"):
            exp.sorted_roc_points()
        
        with self.assertRaises(ValueError, msg="Empty experiment did not raise ValueError for compute_auc"):
            exp.compute_auc()

    def test_invalid_signal_detection(self):
        #Tests handling of invalid SignalDetection values (negative counts)
        exp = Experiment()
        with self.assertRaises(ValueError, msg="Negative counts should raise ValueError"):
            exp.add_condition(SignalDetection(-1, 10, 5, 10), "Invalid")

if __name__ == "__main__":
    unittest.main()
