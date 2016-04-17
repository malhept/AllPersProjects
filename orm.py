from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)

class Address(Base):
     __tablename__ = 'addresses'
     id = Column(Integer, primary_key=True)
     email_address = Column(String, nullable=False)
     er_id = Column(Integer, ForeignKey('users.id'))
     user = relationship("User", back_populates="addresses")

     def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


def afficher_users(sess):
    for instance in sess.query(User).order_by(User.id):
        print(instance.name, instance.fullname, instance.password)

def main():
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

    Session = sessionmaker(bind=engine)
    session = Session()
    ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
    print(ed_user)
    session.add(ed_user)
    session.add_all([User(name='wendy', fullname='Wendy Williams', password='foobar'),
                    User(name='mary', fullname='Mary Contrary', password='xxg527'),
                    User(name='fred', fullname='Fred Flinstone', password='blah')])
    session.commit()
    afficher_users(session)
    our_user = session.query(User).filter_by(name='ed').first()
    print(ed_user is our_user)
    ed_user.password='mon_toto'
    afficher_users(session)
    session.rollback()
    session.commit()
    afficher_users(session)

    jack = User(name='jack', fullname='Jack Bean', password='gjffdd')
    jack.addresses = [Address(email_address='jack@google.com'),Address(email_address='j25@yahoo.com')]
    session.add(jack)
    session.commit()
    liste_adr = session.query(User).join(Address).filter(Address.email_address=='jack@google.com').all()
    print(liste_adr)

if __name__ == '__main__':
    main()

