import glob
import shutil
import os

def read_quarantine_files(quarantine_dir):
    # Use glob to get all files in the quarantine directory
    quarantine_files = glob.glob(quarantine_dir + "/*")

    if not quarantine_files:
        print("No quarantined files found.")
    else:
        for file_path in quarantine_files:
            # Copy the file to destination directory
            try:
                file_name = os.path.basename(file_path)
                dest_path = os.path.join(os.path.dirname(__file__), file_name)
                shutil.copy(file_path, dest_path)
                print("File copied successfully:", file_name)
            except Exception as e:
                print("Error copying file:", str(e))

def read_detection_logs(log_dir):
    # Use glob to get all JSON files in the directory
    json_files = glob.glob(log_dir + "/*.json")

    # Loop through each JSON file
    for json_file in json_files:
        with open(json_file, 'r') as file:
            # Read the contents of the file
            data = file.read()

            # Find all occurrences of 'objectPath'
            start_index = data.find('"objectPath": "')
            while start_index != -1:
                start_index += len('"objectPath": "')
                end_index = data.find('"', start_index)
                if end_index != -1:
                    object_path = data[start_index:end_index]
                    # Print the object path
                    print("Object Path:", object_path)

                    # Copy the file to destination directory
                    try:
                        source_path = os.path.join(log_dir, object_path)
                        dest_path = os.path.join(os.path.dirname(__file__), os.path.basename(object_path))
                        shutil.copy(source_path, dest_path)
                        print("File copied successfully.")
                    except Exception as e:
                        print("Error copying file:", str(e))
                else:
                    print("End of objectPath not found in", json_file)
                # Search for the next occurrence of 'objectPath'
                start_index = data.find('"objectPath": "', end_index)

            # If no occurrences of 'objectPath' were found
            if start_index == -1:
                print("Object Path not found in", json_file)


def main():
    print("Welcome to aceypep.")
    print("Type 'help' for a list of commands.")

    while True:
        user_input = input("> ").strip().lower()

        if user_input.startswith('extract'):
            args = user_input.split()
            if len(args) == 1:
                drive = input("Enter drive letter: ").strip().upper()
            elif len(args) == 2 and args[1] == '-q':
                drive = input("Enter drive letter: ").strip().upper()
            elif len(args) == 2:
                drive = args[1].strip().upper()
            else:
                print("Invalid command.")
                continue

            # Check if the drive exists
            if not os.path.exists(f"{drive}:\\"):
                print("Error: The specified drive does not exist.")
                continue

            log_directory = f"{drive}:\\ProgramData\\Malwarebytes\\MBAMService\\ScanResults"
            quarantine_directory = f"{drive}:\\ProgramData\\Malwarebytes\\MBAMService\\Quarantine"

            if len(args) == 2 and args[1] == '-q':
                read_quarantine_files(quarantine_directory)
            else:
                read_detection_logs(log_directory)
            print("Extraction completed!")
        elif user_input == 'help':
            print("Type 'extract' to extract files from detection logs.")
            print("Type 'extract -q' to check for quarantined files in Malwarebytes.")
            print("Type 'exit' to exit the program.")

            print("\nThis version of aceypep is for Windows and Linux systems only.")
            print("This version of aceypep is meant for reading Malwarebytes logs in order to extract")
            print("malware detected by the antivirus for later analysis.")
        elif user_input == 'exit':
            print("Exiting program.")
            break
        else:
            print(
                "Invalid command. Type 'extract' to begin extraction, 'extract -q' to check for quarantined files, or 'exit' to quit.")

if __name__ == "__main__":
    main()
