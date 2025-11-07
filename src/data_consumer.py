import time
import argparse


def process_log(log_line):
    # Process or handle each line of the log file
    print(f"Processing log: {log_line}")


def consume_logs(log_file_path):
    # Open the log file in read mode
    with open(log_file_path, "r") as log_file:
        # Move the read position to the end of the file ready for new lines
        log_file.seek(0, 2)
        while True:
            # Read a new line from the current position
            line = log_file.readline()
            if not line:
                # If no new line is read, wait and retry
                time.sleep(0.1)
                continue
            # Process any new line that is read
            process_log(line)


if __name__ == "__main__":
    # Set up command-line input with argpaser
    parser = argparse.ArgumentParser(description="Consume logs from a specified file.")
    # Argument for the log file path
    parser.add_argument(
        "log_file_path", type=str, help="Path to the log file to be consumed."
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    # Call the function to start consuming logs
    consume_logs(args.log_file_path)
