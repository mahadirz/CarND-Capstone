import rospy


class Project(object):

    def __init__(self):
        self.last_log = {}
        self.counter = {}
        self.last_counter_allowed = {}
        # log rate, 1 means about 1 log per second
        self.log_rate = 1

    def log_count(self, namespace='main'):
        if namespace not in self.counter:
            self.counter[namespace] = 0
        else:
            self.counter[namespace] += 1

    def get_count(self, namespace='main'):
        if namespace not in self.counter:
            self.counter[namespace] = 0
        return self.counter[namespace]

    def set_last_counter(self, counter, namespace='main'):
        self.last_counter_allowed[namespace] = counter

    def get_last_counter(self, namespace='main'):
        if namespace not in self.last_counter_allowed:
            self.last_counter_allowed[namespace] = 0
        return self.last_counter_allowed[namespace]

    def set_last_log(self, namespace='main'):
        self.last_log[namespace] = rospy.get_time()

    def get_last_log(self, namespace='main'):
        if namespace not in self.last_log:
            self.last_log[namespace] = rospy.get_time()
        return self.last_log[namespace]

    def log(self, msg, namespace='main'):
        now = rospy.get_time()
        # The diff is in second
        if (now - self.get_last_log(namespace)) > self.log_rate or \
                self.get_last_counter(namespace) == self.get_count(namespace):
            rospy.logwarn(msg)
            self.set_last_counter(self.get_last_counter(namespace), namespace)
            self.set_last_log(namespace)
