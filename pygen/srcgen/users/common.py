#Model = declarative_base()
# engine = create_engine('sqlite:///:memory:', echo=True)
# Model.metadata.create_all(engine)
#
# Session = sessionmaker(bind=engine)
# session = Session()

from sqlalchemy import orm
Session = orm.scoped_session(orm.sessionmaker())