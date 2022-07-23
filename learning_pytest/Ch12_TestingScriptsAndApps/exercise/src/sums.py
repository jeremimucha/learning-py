# sums.py
# add the numbers in 'data.txt'


def main():
    sum = 0.0
    with open("data.txt", "r") as file:
        for line in file:
            sum += float(line)
    print(f"{sum:.2f}")


if __name__ == "__main__":
    main()
