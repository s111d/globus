DROP TABLE IF EXISTS "major";
CREATE TABLE "major" (
	`id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	PRIMARY KEY(id)
);

INSERT INTO major VALUES (1, 'Computer Science');
INSERT INTO major VALUES (2, 'Biology');
INSERT INTO major VALUES (3, 'Advanced Manufacturing');
INSERT INTO major VALUES (4, 'Sustainable Development');

DROP TABLE IF EXISTS "student";
CREATE TABLE "student" (
	`id`	INTEGER NOT NULL,
	`major_id`	INTEGER NOT NULL,
	`first_name` TEXT NOT NULL,
	`last_name` TEXT NOT NULL,
	PRIMARY KEY(id),
	FOREIGN KEY(major_id) REFERENCES major(id)
);
INSERT INTO "student" VALUES (1, 1, 'John', 'Doe');


DROP TABLE IF EXISTS "course";
CREATE TABLE "course" (
	`id`	INTEGER NOT NULL,
	`name`	TEXT NOT NULL,
	`year`  INTEGER NOT NULL,
	-- 1-fall, 2-winter, 3-spring
	`quarter` INTEGER NOT NULL,
	PRIMARY KEY(id)
);
INSERT INTO course VALUES (1, 'Math 1A', 2012, 3);
INSERT INTO course VALUES (2, 'Math 1B', 2012, 1);
INSERT INTO course VALUES (3, 'Math 1C', 2013, 2);
INSERT INTO course VALUES (4, 'Comp Sci 1', 2012, 3);
INSERT INTO course VALUES (5, 'Comp Sci 2', 2012, 1);
INSERT INTO course VALUES (6, 'Comp Sci 100', 2013, 2);
INSERT INTO course VALUES (7, 'Comp Sci 111', 2013, 2);
INSERT INTO course VALUES (8, 'History 10', 2012, 3);
INSERT INTO course VALUES (9, 'English 1', 2012, 1);

DROP TABLE IF EXISTS "student_course_link";
CREATE TABLE "student_course_link" (
	`student_id`	INTEGER NOT NULL,
	`course_id`	INTEGER NOT NULL,
	`mark` TEXT NOT NULL,
	FOREIGN KEY(student_id) REFERENCES student(id),
	FOREIGN KEY(course_id) REFERENCES course(id)
);
CREATE UNIQUE INDEX student_course ON student_course_link(student_id, course_id);

INSERT INTO student_course_link values (1, 3, 'B+'),
                                       (1, 6, 'A'),
                                       (1, 7, 'A-'),
                                       (1, 2, 'B'),
                                       (1, 9, 'A'),
                                       (1, 5, 'A-'),
                                       (1, 1, 'A-'),
                                       (1, 8, 'B+'),
                                       (1, 4, 'A');