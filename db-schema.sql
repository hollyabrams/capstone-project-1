-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/sbbF9O
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "User" (
    "id" serial   NOT NULL,
    "username" text   NOT NULL,
    "password" text   NOT NULL,
    "email" text   NOT NULL,
    CONSTRAINT "pk_User" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "Character" (
    "_id" serial   NOT NULL,
    "name" text   NOT NULL,
    "imageUrl" string   NOT NULL,
    CONSTRAINT "pk_Character" PRIMARY KEY (
        "_id"
     )
);

CREATE TABLE "Favorites" (
    "user_id" int   NOT NULL,
    "character_id" int   NOT NULL
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

ALTER TABLE "Favorites" ADD CONSTRAINT "fk_Favorites_user_id" FOREIGN KEY("user_id")
REFERENCES "User" ("id");

ALTER TABLE "Favorites" ADD CONSTRAINT "fk_Favorites_character_id" FOREIGN KEY("character_id")
REFERENCES "Character" ("_id");

ALTER TABLE "Feedback" ADD CONSTRAINT "fk_Feedback_id" FOREIGN KEY("id")
REFERENCES "User" ("id");

