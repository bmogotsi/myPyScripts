# https://www.geeksforgeeks.org/python/detect-encoding-of-a-text-file-with-python/
# https://www.geeksforgeeks.org/python/detect-encoding-of-a-text-file-with-python/ or csv file
import chardet

def detect_encoding(file_path):

    # Open the file in binary mode ('rb') to read raw bytes
    with open(file_path, 'rb') as f:
        # Read the entire file, or a large sample, for analysis
        raw_data = f.read()

    # Use chardet to detect the encoding
    result = chardet.detect(raw_data)

    # The result is a dictionary with 'encoding', 'confidence', and 'language'
    return result

# Example usage:
file_path = 'your_file.txt' # Replace with your file's path
encoding_info = detect_encoding(file_path)

print(f"Detected encoding: {encoding_info['encoding']}")
print(f"Confidence: {encoding_info['confidence']}")
print(f"Language: {encoding_info['language']}")

# You can then use the detected encoding to open and read the file correctly
try:
    with open(file_path, 'r', encoding=encoding_info['encoding']) as f:
        content = f.read()
        print("\nFile successfully read with detected encoding.")
except UnicodeDecodeError:
    print("\nFailed to decode with the detected encoding. The guess might be incorrect.")
