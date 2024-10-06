import argparse

def parse_arguments():
    """
    Parse command line arguments.
    
    :return: Command line argument object.
    """
    parser = argparse.ArgumentParser(description='Twitch Clips Downloader')
    parser.add_argument('-i', '--input', required=True, help='Text file containing clip links and names')
    parser.add_argument('-o', '--output', required=True, help='Directory to save downloaded files')
    parser.add_argument('-t', '--threads', type=int, default=5, help='Number of parallel download threads')
    
    return parser.parse_args()
