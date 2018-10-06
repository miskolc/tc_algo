import logging
import options as op

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    result = op.euro_vanilla(10485, 10800, 20, 0.01, 18.54, option='call')
    print(result)
