CREATE or replace FUNCTION array_append_2d(integer[][], integer[])
    RETURNS integer[][]
    LANGUAGE SQL
    AS 'select array_cat($1, ARRAY[$2])'
    IMMUTABLE
;
CREATE or replace FUNCTION array_append_2d(numeric[][], numeric[])
    RETURNS numeric[][]
    LANGUAGE SQL
    AS 'select array_cat($1, ARRAY[$2])'
    IMMUTABLE
;
CREATE or replace FUNCTION array_append_2d(double precision[][], double precision[])
    RETURNS double precision[][]
    LANGUAGE SQL
    AS 'select array_cat($1, ARRAY[$2])'
    IMMUTABLE
;

CREATE ORDERED AGGREGATE array_agg_array(double precision[])
(
    SFUNC = array_append_2d,
    STYPE = double precision[][]
);


DROP TABLE offer;
CREATE TABLE offer (offerid int, userid int, asktimes int, askbackoffdays int, bought_offer int);
INSERT into offer values(1, 1, 2, 1, 0);
INSERT into offer values(2, 1, 2, 3, 0);
INSERT into offer values(3, 1, 4, 7, 1);
INSERT into offer values(4, 1, 4, 7, 1);
INSERT into offer values(5, 1, 6, 7, 1);
INSERT into offer values(6, 2, 2, 7, 0);
INSERT into offer values(7, 2, 2, 7, 0);
INSERT into offer values(8, 2, 4, 7, 0);
INSERT into offer values(9, 2, 4, 7, 0);
INSERT into offer values(10, 2, 6, 7, 1);


SELECT * from offer;

CREATE TABLE offers_train_agg
AS
SELECT
    array_agg(offerid) as ids,
    array_agg_array(feature_vec) AS features,
    array_agg(bought_offer) as y_vector
FROM (
    SELECT
        offerid,
        bought_offer,
        ARRAY[
            asktimes,
            askbackoffdays
        ] AS feature_vec
    FROM offer
) tmp
;


def logreg_train(features, targets):
    from sklearn.linear_model import LogisticRegression
    import six
    pickle = six.moves.cPickle
    logreg = LogisticRegression(solver='lbfgs')
    logreg.fit(features, targets)
    return pickle.dumps(logreg, protocol=2)
)

DROP FUNCTION IF EXISTS logreg_train(features float[][], targets integer[]);
CREATE OR REPLACE FUNCTION
        logreg_train(features float[][], targets integer[])
RETURNS bytea
LANGUAGE plpythonu
AS
$$
def logreg_train(features, targets):
    from sklearn.linear_model import LogisticRegression
    import six
    pickle = six.moves.cPickle

    logreg = LogisticRegression(solver='lbfgs')
    logreg.fit(features, targets)
    return pickle.dumps(logreg, protocol=2)

return logreg_train(features, targets)
$$;

CREATE TABLE logreg_model
AS
SELECT
    logreg_train(features, y_vector) as model,
    now() as serialized_on
FROM offers_train_agg;

SELECT serialized_on, length(model), model::text
FROM logreg_model;

CREATE OR REPLACE FUNCTION
        sklearn_predict_1(serialized_model bytea, features float[])
RETURNS float
LANGUAGE plpythonu
AS
$$
def sklearn_predict_1(serialized_model, features):
    import six
    pickle = six.moves.cPickle
    model = pickle.loads(serialized_model)
    result = model.predict_proba([features])
    return result[0, 1]

return sklearn_predict_1(serialized_model, features)
$$;

CREATE TABLE other_offers (asktimes int, askbackoffdays int);
insert into other_offers values (1.0, 1.0);
insert into other_offers values (2.0, 2.0);
insert into other_offers values (3.0, 3.0);
insert into other_offers values (4.0, 4.0);
insert into other_offers values (5.0, 5.0);
insert into other_offers values (6.0, 6.0);
insert into other_offers values (7.0, 7.0);
insert into other_offers values (8.0, 8.0);
insert into other_offers values (9.0, 9.0);

SELECT sklearn_predict_1((SELECT model::bytea from logreg_model), '{1.0, 1.0}');


SELECT
    feature_vec,
    sklearn_predict_1((
        SELECT model::bytea from logreg_model),
    feature_vec)
FROM (
    SELECT
        ARRAY[
            asktimes,
            askbackoffdays
        ] AS feature_vec
    FROM other_offers
) tmp order by 2
;


CREATE TABLE offers_by_user_train_agg
AS
SELECT
    userid,
    array_agg(offerid) as ids,
    array_agg_array(feature_vec) AS features,
    array_agg(bought_offer) as y_vector
FROM (
    SELECT
        userid,
        offerid,
        bought_offer,
        ARRAY[
            asktimes,
            askbackoffdays
        ] AS feature_vec
    FROM offer
) tmp
GROUP BY userid
;
select * from offers_by_user_train_agg;

CREATE TABLE logreg_model_by_user
AS
SELECT
    userid,
    logreg_train(features, y_vector) as model,
    now() as serialized_on
FROM offers_by_user_train_agg;
SELECT * from logreg_model_by_user;



