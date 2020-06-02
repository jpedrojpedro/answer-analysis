from pathlib import Path


def enumerate_available_datasets():
    folder = Path('./questions')
    files = list(folder.glob('*.json'))
    datasets = {idx: str(file)[10:-5] for idx, file in enumerate(files, start=1)}
    for idx, dataset in datasets.items():
        print("{} - {}".format(idx, dataset))
    return datasets


def start():
    print('Welcome to Answer Analysis program!')
    print('Which dataset do you wish to interact with?')
    datasets = enumerate_available_datasets()
    number = input('>\t')
    # TODO: handle possible exception
    number = int(number)
    # TODO: handle possible exception
    print(datasets[number])
