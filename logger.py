import sys

def redirect_print_to_file(file_path, function_to_run, *args):
    # Open the file for appending or creating if it doesn't exist
    with open(file_path, 'a+') as log_file:
        # Save the original sys.stdout
        original_stdout = sys.stdout
        
        try:
            # Redirect sys.stdout to the log file
            sys.stdout = log_file

            # Call the function whose print statements you want to capture
            function_to_run(*args)
        finally:
            # Restore the original sys.stdout
            sys.stdout = original_stdout