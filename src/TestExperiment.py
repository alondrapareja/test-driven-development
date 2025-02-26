import unittest
from Experiment import Experiment
from SignalDetection import SignalDetection

class TestExperiment(unittest.TestCase):

    def test_add_condition(self):
        #Test that adding a condition works correctly
        exp = Experiment()
        sdt = SignalDetection(40, 10, 20, 30)
        exp.add_condition(sdt, label="Condition A")
        self.assertEqual(len(exp.conditions), 1, "Condition was not added correct")

    def test_add_multiple_conditions(self):
        #Test adding multiple conditions
        exp = Experiment()
        sdt_1 = SignalDetection(40, 10, 20, 30)
        sdt_2 = SignalDetection(30, 20, 10, 40)
        exp.add_condition(sdt_1, label="Condition A")
        exp.add_condition(sdt_2, label="Condition B")
        self.assertEqual(len(exp.conditions), 2, "Multiple conditions were not added correct")

    def test_sorted_roc_points(self):
        #Tests that ROC points are sorted correctly
        exp = Experiment()
        exp.add_condition(SignalDetection(40, 10, 20, 30), "A")
        exp.add_condition(SignalDetection(30, 20, 10, 40), "B")

        false_alarm_rates, hit_rates = exp.sorted_roc_points()

        #Ensures that false alarm rates are sorted in increasing order
        self.assertTrue(all(false_alarm_rates[i] <= false_alarm_rates[i + 1] for i in range(len(false_alarm_rates) - 1)),
                        "False alarm rates are not sorted correct")

    def test_compute_auc(self):
       #Testes that compute_auc() produces the expected values for known cases
        exp = Experiment()
        exp.add_condition(SignalDetection(1, 0, 0, 1), "A")  #(0,0)
        exp.add_condition(SignalDetection(1, 1, 0, 0), "B")  #(1,1)

        auc = exp.compute_auc()
        self.assertAlmostEqual(auc, 0.0, places=2, msg="AUC value is incorrect for (0,0) and (1,1) cases")

    def test_compute_auc_perfect(self):
        #Tests that compute_auc() produces expected values for perfect conditions
        exp = Experiment()
        exp.add_condition(SignalDetection(1, 0, 1, 0), "A")  #(0,0)
        exp.add_condition(SignalDetection(1, 1, 0, 0), "B")  #(0,1)

        auc = exp.compute_auc()
        self.assertAlmostEqual(auc, 0.75, places=2, msg="AUC value is incorrect for perfect conditions.")

    def test_empty_experiment_raises_error(self):
        #Tests if errors are raised when no conditions are added 
        exp = Experiment()
        with self.assertRaises(ValueError, msg="Empty experiment did not raise ValueError for sorted_roc_points"):
            exp.sorted_roc_points()
        
        with self.assertRaises(ValueError, msg="Empty experiment did not raise ValueError for compute_auc"):
            exp.compute_auc()

if __name__ == "__main__":
    unittest.main()

