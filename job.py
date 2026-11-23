
class Job:
    def __init__(self, job_id, arrival_time, burst_time, priority, deadline):

        self.job_id = job_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.deadline = deadline

        # Execution details
        self.start_time = 0
        self.completion_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = 0

        self.deadline_status = "Pending"

    def calculate_times(self):

        self.turnaround_time = (
            self.completion_time - self.arrival_time
        )

        self.waiting_time = (
            self.turnaround_time - self.burst_time
        )

        self.response_time = (
            self.start_time - self.arrival_time
        )

        if self.completion_time <= self.deadline:
            self.deadline_status = "Completed"
        else:
            self.deadline_status = "Missed"
