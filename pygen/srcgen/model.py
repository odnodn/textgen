
class Experiment(db.Model):
    __tablename__ = 'Experiment'
    id = db.Column(db.Integer, primary_key=True)
    name_id = Column(Integer, ForeignKey('string.id'))
    notes_id = Column(Integer, ForeignKey('string.id'))

    name = db.relationship('string', back_populates='Experiment', lazy='dynamic')
    notes = db.relationship('string', back_populates='Experiment', lazy='dynamic')


class ExperimentRun(db.Model):
    __tablename__ = 'ExperimentRun'
    id = db.Column(db.Integer, primary_key=True)
    name_id = Column(Integer, ForeignKey('string.id'))
    notes_id = Column(Integer, ForeignKey('string.id'))
    experiment_id = Column(Integer, ForeignKey('Experiment.id'))

    name = db.relationship('string', back_populates='ExperimentRun', lazy='dynamic')
    notes = db.relationship('string', back_populates='ExperimentRun', lazy='dynamic')
    experiment = db.relationship('experiment', back_populates='ExperimentRun', lazy='dynamic')
    groups = db.relationship('group', back_populates='ExperimentRun', lazy='dynamic')
    result = db.relationship('result', back_populates='ExperimentRun', lazy='dynamic')


class Group(db.Model):
    __tablename__ = 'Group'
    id = db.Column(db.Integer, primary_key=True)
    name_id = Column(Integer, ForeignKey('string.id'))

    name = db.relationship('string', back_populates='Group', lazy='dynamic')


class UserGroup(db.Model):
    __tablename__ = 'UserGroup'
    id = db.Column(db.Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('Group.id'))
    user_id = Column(Integer, ForeignKey('MyUser.id'))

    group = db.relationship('group', back_populates='UserGroup', lazy='dynamic')
    user = db.relationship('myUser', back_populates='UserGroup', lazy='dynamic')


class Result(db.Model):
    __tablename__ = 'Result'
    id = db.Column(db.Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('MyUser.id'))
    success_id = Column(Integer, ForeignKey('bool.id'))

    user = db.relationship('myUser', back_populates='Result', lazy='dynamic')
    success = db.relationship('bool', back_populates='Result', lazy='dynamic')


class MyUser(db.Model):
    __tablename__ = 'MyUser'
    id = db.Column(db.Integer, primary_key=True)
    username_id = Column(Integer, ForeignKey('string.id'))

    username = db.relationship('string', back_populates='MyUser', lazy='dynamic')

