import front_end as fe
import Davis_Putnam as dp

if __name__ == "__main__":
    fe.main("FrontEndInput.txt", "FrontEndOutput.txt")
    dp.main("FrontEndOutput.txt", "BackEndInput.txt")
