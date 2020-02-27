-- When add a rating, update the attribute review_count and average_score of book relation.
CREATE FUNCTION update_star_rating()
   RETURNS trigger AS
   $BODY$
   BEGIN
    IF ....
   END;
   $BODY$

 CREATE TRIGGER trg_upd_b
 AFTER INSERT
 ON rating
 FOR EACH ROW
 EXECUTE PROCEDURE update_star_rating();
