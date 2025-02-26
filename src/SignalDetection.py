class SignalDetection:
   def __init__(self, hits, misses, false_alarms, correct_rejections):
       if any(x < 0 for x in [hits, misses, false_alarms, correct_rejections]):
           raise ValueError("Counts cannot be negative")
       self.hits = hits
       self.misses = misses
       self.false_alarms = false_alarms
       self.correct_rejections = correct_rejections

   def hit_rate(self) -> float:
       #Calculates the hit rate
       if self.hits + self.misses == 0:
           return 0.0
       return self.hits / (self.hits + self.misses)


   def false_alarm_rate(self) -> float:
       #Calculates the false alarm rate
       if self.false_alarms + self.correct_rejections == 0:
           return 0.0
       return self.false_alarms / (self.false_alarms + self.correct_rejections)
