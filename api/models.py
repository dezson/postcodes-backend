from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Store(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    postcode = db.Column(db.String(255), nullable=False)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)

    def __rerp__(self):
        return f"Product {self.id} {self.name} {self.postcode} {self.longitude} {self.latitude}"

    def to_dict(self):
        """Converting data model to dict without ID, Latitude, Longitude fields"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in ["id",
                                                                                                "longitude",
                                                                                                "latitude"]}

    def to_verbose_dict(self):
        """Converting data model to dict without ID field"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name is not "id"}
