import Tom_Tom_API
import Transform


def main():
    Tom_Tom_API.Run_Extraction()
    Transform.process_raw_data()


if __name__ == "__main__":
    main()
