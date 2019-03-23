from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

from collection import Collection
from image import Image

database_name = "image_database.db"  # todo make configurable

engine = create_engine(f'sqlite:///{database_name}')
Session = sessionmaker(bind=engine)
Base = declarative_base()

EXTENSIONS = ('.jpeg', '.jpg', '.png', '.gif')


class ImageRecord(Base):
    __tablename__ = 'images'

    image_id = Column(Integer(), primary_key=True)
    image_path = Column(String(55), nullable=False)
    image_type = Column(String(32))
    # TODO: metadata could be extremely redundant across images.. maybe this should be its own table?
    image_metadata = Column(String(55))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    collection_id = Column(Integer(), ForeignKey('collections.collection_id'))

    # todo: may want to order_by image path? Slow..

    def __repr__(self):
        return f"Image(collection_id='{self.collection_id}', " \
            f"image_path='{self.image_path}', " \
            f"image_type='{self.image_type}', " \
            f"image_metadata='{self.image_metadata}')"

    @classmethod
    def from_image(cls, image: Image, collection_record: 'CollectionRecord') -> 'ImageRecord':
        return ImageRecord(collection_id=collection_record.collection_id,
                           image_path=str(image.path),
                           image_type=image.image_type,
                           image_metadata=str(image.metadata))


class CollectionRecord(Base):
    __tablename__ = 'collections'

    collection_id = Column(Integer(), primary_key=True)
    collection_name = Column(String(55), index=True, nullable=False, unique=True)
    collection_path = Column(String(255))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    images = relationship("ImageRecord", backref="images")

    def __repr__(self):
        return f"CollectionRecord(collection_name='{self.collection_name}', collection_path='{self.collection_path}')"

    @classmethod
    def from_collection(cls, collection: Collection) -> 'CollectionRecord':
        return CollectionRecord(collection_name=collection.name, collection_path=str(collection.path))


def initialize_database():
    Base.metadata.create_all(engine)


def get_session():
    return Session()
