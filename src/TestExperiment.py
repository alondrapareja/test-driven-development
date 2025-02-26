import unittest
from Experiment import Experiment
from SignalDetection import SignalDetection

class TestExperiment(unittest.TestCase):
    def test_add_condition(self):
        exp = Experiment()
        sdt = SignalDetection(40, 10, 20, 30)
        exp.add_condition(sdt, label="Condition A")
        self.assertEqual(len(exp.conditions), 1)

    def test_sorted_roc_points(self):
        exp = Experiment()
        exp.add_condition(SignalDetection(40, 10, 20, 30), "A")
        exp.add_condition(SignalDetection(30, 20, 10, 40), "B")

        false_alarm_rates, hit_rates = exp.sorted_roc_points()
        self.assertTrue(all(false_alarm_rates[i] <= false_alarm_rates[i+1] for i in range(len(false_alarm_rates)-1)))

    def test_compute_auc(self):
        exp = Experiment()
        exp.add_condition(SignalDetection(1, 0, 0, 1), "A")  # (0,0)
        exp.add_condition(SignalDetection(1, 1, 0, 0), "B")  # (1,1)

        auc = exp.compute_auc()
        self.assertAlmostEqual(auc, 0.0, places=2)

    def test_compute_auc_perfect(self):
        exp = Experiment()
        exp.add_condition(SignalDetection(1, 0, 1, 0), "A")  # (0,0)
        exp.add_condition(SignalDetection(1, 1, 0, 0), "B")  # (0,1)


        auc = exp.compute_auc()
        self.assertAlmostEqual(auc, 0.75, places=2)

    def test_empty_experiment_raises_error(self):
        exp = Experiment()
        with self.assertRaises(ValueError):
            exp.sorted_roc_points()
        with self.assertRaises(ValueError):
            exp.compute_auc()

if __name__ == "__main__":
    unittest.main()