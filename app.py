# Required imports

from scripts.prediction import predict

if __name__ == "__main__":

    print(predict("Contractor Informs Biden It’d Be Cheaper To Just Tear Down U.S. And Start Over",
                  premium=True))