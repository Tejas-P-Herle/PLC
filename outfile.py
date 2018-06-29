class Outfile:
    def main(self: "Outfile") -> 'None':
        i = 0
        j = 50.009
        i_j = 10
        i_j += 100
        print(i_j)
        print(j)
        print("Hello World")
        print("2nd print of 'Hello World'")
        for z in range(10, 0, -1):
            print(z)
        
        if i == 0:
            print(0)
        
        for q in range(10):
            print(10 + q)
        
        if i == 1:
            print(10)
            print(20)
            print(30)
        
        print("Hello")


if __name__ == "__main__":
    Outfile().main()


