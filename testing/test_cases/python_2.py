#
#
# Python Test File 2 (Random)
#
#
# Author: Tejas. P. Herle


def main(argc: int, argv: 'str list') -> None:
    # Prints 2 variables
    # ie. argc a
    print(argc, argv)

    # Prints 'Hello World'
    print('Hello World')
    for i in range(10):  # This is a for loop
        print(i)

        while i != 10:
            print('Steps to 10: ', i)  # Saturating stdout with rubbish
            if i == 5:
                print('Midway')  # Just an other half more
            i += 1  # Just one up?

        while i < 100:
            if i == 50:
                print('Midway through 100')  # Done Through the tedious job

            # Skip 5, cool
            i += 5  # Speeding up the process

        # At last I can take a breath
        # And get ready for the next round :(
        print('Out of mess')  # Done with that 100

    print('At last done!')  # Difficult to repeat that long thing 10 times


def sec_func() -> str:
    # Random func
    # Not necessary
    x = None
    y = None

    # Ahh wasting lines
    z = None  # Mess with this in line comment

    return_val = 'This is my return value'

    return return_val


code = 'rand'
code += 'code'
code += 'level 1'


if __name__ == '__main__':
    main(2, 'abc')
