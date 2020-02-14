from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, func
from sqlalchemy import (
    Integer, String, DateTime, Text,
    ForeignKey, text
)
import os

backend_path = os.path.dirname(os.path.abspath(__file__))
db_file_path = os.path.join(backend_path, "db.sqlite3")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file_path}"
db = SQLAlchemy(app)


class VideoMeasurement(db.Model):
    __tablename__ = 'video_measurement'

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer, ForeignKey('video.id', ondelete="CASCADE"))
    video = relationship("Video", back_populates="measurements")
    measurement_date = Column(DateTime())
    sub_count = Column(Integer, server_default=text("0"))
    comments = Column(Integer, server_default=text("0"))
    subscribersgained = Column(Integer, server_default=text("0"))
    subscriberslost = Column(Integer, server_default=text("0"))
    unsub_views = Column(Integer, server_default=text("0"))
    unsub_likes = Column(Integer, server_default=text("0"))
    unsub_dislikes = Column(Integer, server_default=text("0"))
    unsub_shares = Column(Integer, server_default=text("0"))

    def as_json(self):
        return {
            'id': self.id,
            'video_id': self.video_id,
            'measurement_date': self.measurement_date.isoformat(),
            'comments': self.comments,
            'subscribersgained': self.subscribersgained,
            'subscriberslost': self.subscriberslost,
            'unsub_views': self.unsub_views,
            'unsub_likes': self.unsub_likes,
            'unsub_dislikes': self.unsub_dislikes,
            'unsub_shares': self.unsub_shares,
        }


class Video(db.Model):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True, autoincrement=True)
    youtube_id = Column(String(128))
    channel_id = Column(Integer, ForeignKey('channel.id'))
    channel = relationship("Channel", back_populates="videos")
    create_date = Column(DateTime())
    title = Column(String(128))
    description = Column(Text())
    duration = Column(Integer)
    measurements = relationship(
        "VideoMeasurement", cascade="all,delete",
        back_populates="video", passive_deletes=True)

    def as_json(self):
        return {
            'id': self.id,
            'youtube_id': self.youtube_id,
            'channel_id': self.channel_id,
            'create_date': self.create_date,
            'title': self.title,
            'duration': self.duration,
            'description': self.description,
        }


class Channel(db.Model):
    __tablename__ = 'channel'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))
    videos = relationship("Video")

    def as_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }


@app.route('/results', methods=['GET'])
def results():
    query = db.session.query(
        VideoMeasurement,
        Video,
        Channel,
        func.max(VideoMeasurement.measurement_date)
    ).join(
        Video, Video.id == VideoMeasurement.video_id
    ).join(
        Channel, Channel.id == Video.channel_id
    ).group_by(Channel, Video)

    results = query.all()

    data = []
    for result in results:
        measurement = result[0].as_json()
        measurement['video'] = result[1].as_json()
        measurement['video']['channel'] = result[2].as_json()
        data.append(measurement)

    return jsonify(data)


if __name__ == '__main__':
    app.run()
