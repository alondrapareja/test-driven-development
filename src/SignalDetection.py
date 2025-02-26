class SignalDetection:
    def __init__(self, hits, misses, false_alarms, correct_rejections):
        #Initialize with counts of hits, misses, false alarms, and correct rejections.
        self.hits = hits
        self.misses = misses
        self.false_alarms = false_alarms
        self.correct_rejections = correct_rejections

    def hit_rate(self) -> float:
        #Calculate the hit rate as hits / (hits + misses)
        if self.hits + self.misses == 0:
            return 0.0
        return self.hits / (self.hits + self.misses)

    def false_alarm_rate(self) -> float:
        #Calculate the false alarm rate as false_alarms / (false_alarms + correct_rejections)
        if self.false_alarms + self.correct_rejections == 0:
            return 0.0
        return self.false_alarms / (self.false_alarms + self.correct_rejections)