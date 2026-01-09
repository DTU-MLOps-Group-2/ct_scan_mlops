from ct_scan_mlops.data import MyDataset
from ct_scan_mlops.model import Model


def train():
    _dataset = MyDataset("data/raw")
    _model = Model()
    # add rest of your training code here


if __name__ == "__main__":
    train()
