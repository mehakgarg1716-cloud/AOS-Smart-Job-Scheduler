
class SmartScheduler:

    def __init__(self, jobs):
        self.jobs = jobs
        self.execution_order = []

    # Calculate smart score for each job
    def calculate_score(self, job, current_time):

        # Priority score (lower priority number = higher preference)
        priority_score = 1 / job.priority

        # Deadline urgency
        remaining_time = max(1, job.deadline - current_time)
        deadline_score = 1 / remaining_time

        # Short burst time gets higher preference
        burst_score = 1 / job.burst_time

        # Final weighted score
        score = (
            0.40 * priority_score +
            0.35 * deadline_score +
            0.25 * burst_score
        )

        return score

    # Execute smart scheduling
    def schedule_jobs(self):

        pending_jobs = self.jobs.copy()
        current_time = 0

        self.execution_order = []

        while pending_jobs:

            # Select jobs that have arrived
            available_jobs = [
                job for job in pending_jobs
                if job.arrival_time <= current_time
            ]

            # If no job is available, move to next arrival
            if not available_jobs:

                current_time = min(
                    job.arrival_time for job in pending_jobs
                )

                continue

            # Find job with highest smart score
            selected_job = max(
                available_jobs,
                key=lambda job: self.calculate_score(
                    job, current_time
                )
            )

            # Store execution details
            selected_job.start_time = current_time

            selected_job.completion_time = (
                current_time + selected_job.burst_time
            )

            # Calculate performance metrics
            selected_job.calculate_times()

            # Store execution order
            self.execution_order.append(selected_job)

            # Update CPU time
            current_time = selected_job.completion_time

            # Remove completed job
            pending_jobs.remove(selected_job)

        return self.execution_order
