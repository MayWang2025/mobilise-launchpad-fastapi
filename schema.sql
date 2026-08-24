BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Audit_logs" (
	"log_id"	INTEGER,
	"user_id"	TEXT NOT NULL,
	"action"	TEXT NOT NULL,
	"timestamp"	TEXT NOT NULL,
	"details"	TEXT,
	PRIMARY KEY("log_id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Booking_results" (
	"booking_id"	INTEGER,
	"worker_id"	TEXT NOT NULL,
	"booking_type"	TEXT NOT NULL,
	"booking_status"	TEXT NOT NULL,
	"booking_details"	TEXT NOT NULL,
	PRIMARY KEY("booking_id" AUTOINCREMENT),
	FOREIGN KEY("worker_id") REFERENCES "Workforce"("worker_id")
);
CREATE TABLE IF NOT EXISTS "Eligibility_results" (
	"eligibility_id"	INTEGER,
	"worker_id"	TEXT NOT NULL,
	"eligibility_status"	TEXT NOT NULL,
	"assessment_reason"	TEXT NOT NULL,
	PRIMARY KEY("eligibility_id" AUTOINCREMENT),
	FOREIGN KEY("worker_id") REFERENCES "Workforce"("worker_id")
);
CREATE TABLE IF NOT EXISTS "Mobilisation_requests" (
	"request_id"	TEXT NOT NULL,
	"worker_id"	TEXT NOT NULL,
	"project"	TEXT NOT NULL,
	"site"	TEXT NOT NULL,
	"start_date"	TEXT NOT NULL,
	"end_date"	TEXT NOT NULL,
	"role"	TEXT NOT NULL,
	"status"	TEXT NOT NULL,
	PRIMARY KEY("request_id"),
	FOREIGN KEY("worker_id") REFERENCES "Workforce"("worker_id")
);
CREATE TABLE IF NOT EXISTS "Workforce" (
	"worker_id"	TEXT NOT NULL,
	"name"	TEXT NOT NULL,
	"role"	TEXT,
	"work_status"	TEXT,
	"employment_status"	TEXT,
	"work_rights"	TEXT,
	"site_induction"	TEXT,
	"medical_clearance"	TEXT,
	"qualification_status"	TEXT,
	PRIMARY KEY("worker_id")
);
COMMIT;
