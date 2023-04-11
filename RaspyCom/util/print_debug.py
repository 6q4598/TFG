"""
    --------------------------------
    Check:
    ------
"""
print("PLC connected.")
read_db = client.db_read(91, 0, 2)

print("DB readed data:\n---------------")
print(convert_byte_to_bit(read_db)[1:-1])
print("DB readed data:\n... ... ... ... ...")

# print(int(convert_byte_to_bit(read_db)[0]), end = "")
# print(convert_byte_to_bit(read_db)[1], end = "")

print(int(convert_byte_to_bit(read_db)[2]), end = "")

print(".", end = "")
print(int(convert_byte_to_bit(read_db)[3]), end = "")
print(int(convert_byte_to_bit(read_db)[4]), end = "")
print(int(convert_byte_to_bit(read_db)[5]), end = "")
print(int(convert_byte_to_bit(read_db)[6]), end = "")

print(".", end = "")
print(int(convert_byte_to_bit(read_db)[7]), end = "")
print(int(convert_byte_to_bit(read_db)[8]), end = "")
print(int(convert_byte_to_bit(read_db)[9]), end = "")
print(int(convert_byte_to_bit(read_db)[10]), end = "")

print(".", end = "")
print(int(convert_byte_to_bit(read_db)[11]), end = "")
print(int(convert_byte_to_bit(read_db)[12]), end = "")
print(int(convert_byte_to_bit(read_db)[13]), end = "")
print(int(convert_byte_to_bit(read_db)[14]), end = "")

print(".", end = "")
print(int(convert_byte_to_bit(read_db)[15]), end = "")
print(int(convert_byte_to_bit(read_db)[16]), end = "")
print(int(convert_byte_to_bit(read_db)[17]), end = "")
print(int(convert_byte_to_bit(read_db)[18]), end = " ------------ \n")
