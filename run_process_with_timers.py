# implement a process that runs for a certain amount of time, and then stops

import random
import time
import multiprocessing
import os
import subprocess

def run_os_command(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = popen.communicate()
    returncode = popen.returncode
    print(f"stdout: {stdout}")
    return stdout, stderr, returncode

def main(timeout, grace_time, minimum_proc_time):
    """Implement a kill control that will kill the process after the timeout,
    but give the process a grace time to finish gracefully before killing it.
    """
    #start a timer process
    start_time = time.time()
    print(f"Start time: {start_time}")

    for i in range(10):
        # generate a random time to run the process
        random_time = random.randint(8, 15)
        #start the process to run
        print(f"Starting process {i} with random time {random_time} at {time.time()-start_time:.1f} seconds")
        process = multiprocessing.Process(
            target=run_os_command, 
            args=(['/bin/bash', './os_script.sh',str(i), str(random_time)],)  # Explicitly use bash to run the script
        )
        process.start()
    
        # Wait for the timeout period
        already_elapsed = time.time() - start_time
        remaining_time = timeout - already_elapsed - grace_time
        if remaining_time > 0: # is there enought time for another run?
            process.join(remaining_time)
            elapsed_time = time.time() - start_time
            print(f"Remaining time: {remaining_time:.1f} vs {elapsed_time:.1f}")
            if process.is_alive():
                print(f"elapsed time {elapsed_time:.1f} exceeded timeout of {timeout}-{grace_time} seconds. Killing process and proceeding with clean up...")
                process.terminate()
                process.join()
                break
        else:
            print(f"Remaining time is zero, ending")
            if process.is_alive():
                process.terminate()
                process.join()
            break
        elapsed_time = time.time() - start_time
        remaining_time = timeout - elapsed_time
        if remaining_time < grace_time + minimum_proc_time:
            print(f"Not enough time for another run, ending: {remaining_time:.1f} < {grace_time} + {minimum_proc_time}")
            break
        else:
            print(f"Launching another run {remaining_time:.1f} > {grace_time} + {minimum_proc_time}")

if __name__ == "__main__":
    timeout = 30  # 5 seconds timeout
    grace_time = 5  # 2 seconds grace period
    minimum_proc_time = 5 # minimum time expected for the process to run
    main(timeout, grace_time, minimum_proc_time)

