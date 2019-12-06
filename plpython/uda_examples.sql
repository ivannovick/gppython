CREATE TABLE test_results (testtype int, testresults int[], test_attr int[]);

INSERT into test_results VALUES
(10, '{32,131,13,331,323}', '{33,33,33,11,11}'),
(10, '{21,11,13,34,2}', '{11,11,11,11,11}'),
(20, '{222,112,212,233,191}', '{33,33,33,33,11}'),
(20, '{44,12,66,81,99,100}', '{33,44,44,11,44}'),
(30, '{89,85,80,88,89}', '{11,33,33,11,33}');

SELECT count(*) from test_results group by testtype;

CREATE OR REPLACE FUNCTION segment_array_concat(a int[], b int[])
  RETURNS int[] AS $$
  return a+b
$$
LANGUAGE plpythonu
IMMUTABLE
RETURNS NULL ON NULL INPUT;

CREATE OR REPLACE FUNCTION master_array_concat(a int[], b int[])
  RETURNS int[] AS $$
  return a+b
$$
LANGUAGE plpythonu
IMMUTABLE
RETURNS NULL ON NULL INPUT;

DROP AGGREGATE gp_concat_arrays(int[]);
CREATE AGGREGATE gp_concat_arrays(int[]) (
   SFUNC = master_array_concat,
   PREFUNC = segment_array_concat,
   STYPE = int[]);


EXPLAIN SELECT gp_concat_arrays(testresults) from test_results;

SELECT gp_concat_arrays(testresults) from test_results;

EXPLAIN SELECT gp_concat_arrays(testresults) from test_results group by testtype;

SELECT gp_concat_arrays(testresults) from test_results group by testtype;
