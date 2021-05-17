from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import declarative_base

if __name__ == '__main__':
    filepath = 'train.csv'
    with open(filepath, 'r') as f:
        # get the head column name
        line = f.readline().strip()
        heads = line.split(',')
        print(heads)
        # break

    #     data = []
    #     for line in f:
    #         data.append(line.strip().split(','))
    #
    #
    # engine = create_engine('mysql+pymysql:', echo=True)
    #
    Base = declarative_base()

    class HousePrice(Base):
        __tablename__ = 'house_price'


        id = Column(Integer, primary_key=True)
        MSSubClass = Column(String, name='ms_sub_class')
        MSZoning = Column(String, name='ms_zoning')
        LotFrontage = Column(String, name='lot_frontage')

    session = 