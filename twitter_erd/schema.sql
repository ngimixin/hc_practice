-- users
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users (
  id                BIGSERIAL PRIMARY KEY,
  email             VARCHAR NOT NULL UNIQUE,
  username          VARCHAR NOT NULL UNIQUE,
  phone_number      VARCHAR NULL UNIQUE,
  full_name         VARCHAR NOT NULL,
  bio               TEXT NULL,
  location          VARCHAR NULL,
  website           VARCHAR NULL,
  birthdate         DATE NOT NULL,
  profile_image_url VARCHAR,
  avatar_image_url  VARCHAR,
  created_at        TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at        TIMESTAMP NOT NULL DEFAULT NOW()
);

-- tweets
DROP TABLE IF EXISTS tweets CASCADE;
CREATE TABLE tweets (
  id                   BIGSERIAL PRIMARY KEY,
  user_id              BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  body                 VARCHAR(140) NOT NULL,
  in_reply_to_tweet_id BIGINT NULL REFERENCES tweets(id) ON DELETE SET NULL,
  created_at           TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at           TIMESTAMP NOT NULL DEFAULT NOW()
);

-- likes
DROP TABLE IF EXISTS likes CASCADE;
CREATE TABLE likes (
  id          BIGSERIAL PRIMARY KEY,
  user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  tweet_id    BIGINT NOT NULL REFERENCES tweets(id) ON DELETE CASCADE,
  created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMP NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, tweet_id)
);

-- retweets
DROP TABLE IF EXISTS retweets CASCADE;
CREATE TABLE retweets (
  id          BIGSERIAL PRIMARY KEY,
  user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  tweet_id    BIGINT NOT NULL REFERENCES tweets(id) ON DELETE CASCADE,
  created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMP NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, tweet_id)
);

-- bookmarks
DROP TABLE IF EXISTS bookmarks CASCADE;
CREATE TABLE bookmarks (
  id          BIGSERIAL PRIMARY KEY,
  user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  tweet_id    BIGINT NOT NULL REFERENCES tweets(id) ON DELETE CASCADE,
  created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at  TIMESTAMP NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, tweet_id)
);

-- follows
DROP TABLE IF EXISTS follows CASCADE;
CREATE TABLE follows (
  id            BIGSERIAL PRIMARY KEY,
  follower_id   BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  followee_id   BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMP NOT NULL DEFAULT NOW(),
  CONSTRAINT chk_follow_not_self CHECK (follower_id <> followee_id),
  UNIQUE (follower_id, followee_id)
);

-- direct_messages
DROP TABLE IF EXISTS direct_messages CASCADE;
CREATE TABLE direct_messages (
  id            BIGSERIAL PRIMARY KEY,
  sender_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  recipient_id  BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  body          TEXT NOT NULL,
  read_at       TIMESTAMP NULL,
  created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at    TIMESTAMP NOT NULL DEFAULT NOW(),
  CHECK (sender_id <> recipient_id)
);

-- notifications
DROP TABLE IF EXISTS notifications CASCADE;
CREATE TABLE notifications (
  id             BIGSERIAL PRIMARY KEY,
  user_id        BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,   -- 受け手
  actor_user_id  BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,   -- 行為者
  type           VARCHAR NOT NULL,                                         -- 'like'|'follow'|'retweet'|'direct_message' など
  tweet_id       BIGINT NULL REFERENCES tweets(id) ON DELETE CASCADE,
  direct_message_id BIGINT NULL REFERENCES direct_messages(id) ON DELETE CASCADE,
  read_at        TIMESTAMP NULL,
  created_at     TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at     TIMESTAMP NOT NULL DEFAULT NOW()
);
