import argparse
from brochure_generation import create_brochure, stream_brochure



def parse_args():
    parser = argparse.ArgumentParser(description="Generate a sales brochure for a website.")
    parser.add_argument("website_url", type=str, help="The URL of the website to scrape.")
    parser.add_argument("--stream", action="store_true", help="Enable streaming mode.")
    return parser.parse_args()

def main():
    args = parse_args()
    print(f"Website URL: {args.website_url}")
    if args.stream:
        brochure = stream_brochure(args.website_url)
    else:
        brochure = create_brochure(args.website_url)
        print("\nGenerated Brochure:\n")
        print(brochure)


if __name__ == "__main__":
    main() 