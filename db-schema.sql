-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/sbbF9O
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.


CREATE TABLE "users" (
    "id" serial   NOT NULL,
    "username" text   NOT NULL,
    "password" text   NOT NULL,
    "email" text   NOT NULL,
    CONSTRAINT "pk_User" PRIMARY KEY (
        "id"
     )
);

CREATE TABLE "favorite_character" (
    "id" serial   NOT NULL,
    "character_id" int   NOT NULL,
    "user_id" int   NOT NULL,
    "added_date" date   NOT NULL,
    "name" text   NOT NULL,
    "image_url" text NOT NULL,
);

ALTER TABLE "User" ADD CONSTRAINT "fk_User_id" FOREIGN KEY("id")
REFERENCES "Favorites" ("user_id");
 