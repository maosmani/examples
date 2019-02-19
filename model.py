
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///test.db')
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    pages = Column(Integer)
    
    
    def __repr__(self):
        return "<Book(title='{}', author='{}', pages={})>"\
                .format(self.title, self.author, self.pages)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
s = Session()
book = Book(
    title='Deep Learning',
    author='Ian Goodfellow',
    pages=775,
    
)
s.add(book)
s.add(book)
s.add(book)
s.commit()
print(s.query(Book).all())
print(s.query(Book).first())
print("____________________________________________________________")

# filtering basics where 
r = s.query(Book).filter_by(title='Deep Learning').first()

print("filter_by:", r)

r = s.query(Book).filter(Book.title=='Deep Learning').first()

print("filter:", r)

#ignor uper and lower case

x = s.query(Book).filter(Book.title.ilike('deep learning')).first()   
print(x)

# between tow ranges
s.query(Book).filter(Book.published.between(start_date, end_date)).all()

#Let's say we want all books that are over 750 pages and published after 2016 
#Here's how we would do that:
from sqlalchemy import and_

s.query(Book).filter(
    and_(
       Book.pages > 750,
       Book.published > datetime(2016, 1, 1)
    )
).all()

#Now let's say we want any books that were published either before 2010 
#or after 2016:
from sqlalchemy import or_

s.query(Book).filter(
    or_(
        Book.published < datetime(2010, 1, 1),
        Book.published > datetime(2016, 1, 1)
    )
).all()
print("""
Let's say we want to return a result that matches following criteria

    books either less than 500 pages or greater than 750 pages long
    books published between 2013 and 2017
    ordered by the number of pages
    limit it to one result

Here's what we're looking at:
""")
s.query(Book).filter(
    and_(
        or_(
            Book.pages < 500,
            Book.pages > 750
        ),
        Book.published.between(datetime(2013, 1, 1), datetime(2017, 1, 1))
    )
)\
.order_by(Book.pages.desc())\
.limit(1)\
.first()

s.close_all()   
