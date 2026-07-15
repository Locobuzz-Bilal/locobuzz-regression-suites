import time
import allure

def allure_step(step_name: str):
    """
    Custom Allure step wrapper that tracks and logs step duration.
    Usage:
        with allure_step("Login to Locobuzz"):
            # perform your step
    """
    class StepTimer:
        def __enter__(self):
            self.start_time = time.time()
            self.step_name = step_name
            self.ctx = allure.step(step_name)
            self.ctx.__enter__()
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            end_time = time.time()
            duration = round(end_time - self.start_time, 2)
            message = f"⏱ Step '{self.step_name}' took {duration} seconds"
            
            # Log in terminal
            print(message)

            # Attach duration info in Allure report
            allure.attach(message, name=f"{self.step_name} Duration", attachment_type=allure.attachment_type.TEXT)

            # Exit Allure context
            self.ctx.__exit__(exc_type, exc_val, exc_tb)

    return StepTimer()
