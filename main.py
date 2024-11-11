import my_select

if __name__ == '__main__':
    for i in range(1, 11):
        print(getattr(my_select, f"select_{i}")())


