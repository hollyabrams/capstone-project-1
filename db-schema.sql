-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/sbbF9O
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "Character" (
    "_id" serial   NOT NULL,
    "name" string   NOT NULL,
    "imageUrl" string   NOT NULL,
    "url" string   NOT NULL,
    CONSTRAINT "pk_Character" PRIMARY KEY (
        "_id"
     )
);

CREATE TABLE "Film" (
    "id" serial   NOT NULL,
    "title" text   NOT NULL,
    CONSTRAINT "pk_Film" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "CharacterFilms" (
    "characterFilms" serial   NOT NULL,
    "character_id" int   NOT NULL,
    "film_id" int   NOT NULL,
    CONSTRAINT "pk_CharacterFilms" PRIMARY KEY (
        "characterFilms"
     )
);

CREATE TABLE "ParkAttraction" (
    "id" serial   NOT NULL,
    "name" string   NOT NULL,
    CONSTRAINT "pk_ParkAttraction" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "CharacterParkAttractions" (
    "id" serial   NOT NULL,
    "character_id" int   NOT NULL,
    "parkAttraction_id" int   NOT NULL,
    CONSTRAINT "pk_CharacterParkAttractions" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "User" (
    "id" serial   NOT NULL,
    "username" text   NOT NULL,
    "password" text   NOT NULL,
    "email" text   NOT NULL,
    CONSTRAINT "pk_User" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "FavoriteCharacters" (
    "favorite_id" serial   NOT NULL,
    "user_id" int   NOT NULL,
    "character_id" int   NOT NULL,
    CONSTRAINT "pk_FavoriteCharacters" PRIMARY KEY (
        "favorite_id"
     )
);

CREATE TABLE "Feedback" (
    "id" serial   NOT NULL,
    "user_id" int   NOT NULL,
    "feedbackDate" date   NOT NULL,
    "feedbackContent" text   NOT NULL,
    CONSTRAINT "pk_Feedback" PRIMARY KEY (
        "id"
     )
);

ALTER TABLE "CharacterFilms" ADD CONSTRAINT "fk_CharacterFilms_character_id" FOREIGN KEY("character_id")
REFERENCES "Character" ("_id");

ALTER TABLE "CharacterFilms" ADD CONSTRAINT "fk_CharacterFilms_film_id" FOREIGN KEY("film_id")
REFERENCES "Film" ("id");

ALTER TABLE "CharacterParkAttractions" ADD CONSTRAINT "fk_CharacterParkAttractions_character_id" FOREIGN KEY("character_id")
REFERENCES "Character" ("_id");

ALTER TABLE "CharacterParkAttractions" ADD CONSTRAINT "fk_CharacterParkAttractions_parkAttraction_id" FOREIGN KEY("parkAttraction_id")
REFERENCES "ParkAttraction" ("id");

ALTER TABLE "FavoriteCharacters" ADD CONSTRAINT "fk_FavoriteCharacters_user_id" FOREIGN KEY("user_id")
REFERENCES "User" ("id");

ALTER TABLE "FavoriteCharacters" ADD CONSTRAINT "fk_FavoriteCharacters_character_id" FOREIGN KEY("character_id")
REFERENCES "Character" ("_id");

ALTER TABLE "Feedback" ADD CONSTRAINT "fk_Feedback_user_id" FOREIGN KEY("user_id")
REFERENCES "User" ("id");

