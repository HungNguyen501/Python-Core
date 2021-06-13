import my_program

def test_doc_string():
    """This is test for doc string
    """
    pass

test_doc_string()

# get name from my_program module
my_program.get_name()
# print name of file
print(__name__)

"""
Result is below:
my_program
__main__
"""