import random

#
# def create_csv(csv_filename):
#     with open(csv_filename,'wt')as f:
#         f.write()

def process_csv(csv_filename):
    with open(csv_filename,'rt') as f:
        content=tuple(f)
    header, *data=content

    data=list(data)
    random.shuffle(data)

    data_num=len(data)
    train_num=int(0.5*data_num)

    train_data=data[:train_num]
    test_data=data[train_num:]

    with open('train.csv','wt')as f:
        f.write(header)
        f.writelines(train_data)

    with open('test.csv','wt')as f:
        f.write(header)
        f.writelines(test_data)

def main():
    # create_csv('Menu-csv.csv')
    process_csv('Menu-csv.csv')


if __name__=='__main__':
    main()
