def create_files():
    input_file = "phishtank_samples.txt"
    part_files = [
        "phishtank_part1.txt",
        "phishtank_part2.txt",
        "phishtank_part3.txt",
        "phishtank_part4.txt",
        "phishtank_part5.txt"
    ]

    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()

        # Define line ranges for each part
        ranges = [
            (0, 10),   # First 10 lines
            (10, 20),  # Next 10 lines
            (20, 30),  # Next 10 lines
            (30, 40),  # Next 10 lines
            (40, 50)   # Next 10 lines
        ]

        # Creating each part file with the specified lines
        for i, (start, end) in enumerate(ranges):
            with open(part_files[i], 'w') as part_file:
                part_file.writelines(lines[start:end])

        print(f"Files {', '.join(part_files)} created successfully.")
        
    except FileNotFoundError:
        print(f"The file '{input_file}' does not exist in the current directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_files()

