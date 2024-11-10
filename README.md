# py_sample_timer_kill
This sample project is to PoC an OS command runner that can launch multiple commands
But at some given timeout period it needs to shutdown any running process and use a grace time to
perform cleanup and closing activities.

General goals are:

# Record the time at the beginning of execution.
# Start processes, and watch the time if it is > timeout - grace then kill the process
# if process completes, then check if there is still time left to launch another process.

