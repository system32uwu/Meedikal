import os, sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import Config

p = os.path.join(os.path.dirname(__file__))
from models.User import User, Administrative

if __name__ == '__main__':
    User.save(Config.Admin) # save base user
    Administrative.save({'ci': Config.Admin['ci']}) # give role to user