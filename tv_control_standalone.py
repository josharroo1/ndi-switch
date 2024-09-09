from tv_control import TVController
import argparse

def main():
    parser = argparse.ArgumentParser(description="Control TVs via RS232")
    parser.add_argument("action", choices=["on", "off"], help="Turn TVs on or off")
    parser.add_argument("--tv", help="Specific TV to control (e.g., tv1, tv2)")
    args = parser.parse_args()

    controller = TVController()

    if args.tv:
        if args.action == "on":
            controller.turn_on_tv(args.tv)
        else:
            controller.turn_off_tv(args.tv)
    else:
        if args.action == "on":
            controller.turn_on_all_tvs()
        else:
            controller.turn_off_all_tvs()

if __name__ == "__main__":
    main()